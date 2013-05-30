import Image # for image data

def absDiff(generatedMaskData, idealMaskData):
    # Requires: both inputs are RGB (0 - 255) based images
    # Effects:  returns # of black/white pixels in generated mask
    #           that differ from ideal mask           
    totalDiff = 0
    for i in range(len(generatedMaskData)):
        totalDiff += abs(generatedMaskData[i][0]/255 - idealMaskData[i][0]/255)
    return totalDiff

def runFitness(maskName, idealMaskName):
    # Effects: runs fitness function as specified
    print "Running fitness segmenter with simple Black-White function"
    generatedMask = Image.open(maskName)
    idealMask = Image.open(idealMaskName)
    generatedMaskData = list(idealMask.getdata())
    idealMaskData = list(generatedMask.getdata())
    print "Number of Differing Pixels:", absDiff(generatedMaskData, idealMaskData)