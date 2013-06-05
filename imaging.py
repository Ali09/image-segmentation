# Implementations of image data handling functions

import Image # for image data
import datetime # for output file name
import colorsys # for color space conversion

def dataToImage(data, imageSize):
    # Requires: -data holds 0-255 rgb tuples
    #           -imageSize is a tuple of (width, height)
    # Effects: saves the given linear list of rgb tuples
    #          as an image named "output-'date'-'time'.png"
    output = Image.new("RGB", imageSize)
    output.putdata(data)
    time = datetime.datetime.now()
    timeString = "output-" + str(time.month) + '.' + str(time.day) + '.' + str(time.year) 
    timeString += '-' + str(time.hour) + '.' + str(time.minute) + ".png"
    output.save(timeString, "PNG")

def colorSpaceConvert(imageData, colorSpace):
    # Requires: -imageData holds three-tupled RGB 0-255 based data
    #           -parameters is of type Parameters
    # Modifies: imageData
    # Effects: converts an RGB based image data set holding 0-255 values to either
    #          the RGB, HSV, or HLS based color space, holding 0-1 values
    if colorSpace.lower() == "rgb":
        func = lambda x: (x[0] / 255.0, x[1] / 255.0, x[2] / 255.0)
    elif colorSpace.lower() == "hsv":
        func = lambda x: colorsys.rgb_to_hsv(x[0] / 255.0, x[1] / 255.0, x[2] / 255.0)
    elif colorSpace.lower() == "hls":
        func = lambda x: colorsys.rgb_to_hls(x[0] / 255.0, x[1] / 255.0, x[2] / 255.0)
    else:
        print "Invalid color scheme specified"
        exit(1)
    
    for i in range(len(imageData)):
        imageData[i] = func(imageData[i])
    
    return imageData
        