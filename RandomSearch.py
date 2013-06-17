# Implementations of search subclass random search

from random import random # for [0, 1) random values
from random import choice # for random flip bit value
from random import randint # for color ranges
from Grammer import Search # Abstract Base Class
import pylab # for plotting
from copy import deepcopy # make deep copy for parameters

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
    
    def searchImage(self, imageData, idealMaskData, parameters, plot = False):
        # Requires: -image and idealMask is an RGB based image such as a .png file'
        #           -parameters is of type Parameters
        # Modifies:  parameters
        # Effects: -Randomly searches the parameter space
        #           for an optimal solution, and returns most optimal parameter found
        #          -plots fitness vs. iterations of search if plot set to True
        
        print "Running random search"
        
        curBestColorRange = self.randColorRange()
	curBestFlipBit = choice([True, False])
        parameters.setColorRanges(curBestColorRange)
	parameters.setFlipBit(curBestFlipBit)
        mask = self.segmenter.segmentImage(imageData, parameters)
        curBestFit = self.fitness.findFitness(mask, idealMaskData, parameters)
        parameters.setUpperLimit(curBestFit)
        
        iterations = int(raw_input("How many iterations do you want random search to run: "))
        
        # if plotting enabled, make a list
        if plot == True:
            self.fitnessList = [curBestFit]
            self.iterationsList = [0]
        
        for i in range(iterations):
            newColorRange =  self.randColorRange()
	    newFlipBit = choice([True, False])
            
	    parameters.setColorRanges(newColorRange)
	    parameters.setFlipBit(newFlipBit)
	    
            mask = self.segmenter.segmentImage(imageData, parameters)
            newFit = self.fitness.findFitness(mask, idealMaskData, parameters)
            
            if newFit < curBestFit:
                curBestColorRange = deepcopy(newColorRange)
		curBestFlipBit = newFlipBit
                curBestFit = newFit
                parameters.setUpperLimit(curBestFit)
                
                #append to list if plotting enabled
                if plot == True:
                    self.fitnessList.append(newFit)
                    self.iterationsList.append(i + 1)
                    
            print "Iteration " + str(i + 1) + ", Fitness: " + str(curBestFit)
        
        parameters.setColorRanges(curBestColorRange)
        parameters.setFlipBit(curBestFlipBit)
        
        if plot == True:
            self.plotSearch()
        
        return parameters
    
    def randColorRange(self):
        # Effects: returns three 2-tuples of valid [0, 1] color range Min-Max's
        colorRangeList = []
        for i in range(6):
            colorRangeList.append(random())

        return (sorted(colorRangeList[0:2]) , sorted(colorRangeList[2:4]), sorted(colorRangeList[4:6]))
    
    def randPointsColorRange(self, imageData):
        # Requires: imageData holds 3-tupled image data in range [0, 1]
        # Effects: returns three 2-tuples of valid [0, 1] color ranges
        #          using randomly sampled points from the image
        p1 = []
	p2 = []
	
	for i in range(3):
	    p1.append(imageData[randint(0, len(imageData))][i])
	    p2.append(imageData[randint(0, len(imageData))][i])	
	
        return (sorted([p1[0], p2[0]]), sorted([p1[1], p2[1]]), sorted([p1[2], p2[2]]))
    
    def plotSearch(self):
        print self.fitnessList
        print self.iterationsList
        pylab.plot(self.iterationsList, self.fitnessList)
        pylab.xlabel('Number of iterations')
        pylab.ylabel('Fitness (lower is better)')
        pylab.title('Fitness vs. Iterations')
        pylab.savefig("plot.png")
        
