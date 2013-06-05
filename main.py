#!/usr/bin/env python
"""Main Image Semgentation testing program
Usage options:
    
    Optional:
    -h --help    Prints this help message
    -e --export  Saves generated mask as output.png
    -p --plot    Exports a plot of fitness vs. iterations (for random search)
    
    Required:
    -d --seg     Segmentation tool: 'rgb', 'hsv', 'hls' ...
    -f --fitness Fitness function:  'diff', ...
    -s --search  Search function:   'random', ...
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
import search
import parameters

def main():
    # commented out try for debugging purposes
    #try:
        shortOpts = "d:f:s:i:m:hep"
        longOpts = ["segment=", "fitness=", "search=", "image=", "mask=", "help", "export", "plot"]
        
        try:
            options, remainder = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
        except:
            print "\nERROR: Invalid option argument\n"
            exit(1)
        
        export = False
        plot = False
        
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
            elif opt in ("-h", "--help"):
                print __doc__
                exit(0)
            else:
                pass
                
        if remainder != []:
            print "\nERROR: Extraneous input\n"
            exit(1)
            
        # initialize program based on arguments
        if segmenterName.lower() in ("rgb", "hsv", "hls"):
            segmenter = segmentation.colorSegmenter()
        else:
            print "\nERROR: Invalid or no segmenter name\n"
            exit(1)
        
        if fitnessName.lower() == "diff":
            fitnessFunc = fitness.absDiffFitness()
        else:
            print "\nERROR: Invalid or no fitness name\n"
            exit(1)
        
        if searchName.lower() == "random":
            searchFunc = search.randomSearch(segmenter, fitnessFunc)
        else:
            print "\nERROR: Invalid or no search name\n"
            exit(1)
        
        try:
            image = Image.open(imageName)
            imageData = colorSpaceConvert(list(image.getdata()), segmenterName)
        except:
            print "\nERROR: Invalid or no image name\n"
            exit(1)
            
        try:
            mask = Image.open(idealMaskName)
            idealMaskData = list(mask.getdata())
        except:
            print "\nERROR: Invalid or no mask name\n"
            exit(1)
        
        parameter = parameters.Parameters()
        parameter.setImageSize(image.size)
        parameter.setColorSpace(segmenterName)
        
        # run search on image, returns optimal paramaters found
        optimalParameters = searchFunc.searchImage(imageData, idealMaskData, parameter, plot)
        
        # saves mask to output.png if export option set
        if (export == True):
            segmenter.segmentImage(imageData, optimalParameters, True)
    
    #except:
    #    print "Type -h or --help for option info\n"
        

main()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
