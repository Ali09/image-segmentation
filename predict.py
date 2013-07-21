from imaging import dataToImage # to save masks for predict
import glob # get filenames for predict
import pylab # to plot for predict
import Image # to open files
from imaging import colorSpaceConvert # to convert color spaces for new images
import datetime # for output plot file name
import numpy # for mean, median, and standard deviation

def predict(folderName, parameters, segmentAlgo,
            fitnessFunc, plot = False, exportImages = False):
    # Requires: -parameters is of type Parameters
    #           -segmentAlgo is of type Segment
    #           -fitnessFunc is of type Fitness
    #           -folder is a string of a folder which contains two subfolders:
    #               -original which contains the original image
    #               -manualsegmentations which contains segmentations
    #                of the original images, the segmentations have the same
    #                name and are of .png format
    #           -plot and export is of type Bool
    # Effects: -attempts to segment images inside of the speicied folder
    #           based on the single sample image / mask provided to the system
    #          -outputs a histogram plot, "plot-date-time.png", of the fitness
    #           distrubution of the images segmented if plot = True
    #          -saves masks of the segmented images if export = True
    file_list = glob.glob(folderName + "original/" + "*")
    
    prefixLen = len(folderName) + len("original/")
    suffixLen = len(file_list[0].split(".")[-1]) + 1
    
    fitnessList = []
    
    iteration = 1
    for fileName in file_list:
        image = Image.open(fileName)
        if parameters.colorSpace in ("hsv", "hls"):
            imageData = colorSpaceConvert(list(image.getdata()), parameters.colorSpace)
        else:
            imageData = colorSpaceConvert(list(image.getdata()), parameters.colorSpace)
            
        
        maskname = fileName[prefixLen:-suffixLen] + ".png"
        mask = Image.open(folderName + "manualsegmentations/" + maskname)
        idealMaskData = list(mask.getdata())
        
        parameters.setImageSize(image.size)
        
        maskData = segmentAlgo.segmentImage(imageData, parameters, True)
        fit = fitnessFunc.findFitness(maskData, idealMaskData, parameters)
        
        # save mask if export enabled
        if exportImages == True:
            dataToImage(maskData, image.size, "-" + str(iteration))
        
        fitnessList.append(fit / float(image.size[0] * image.size[1]))
        iteration += 1
    
    time = datetime.datetime.now()
    
    npFitnessList = numpy.array(fitnessList)
    mu = npFitnessList.mean()
    median = numpy.median(npFitnessList)
    sigma = npFitnessList.std()
    textstr = '$\overline{x}=%.2f$\n$\mathrm{median}=%.2f$\n$\sigma=%.2f$'%(mu, median, sigma)
    
    fig, ax = pylab.subplots(1)
    
    pylab.hist(fitnessList, bins = 10)
    pylab.xlabel('Fitness ratio (Fitness / Image Size)')
    pylab.ylabel('Number of Images')
    pylab.title('Number of Images vs. Fitness Ratio')
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    pylab.text(0.78, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    
    timeString = "output-" + str(time.month) + '.' + str(time.day) + '.' + str(time.year) 
    timeString += '-' + str(time.hour) + '.' + str(time.minute)  
     
    pylab.savefig("plotImages" + timeString + ".png")