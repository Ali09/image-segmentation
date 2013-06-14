from parameters import Parameters
import Image
from sys import argv
from imaging import colorSpaceConvert
import segmentation
import closure

def countRegions():
    # Requires: -the first command line argument is the name of the
    #            image to be segmented
    #           -the second command line argument is the color space being
    #            used, either RGB, HSV, or HLS
    # Effects: -calls closure with count foreground argument on, returns
    #           count of distinct foreground objects
    
    colorSpace = argv[2].lower()
    
    if not (colorSpace in ["rgb", "hsv", "hls"]):
        print "Second argument not one of RGB, HSV, or HLS"
        exit(1)
    
    try:
        image = Image.open(argv[1])
        imageData = colorSpaceConvert(list(image.getdata()), argv[2].lower())
    except:
        print "Invalid or no image name given"
        exit(1)
        
    if colorSpace == "rgb":
        redMinMax = raw_input("Red min-max, between 0 and 255: ")
        greenMinMax = raw_input("Green min-max, between 0 and 255: ")
        blueMinMax = raw_input("Blue min-max, between 0 and 255: ")
        redMinMax = [float(x) / 255.0 for x in redMinMax.split()]
        greenMinMax = [float(x) / 255.0 for x in greenMinMax.split()]
        blueMinMax = [float(x) / 255.0 for x in blueMinMax.split()]
        colorRanges = [redMinMax, greenMinMax, blueMinMax]
    elif colorSpace == "hsv":
        hueMinMax = raw_input("Hue min-max, between 0 and 360: ")
        satMinMax = raw_input("Saturation min-max, between 0 and 100: ")
        valMinMax = raw_input("Value min-max, between 0 and 100: ")
        hueMinMax = [float(x) / 360.0 for x in hueMinMax.split()]
        satMinMax = [float(x) / 100.0 for x in satMinMax.split()]
        valMinMax = [float(x) / 100.0 for x in valMinMax.split()]
        colorRanges = [hueMinMax, satMinMax, valMinMax]
    else:
        hueMinMax = raw_input("Hue min-max, between 0 and 360: ")
        lightMinMax = raw_input("Lightness min-max, between 0 and 100: ")
        satMinMax = raw_input("Saturation min-max, between 0 and 100: ")
        hueMinMax = [float(x) / 360.0 for x in hueMinMax.split()]
        lightMinMax = [float(x) / 100.0 for x in lightMinMax.split()]
        satMinMax = [float(x) / 100.0 for x in satMinMax.split()]
        colorRanges = [hueMinMax, lightMinMax, satMinMax]
    
    param = Parameters()
    param.setImageSize(image.size)
    param.setColorRanges(colorRanges)
    
    seg = segmentation.colorSegmenter()
    mask = seg.segmentImage(imageData, param, True)
    
    close = closure.closure()
    close.segmentRegions(mask, param, 0, True, False)

countRegions()
