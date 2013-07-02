# Implementations of search subclass anneal search

from scipy import optimize # for simulated annealing
import numpy # for numpy array, as required by scipy's anneal
from random import randint # for random initial guess
from Grammer import Search # abstract base class
import segmentation # color segmenter, annealing needs this
import RandomSearch # for anneal's initial guess

class annealSearch(Search):
    # Anneal Search Class that uses
    # a pre-written simulated annealing function from scipy
    
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
        # Effects: - Searches the parameter space using simulated annealing
        #           to find an optimal solution, returns most optimal parameter found
        #          -plots fitness vs. generation of search if plot set to True
        
        # runs random search to find best from initial population
        # note, random search sets initial upper limit 
        print "Calling random search for initial random guess"
        randSearch = RandomSearch.randomSearch(self.segmenter, self.fitness)
        parameters = randSearch.searchImage(imageData, idealMaskData, parameters)
        
        parameters.setUpperLimit(float("inf"))
        initialGuess = numpy.array(sum(parameters.colorRanges, []))
                
        # hold references to image data and ideal mask data
        # to conform with scipy's need for a simple fitness function (not multiple arguments) 
        self.imageData = imageData
        self.idealMaskData = idealMaskData
        
        # runs scipy's anneal
        results = optimize.anneal(self.segmentAndFitness, x0 = initialGuess, args=(parameters,), 
                                  schedule='cauchy', full_output=True, dwell=50, 
                                  lower=0.0, upper=1.0, disp=True,
                                  T0 = .005)
                                  
        #dicts = {'args' : (parameters,)}
        #results = optimize.basinhopping(self.segmentAndFitness, x0 = initialGuess, minimizer_kwargs=dicts, 
        #                          niter = 1000)
        
        # prints anneal's final fitness                          
        print "Fitness " + str(results[1])
        
        colorRanges = results[0]
        colorRanges = [colorRanges[0:2], colorRanges[2:4], colorRanges[4:6]]
        parameters.setColorRanges(colorRanges)
        return parameters
        
    def segmentAndFitness(self, colorRangesArray, *parameters):
        # Requires: -colorRangesArray is a six numbered array,
        #            unlike other color ranges used in this program
        #            it is not three 2-tuples, but instead min/max or RGB
        #            in their respective order; this is done to conform with
        #            scipy's need for anneal to take only a list of input arguments
        #           -parameters is of type Parameters
        # Effects: -runs both the specified segmenter and fitness function for
        #           annealSearch, returns fitness of segmenter based on color ranges
        #          -function necessary for scipy's anneal to work
        parameters = parameters[0]

        for i in range(6):
            if not (0 <= colorRangesArray[i] <= 1):
                return float("inf")
        
        for i in [0, 2, 4]:
            if colorRangesArray[i] > colorRangesArray[i + 1]:
                return float("inf")
        
        print colorRangesArray
        colorRanges = [colorRangesArray[0:2], colorRangesArray[2:4], colorRangesArray[4:6]]
        
        
        parameters.setColorRanges(colorRanges)
        maskData = self.segmenter.segmentImage(self.imageData, parameters)
        fit = self.fitness.findFitness(maskData, self.idealMaskData, parameters)
        print fit
        return fit
        