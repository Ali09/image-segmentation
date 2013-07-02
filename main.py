#!/usr/bin/env python
"""Main Image Semgentation testing program
Usage options:
    
    Optional:
    -h --help    Prints this help message
    -e --export  Saves generated mask as output-date-time.png
    -p --plot    Exports a plot of fitness vs. iterations (for random search)
    -c --close   Fills in black regions surrounded by white regions in final image mask,
                 filled in mask only visible to user if export set true
    
    Required:
    -d --seg     Segmentation tool: 'rgb', 'hsv', 'hls', ...
    -f --fitness Fitness function:  'diff', ...
    -s --search  Search function:   'random', 'genetic', 'anneal', ...
    -i --image   Image filename
    -m --mask    Ideal Mask filename
    
Example:
        
    >>>  main.py -d rgb -f diff -s random --image cameleon.png --mask cameleonMask.png
    >>>  How many iterations do you want random search to run: 10    
    Iteration 1
    Iteration 2
    ...
"""

import sys # for argv
import Image # for image data
import getopt # for command line parsing
from imaging import colorSpaceConvert # for color space converting
import segmentation
import fitness
import RandomSearch
import GeneticSearch
import AnnealSearch
import parameters
import closure

def main():
    # commented out try for debugging purposes
    #try:
        shortOpts = "d:f:s:i:m:hepc"
        longOpts = ["segment=", "fitness=", "search=", "image=", 
                    "mask=", "help", "export", "plot", "close"]
        
        try:
            options, remainder = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
        except:
            print "\nERROR: Invalid option argument\n"
            exit(1)
        
        export = False
        plot = False
        close = False
        
        # sets relevant variables based on command line input
        for opt, arg in options:
            if opt in ("-d", "--segment"):
                segmenterName = arg
            elif opt in ("-f", "--fitness"):
                fitnessName = arg
            elif opt in ("-s", "--search"):
                searchName = arg
            elif opt in ("-i", "--image"):
                imageName = arg
            elif opt in ("-m", "--mask"):
                idealMaskName = arg
            elif opt in ("-e", "--export"):
                export = True
            elif opt in ("-p", "--plot"):
                plot = True
            elif opt in ("-c", "--close"):
                close = True
            elif opt in ("-h", "--help"):
                print __doc__
                exit(0)
            else:
                pass
        
        # quit if extraneous input provided       
        if remainder != []:
            print "\nERROR: Extraneous input\n"
            exit(1)
            
        # initialize segmenter algorithm
        if segmenterName.lower() in ("rgb", "hsv", "hls"):
            segmenter = segmentation.colorSegmenter()
        else:
            print "\nERROR: Invalid or no segmenter name\n"
            exit(1)
        
        # initialize fitness function
        if fitnessName.lower() == "diff":
            fitnessFunc = fitness.absDiffFitness()
        else:
            print "\nERROR: Invalid or no fitness name\n"
            exit(1)
        
        # initialize search space algorithm
        if searchName.lower() == "random":
            searchFunc = RandomSearch.randomSearch(segmenter, fitnessFunc)
        elif searchName.lower() == "genetic":
            searchFunc = GeneticSearch.geneticSearch(segmenter, fitnessFunc)
        elif searchName.lower() == "anneal":
            searchFunc = AnnealSearch.annealSearch(segmenter, fitnessFunc)
        else:
            print "\nERROR: Invalid or no search name\n"
            exit(1)
        
        # try to open image, and convert image data from a [0, 255] RGB space 
        # to a [0, 1] normalized RGB, HSV, or HLS space, depending on the segmenter selected
        # (chooses HSV or HLS if their respective segmenter is selected, else selects RGB)
        # if opening image fails, quit with error
        try:
            image = Image.open(imageName)
        
            if segmenterName.lower() in ("hsv", "hls"):
                imageData = colorSpaceConvert(list(image.getdata()), segmenterName.lower())
            else:
                imageData = colorSpaceConvert(list(image.getdata()), "rgb")
                
        except:
            print "\nERROR: Invalid or no image name\n"
            exit(1)
            
        # try to open ideal mask, if it fails, quit with error
        try:
            mask = Image.open(idealMaskName)
            idealMaskData = list(mask.getdata())
        except:
            print "\nERROR: Invalid or no mask name\n"
            exit(1)
        
        # initialize parameters object, init's image size and color space used
        parameter = parameters.Parameters()
        parameter.setImageSize(image.size)
        parameter.setColorSpace(segmenterName.lower())
        
        # run search on image parameter space for segmentation
        # returns optimal paramaters found upon search completion
        # and saves a plot of fitness vs. search extent if plot set to true
        optimalParameters = searchFunc.searchImage(imageData, idealMaskData, parameter, plot)
        
        # if export enabled, saves mask using optimal parameters found to output.png
        if (export == True):
            segmenter.segmentImage(imageData, optimalParameters, True)
        
        # if export enabled, saves a 'closed' mask using optimal parameters found to output.png
        if (close == True):
            mask = segmenter.segmentImage(imageData, optimalParameters)
            close = closure.closure()
            close.segmentRegions(mask, optimalParameters, saveImage = export)

        
    
    #except:
    #    print "Type -h or --help for option info\n"
        

main()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
