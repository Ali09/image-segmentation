from random import randint # for rgb ranges
from Grammer import Search # Abstract Base Class

class randomSearch(Search):
    # Random Search Class that randomly alters the
    # parameter space to find an optimal fitness
    
    def __init__(self, segmenter, fitness):
        # Requires: -segmenter is of type Segment
        #           -fitness is of type Fitness
        # Modifies: this
        # Effects: tells Search which segmenter and fitness function to use
        self.segmenter = segmenter
        self.fitness = fitness
    
    def searchImage(self, imageData, idealMaskData, parameters):
        # Requires: -image and idealMask is an RGB based image such as a .png file'
        #           -parameters is of type Parameters
        # Modifies: parameters
        # Effects:  Randomly searches the parameter space
        #           for an optimal solution, and returns most optimal parameter found
        print "Running random search"
        
        curBestRGB = self.randRgbRange()
        parameters.setRgbRanges(curBestRGB)
        mask = self.segmenter.segmentImage(imageData, parameters)
        curBestFit = self.fitness.findFitness(mask, idealMaskData, parameters)
        
        iterations = int(raw_input("How many iterations do you want random search to run: "))
        
        for i in range(iterations):
            newRGB =  self.randRgbRange()
            parameters.setRgbRanges(newRGB)
            print "Iteration " + str(i + 1) 
            mask = self.segmenter.segmentImage(imageData, parameters)
            newFit = self.fitness.findFitness(mask, idealMaskData, parameters)
            
            if newFit < curBestFit:
                curBestRGB = newRGB
                curBestFit = newFit
        
        parameters.setRgbRanges(curBestRGB)
        return parameters
    
    def randRgbRange(self):
        # Effects: returns three 2-tuples of valid RGB Min-Max's
        rgbRangeList = []
        for i in range(6):
            rgbRangeList.append(randint(0,255))
        for i in [1,3,5]:
            if rgbRangeList[i] < rgbRangeList[i - 1]:
                rgbRangeList[i] = randint(rgbRangeList[i - 1], 255)
        return (rgbRangeList[0:2], rgbRangeList[2:4], rgbRangeList[4:6])