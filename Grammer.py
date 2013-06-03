# Abstract Base Classes for Image Segmentation Project

class Segment(object):
    # Segment class that segments an image's data as specified
    
    def segmentImage(self, imageData, parameters, saveMaskImage = False):
        # Requires: -imageData is a list of three-tupled RGB (0 - 255) data
        #            i.e. data from PIL's list(image.getdata())
        #           -parameters is of type Parameters
        # Effects: segment's image with given parameters
        #          -returns a list of three-tupled RGB data where
        #           (0, 0, 0) (Black) is background and 
        #           (256, 256, 256) (White) is foreground
        #          -saves the output mask as an image 'output.png' if saveMaskImage set to True
        raise NotImplementedError
   
class Fitness(object):
    # Fitness function class that finds an objective fitness metric of a particular image mask
    
    def findFitness(self, generatedMaskData, idealMaskData, parameters):
        # Requires: -generatedMaskData and idealMaskData are
        #            lists of three-tupled RGB (0 - 255) data
        #            i.e. data from Segmenter's segmentImage and PIL's list(image.getdata())
        #           -parameters is of type Parameters
        # Effects: finds an objective fitness of generated mask data
        #          relative to an ideal mask as specified with given parameters
        raise NotImplementedError

class Search(object):
    # Search - 'learning loop' - class that utilizes segmentation and fitness
    # tools to find an optimal mask for an image
    
    def __init__(self, segmenter, fitness):
        # Requires: -segmenter is of type Segment
        #           -fitness is of type Fitness
        # Modifies: this
        # Effects: tells Search which segmenter(s) and fitness function(s) to use
        raise NotImplementedError
    
    def searchImage(self, imageData, idealMaskData, parameters, plot = False):
        # Requires: -imageData and idealMaskData are
        #            lists of three-tupled RGB (0 - 255) data
        #            i.e. data from PIL's list(image.getdata())
        #           -parameters is of type Parameters
        # Modifies: parameters
        # Effects: -searches the image's parameter space as specified
        #           attempting to minimize the objective fitness cost
        #          -returns parameters that give optimal cost
        #          -plots fitness vs. extent of search if plot set to True
        raise NotImplementedError
        

