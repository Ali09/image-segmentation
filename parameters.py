class Parameters(object):
    # Parameters class that holds parameters related
    # to image segmentation

    def __init__(self):
        # Modifies: this
        # Effects: init's class
        self.imageSize = None
        self.RGBranges = None
    
    def setImageSize(self, imageSize):
        # Requires: imageSize is 2-tuple of (width, height)
        # Modifies: this
        # Effects: sets the image size being used
        self.imageSize = imageSize
    
    def setRgbRanges(self, RGBranges):
        # Requires: RGBranges is a list of three 2-tuples
        #           -that range from 0-255
        #           -first num  <= second num in tuple
        # Modifies: this           
        # Effects: sets RGB filtering ranges in Parameters
        #          for use with segmentation
        self.RGBranges = RGBranges

