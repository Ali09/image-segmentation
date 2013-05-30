import Image # for image data

def dataToImage(data, imageSize):
    # Requires: -data holds 0-255 rgb tuples
    #           -imageSize is a tuple of (width, height)
    # Effects: saves a linear list of rgb tuples
    #          as an image named "output.png"
    output = Image.new("RGB", imageSize)
    output.putdata(data)
    output.save("output.png", "PNG")

def rgbSegmenter(imageData, parameters):
    # Requires: -imageData is a RGB (0 - 255) based image data set
    #           -parameters is three 2-tuple numbers between 0 - 255 that
    #            respectively represent (min, max) RGB ranges for foreground selection
    # Effects:  returns a mask-list where 
    #           (0, 0, 0) is background, (255, 255, 255) is foreground
    
    rRange = (parameters[0], parameters[1])
    gRange = (parameters[2], parameters[3])
    bRange = (parameters[4], parameters[5])
    
    #check for bounds errors
    for ranges in parameters:
        if not (0 <= ranges <= 255):
               print "Parameter not within 0 - 255 range!"
               exit(1)
               
    for tuples in (rRange, gRange, bRange):
        if tuples[0] > tuples[1]:
            print "Min > Max in parameter!"
            exit(1)
    
    mask = [(0, 0, 0)] * len(imageData)
    
    isForeground = lambda x: (rRange[0] <= x[0] <= rRange[1] and
                              gRange[0] <= x[1] <= gRange[1] and
                              bRange[0] <= x[2] <= bRange[1])
    
    for i in range(len(imageData)):
        if isForeground(imageData[i]):
            mask[i] = (255, 255, 255)
    
    return mask

def runSegmenter(imageName, rgbLimits):
    # Effects: runs image segmenter as specified
    print "Running image segmenter with simple rgb segmentation"
    image = Image.open(imageName)
    imageData = list(image.getdata())
    mask = rgbSegmenter(imageData, rgbLimits)
    dataToImage(mask, image.size)
