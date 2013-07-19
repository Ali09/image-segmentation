# Implementations of search subclass genetic search

from Grammer import Search # Abstract Base Class
import RandomSearch # for best range from initial population
from copy import deepcopy # make deep copy for parameters
from random import randint # for randomly selected mutated bit
from random import random # for [0, 1) random values in mutated color bit
import segmentation # to check for segmentation type in mutate function

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
        # Requires: -image and idealMask is an RGB based image
        #           -parameters is of type Parameters
        # Modifies:  parameters
        # Effects: - Searches the parameter space using selective mutations
        #           to find an optimal solution, returns most optimal parameter found
        #          -plots fitness vs. generation of search if plot set to True
        print "Running genetic search"
                
        mutatedPopSize = int(raw_input("Size of mutated populations: "))
        numGenerations = int(raw_input("Number of generations: "))
        
        # runs random search to find best from initial population
        # note, random search sets initial upper limit 
        print "Calling random search for initial population"
        print "Initial population size = Number of Iterations"
        randSearch = RandomSearch.randomSearch(self.segmenter, self.fitness)
        parameters = randSearch.searchImage(imageData, idealMaskData, parameters)
                
        newBestParameters = deepcopy(parameters)
        
        # outter loop, number of generations        
        for i in range(numGenerations):
            print "Generation " + str(i + 1)
            
            curBestParameters = deepcopy(newBestParameters)

            newMask = self.segmenter.segmentImage(imageData, curBestParameters)
            curBestFit = self.fitness.findFitness(newMask, idealMaskData, curBestParameters)
            
            # inner loop, number of pop per generations            
            for j in range(mutatedPopSize):
                
                self.mutateParameters(parameters)
                newMask = self.segmenter.segmentImage(imageData, parameters)
                newFit = self.fitness.findFitness(newMask, idealMaskData, parameters)
                
                if newFit < curBestFit:
                    curBestFit = newFit
                    newBestParameters = deepcopy(parameters)
                    newBestParameters.setUpperLimit(curBestFit)
                    
                parameters = deepcopy(curBestParameters)
                
                print "Gen " + str(i + 1) + " Iter " + str(j + 1) + ", " + str(curBestFit)
            
        parameters = deepcopy(curBestParameters)
        return parameters
        
    def mutateParameters(self, parameters):
        # Requires: parameters is of type Parameters
        # Modifies: parameters
        # Effects: mutates the parameters based on segmenter used
                
        # if color based segmenter, then mutate color range
        if type(self.segmenter) == type(segmentation.colorSegmenter()):
            self.mutateColorRange(parameters.colorRanges)
            
    def mutateColorRange(self, colorRange):
        # Requires: colorRange is a list of valid three 2-tupled [0, 1] color ranges
        # Modifies: colorRange
        # Effects: randomly modifies one of the bits in the colorRange list
        
        # randomly select bit to be mutated
        mutatedBit = [randint(0, 2), randint(0, 1)]
        
        # if bit is min in color range, make sure < max
        if mutatedBit[1] in [0, 2, 4]:
            rand = random()
            while not (rand < colorRange[mutatedBit[0]][mutatedBit[1] + 1]):
                rand = random()
        
        # if bit is max in color range, make sure > min
        if mutatedBit[1] in [1, 3, 5]:
            rand = random()
            while not (rand > colorRange[mutatedBit[0]][mutatedBit[1] - 1]):
                rand = random()
        
        # set specific bit to new random value
        colorRange[mutatedBit[0]][mutatedBit[1]] = rand
        
        return