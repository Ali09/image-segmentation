# Implementations of fitness subclasses

import Image # for image data
from Grammer import Fitness # Abstract Base Class

class absDiffFitness(Fitness):
    # Absolute Difference Fitness Class, 
    # finds # of differing White/Black pixels in generated mask to ideal mask
    def __init__(self):
        pass
    
    def findFitness(self, generatedMaskData, idealMaskData, parameters):
        # Requires: -both inputs are RGB (0 - 255) based images
        # Effects:  -returns # of black/white pixels in generated mask
        #            that differ from ideal mask
        #           -if upperLimit in parameters is set to a non-default value, then
        #            the fitness function will stop calculations
        #            if the fitness exceeds the upper limit and return
        #            upper limit + 1 as the fitness; this is implemented
        #            so as to make calculations faster when used in conjunction
        #            with another algorithm such as random search
        totalDiff = 0
        for i in range(len(generatedMaskData)):
            totalDiff += abs(generatedMaskData[i][0]/255 - idealMaskData[i][0]/255)
            if totalDiff > parameters.upperLimit:
                return totalDiff
        return totalDiff

