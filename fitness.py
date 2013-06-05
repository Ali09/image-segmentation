# Implementations of fitness subclasses

import Image # for image data
from Grammer import Fitness # Abstract Base Class

class absDiffFitness(Fitness):
    # Absolute Difference Fitness Class, 
    # finds # of differing White/Black pixels in generated mask to ideal mask
    def __init__(self):
        pass
    
    def findFitness(self, generatedMaskData, idealMaskData, parameters):
        # Requires: both inputs are RGB (0 - 255) based images
        # Effects:  returns # of black/white pixels in generated mask
        #           that differ from ideal mask
        totalDiff = 0
        for i in range(len(generatedMaskData)):
            totalDiff += abs(generatedMaskData[i][0]/255 - idealMaskData[i][0]/255)
        return totalDiff

