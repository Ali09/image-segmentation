# Implementations of search subclass genetic search

from Grammer import Search # Abstract Base Class
import RandomSearch # for best range from initial population
from copy import deepcopy # make deep copy for parameters
from random import randint # for randomly selected mutated bit
from random import random # for [0, 1) random values in mutated color bit

class geneticSearch(Search):
    # Genetic Search Class that finds an optimal
    # parameter set by selective mutations
    
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
        # Effects: - Searches the parameter space using selective mutations
        #           to find an optimal solution, returns most optimal parameter found
        #          -plots fitness vs. generation of search if plot set to True
        print "BLAH BLAH, outside hole - should I not take new things if not any better"
        print "Running genetic search"
        
        mutatedPopSize = int(raw_input("Size of subsequent mutated populations: "))
        numGenerations = int(raw_input("Number of mutated generations: "))
        
        # runs random search to find best from initial population
        # note, random search sets initial upper limit 
        print "Running random search for initial population"
        randSearch = RandomSearch.randomSearch(self.segmenter, self.fitness)
        parameters = randSearch.searchImage(imageData, idealMaskData, parameters)
        
        flipBit = parameters.flipBit
        
        newBestColorRange = deepcopy(parameters.colorRanges)
                
        for i in range(numGenerations):
            print "Generation " + str(i + 1)
            
            curBestColorRange = deepcopy(newBestColorRange)
            
            parameters.setColorRanges(curBestColorRange)
            newMask = self.segmenter.segmentImage(imageData, parameters)
            curBestFit = self.fitness.findFitness(newMask, idealMaskData, parameters)
                        
            for j in range(mutatedPopSize):
                newColorRange = self.mutateColorRange(curBestColorRange)
                parameters.setColorRanges(newColorRange)
                newMask = self.segmenter.segmentImage(imageData, parameters)
                newFit = self.fitness.findFitness(newMask, idealMaskData, parameters)
                
                if newFit < curBestFit:
                    curBestFit = newFit
                    newBestColorRange = deepcopy(newColorRange)
                    parameters.setUpperLimit(curBestFit)
                
                print "Gen " + str(i + 1) + " Iter " + str(j + 1) + ", " + str(curBestFit)
            
        
        curBestColorRange = deepcopy(newBestColorRange)
        parameters.setColorRanges(curBestColorRange)
        
        return parameters
            
    def mutateColorRange(self, colorRange):
        # Requires: -colorRange is a list of valid three 2-tupled [0, 1] color ranges
        # Modifies: colorRange
        # Effects: randomly modifies one of the bits in the color range list
        #          and returns the mutated range
        
        # make a deep copy of o.g. coloRange
        newColorRange = deepcopy(colorRange)
        
        # randomly select bit to be mutated
        mutatedBit = [randint(0, 2), randint(0, 1)]
        
        # if bit is min in color range, make sure < max
        if mutatedBit[1] in [0, 2, 4]:
            rand = random()
            while not (rand < newColorRange[mutatedBit[0]][mutatedBit[1] + 1]):
                rand = random()
        
        # if bit is max in color range, make sure > min
        if mutatedBit[1] in [1, 3, 5]:
            rand = random()
            while not (rand > newColorRange[mutatedBit[0]][mutatedBit[1] - 1]):
                rand = random()
        
        newColorRange[mutatedBit[0]][mutatedBit[1]] = rand
        
        return newColorRange