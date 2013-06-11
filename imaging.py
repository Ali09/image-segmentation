# Implementations of image data handling functions

import Image # for image data
import datetime # for output file name
import colorsys # for color space conversion

def dataToImage(data, imageSize, suffix = ""):
    # Requires: -data holds 0-255 rgb tuples
    #           -imageSize is a tuple of (width, height)
    #           -suffix is of type string
    # Effects: saves the given linear list of rgb tuples
    #          as an image named "output-'date'-'time'-'suffix'.png"
    output = Image.new("RGB", imageSize)
    output.putdata(data)
    time = datetime.datetime.now()
    timeString = "output-" + str(time.month) + '.' + str(time.day) + '.' + str(time.year) 
    timeString += '-' + str(time.hour) + '.' + str(time.minute) + suffix + ".png"
    output.save(timeString, "PNG")

def dataToMatrix(imageData, imageSize):
    # Requires: -imageData is a list of size imageSize[0] * imageSize[1]
    #           -imageSize is a 2-tuple of (width, height)
    # Effects: returns a matrix representation of imageData of imageSize
    imageMatrix = []
    
    for i in range(imageSize[1]):
        imageMatrix.append(imageData[imageSize[0] * i : (imageSize[0] * (i + 1))])
    
    return imageMatrix

def matrixToData(matData):
    # Requires: -matData is a rectangular matrix
    # Effects: returns a list of matrix data of size height * width
    dataList = []
    
    for row in range(len(matData)):
        for col in range(len(matData[0])):
            dataList.append(matData[row][col])
    
    return dataList

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