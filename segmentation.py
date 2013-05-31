import Image # for image data
from Grammer import Segment # Abstract Base Class

class rgbSegmenter(Segment):
    # RGB Segmenter Class that segments an image
    # based on ranges of RGB parameters
    def __init__(self):
        pass
    
    def segmentImage(self, imageData, parameters, saveMaskImage = False):
        # Requires: -imageData is a RGB (0 - 255) based image data set
        #           -parameters is three 2-tuple numbers between 0 - 255 that
        #            respectively represent (min, max) RGB ranges for foreground selection
        # Effects:  returns a mask-list where 
        #           (0, 0, 0) is background, (255, 255, 255) is foreground
        if (parameters.RGBranges == None):
            print "No RGB range set!"
            exit(1)
        
        RGBranges = parameters.RGBranges
        
        #check for bounds errors
        for tuples in RGBranges:
            if tuples[0] > tuples[1]:
                print "Min > Max in parameter!"
                exit(1)
            
            for number in tuples:
                if not (0 <= number <= 255):
                    print "Parameter not within 0 - 255 range!"
                    exit(1)
        
        mask = [(0, 0, 0)] * len(imageData)
        
        rRange = RGBranges[0]
        gRange = RGBranges[1]
        bRange = RGBranges[2]
        
        isForeground = lambda x: (rRange[0] <= x[0] <= rRange[1] and
                                  gRange[0] <= x[1] <= gRange[1] and
                                  bRange[0] <= x[2] <= bRange[1])
        
        for i in range(len(imageData)):
            if isForeground(imageData[i]):
                mask[i] = (255, 255, 255)
        
        if saveMaskImage == True:
            dataToImage(mask, parameters.imageSize)
        
        return mask
        

def dataToImage(data, imageSize):
    # Requires: -data holds 0-255 rgb tuples
    #           -imageSize is a tuple of (width, height)
    # Effects: saves a linear list of rgb tuples
    #          as an image named "output.png"
    output = Image.new("RGB", imageSize)
    output.putdata(data)
    output.save("output.png", "PNG")
