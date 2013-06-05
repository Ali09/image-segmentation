# Implementation of parameters class

class Parameters(object):
    # Parameters class that holds parameters related
    # to image segmentation

    def __init__(self):
        # Modifies: this
        # Effects: init's class
        self.imageSize = None
        self.colorSpace = None
        self.colorRanges = None
	self.flipBit = False
    
    def setImageSize(self, imageSize):
        # Requires: imageSize is 2-tuple of (width, height)
        # Modifies: this
        # Effects: sets the image size being used
        self.imageSize = imageSize
    
    def setColorSpace(self, colorSpace):
        # Requires: colorSpace is a string
        #           containing either: "RGB", "HSV", or "HLS"
        # Modifies: this
        # Effects: tells parameters which color space is being used
        self.colorSpace = colorSpace
    
    def setColorRanges(self, colorRanges):
        # Requires: RGBranges is a list of three 2-tuples
        #           -that range from 0-1
        #           -first num  <= second num in tuple
        # Modifies: this           
        # Effects: sets color filtering ranges in Parameters
        #          for use with segmentation
        self.colorRanges = colorRanges
    
    def setFlipBit(self, value):
    	# Requires: value is of type bool
    	# Modifies: this
	# Effects: -sets flip bit to value
	#	   -when flip bit is false (default),
	#	    segmenter will segment as normal using rgb parameters 
	#	   -when flip bit is true,
	#           segmenter will invert the segmentation found using rgb parameters
	self.flipBit = value
