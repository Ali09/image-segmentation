# Implementations of segmentation sublcasses

from Grammer import Segment # Abstract Base Class
from imaging import dataToImage # convert output mask data to image


class colorSegmenter(Segment):
    # RGB Segmenter Class that segments an image
    # based on ranges of RGB parameters
    
    def __init__(self):
        pass
    
    def segmentImage(self, imageData, parameters, saveMaskImage = False):
        # Requires: -imageData holds 0-1 values of color values (either RGB, HSV, or HLS)
        #           -parameters is three 2-tuple numbers between 0 - 1 that
        #            respectively represent (min, max) color ranges for foreground selection
        # Effects:  returns an RGB mask-list where 
        #           (0, 0, 0) is background, (255, 255, 255) is foreground
        if (parameters.colorRanges == None):
            print "No color range set!"
            exit(1)
        
        colorRanges = parameters.colorRanges
        
        #check for bounds errors
        for tuples in colorRanges:
            if tuples[0] > tuples[1]:
                print "Min > Max in parameter!"
                exit(1)
            
            for number in tuples:
                if not (0 <= number <= 1):
                    print "Parameter not within 0 - 1 range!"
                    exit(1)
        
        # xRange either R or H
        # yRange either G or S
        # zRange either B or V or L
        xRange = colorRanges[0]
        yRange = colorRanges[1]
        zRange = colorRanges[2]
        
        isForeground = lambda x: (xRange[0] <= x[0] <= xRange[1] and
                                  yRange[0] <= x[1] <= yRange[1] and
                                  zRange[0] <= x[2] <= zRange[1])
        
        
        # if flip bit off, act normally,
        # else switch background and foreground
        if parameters.flipBit == False:
            foreground = (255, 255, 255)
            background = (0, 0, 0)
        else:
            foreground = (0, 0, 0)
            background = (255, 255, 255)
        
        mask = [background] * len(imageData)
        
        for i in range(len(imageData)):
            if isForeground(imageData[i]):
                mask[i] = foreground
        
        if saveMaskImage == True:
            dataToImage(mask, parameters.imageSize)
        
        return mask



