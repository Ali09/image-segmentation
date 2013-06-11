# Implementation of blach / white region identifying class, closure

import imaging
from Queue import Queue # queue for flood filling regions

class closure(object):
    # Closure class that identifies distinct
    # black / white regions in an image and attempts
    # to fill black regions to improve fitness
    
    def __init__(self):
        pass
    
    def segmentRegions(self, maskData, parameters):
        # Requires : -maskData is a (0, 0, 0) / (255, 255, 255)
        #             black / white rgb based list data set 
        #            -parameters is of type Parameters
        # Effects : -segments a black / white image into distinct
        #            black / white regions and attempts to fill
        #            smaller black regions for increased fit 
        imageSize = parameters.imageSize
        
        imageMat = imaging.dataToMatrix(maskData, imageSize)
        
        # label matrix with "black"/"white" instead of rgb values for convenience
        for row in range(imageSize[1]):
            for col in range(imageSize[0]):
                if imageMat[row][col] == (0, 0, 0):
                    imageMat[row][col] = "black"
                else:
                    imageMat[row][col] = "white"
        
        #list of distinct white / black regions with the count of pixels in each
        blackRegions = []
        whiteRegions = []
        
        blackCount = 0
        whiteCount = 0
        for row in range(imageSize[1]):
            for col in range(imageSize[0]):
                if imageMat[row][col] == "black":
                    blackCount += 1
                    (count, border) = self.floodFill(imageMat, (col, row), blackCount, parameters)
                    blackRegions.append((count, border))
                elif imageMat[row][col] == "white":
                    whiteCount -= 1
                    (count, border) = self.floodFill(imageMat, (col, row), whiteCount, parameters)
                    whiteRegions.append((count, border))
        dataList = imaging.matrixToData(imageMat)
        
        
        #maxBlackMarked = blackRegions.index(max(blackRegions)) + 1

        # any black that is adjacent to border is background
        # otherwise surrounded by white, foreground
        for i in range(len(dataList)):
            if dataList[i] > 0 and blackRegions[abs(dataList[i]) - 1][1] == False:
                dataList[i] = (255,) * 3
            elif dataList[i] > 0:
                dataList[i] = (0,) * 3
            else:
                dataList[i] = (255,) * 3                

        imaging.dataToImage(dataList, parameters.imageSize, "-region")

        
    def floodFill(self, imageMat, coordinate, marker, parameters):
        # Requires : -imageMat is a data matrix of the image
        #            -coordinate is a 2-tuple of (x,y) coordinates within the matrix
        #            -marker is an integer
        #            -the imageMat at coordinate holds either "black" or "white"
        # Modifies : imageMat
        # Effects : 'flood fills' the image matrix to segment a region that contains
        #            coordinate, marks the region with the number marker
        #            returns the total count of pixels in region; used by segmentRegions
        #            to segment different masked regions
        
        coordinates = Queue()
        
        coordinates.put(coordinate)
        
        x = coordinate[0]
        y = coordinate[1]
        
        color = imageMat[y][x]
        
        imageMat[y][x] = marker
        
        totalCount = 1
        
        validCoord = lambda a, b : (0 <= a < len(imageMat[0]) and
                                    0 <= b < len(imageMat) and
                                    imageMat[b][a] == color)
        
        adjBorder = lambda c, d : (not (0 <= c < len(imageMat[0]) and
                                       0 <= d < len(imageMat)))
        
        BorderAdjacent = False
        
        while coordinates.empty() == False:                     
            coordinate = coordinates.get()
            x = coordinate[0]
            y = coordinate[1]
            
            l = (x - 1, y)
            ld = (x - 1, y + 1)
            d = (x, y + 1)
            dr = (x + 1, y + 1)
            r = (x + 1, y)
            ur = (x + 1, y - 1)
            u = (x, y - 1)
            ul = (x - 1, y - 1)
            
            directions = [l, ld, d, dr, r, ur, u, ul]
            
            for x2, y2 in directions:
                if validCoord(x2, y2):
                    imageMat[y2][x2] = marker
                    coordinates.put((x2, y2))
                    totalCount += 1
                if adjBorder(x2, y2):
                    BorderAdjacent = True
        
        return (totalCount, BorderAdjacent)


'''from parameters import Parameters
import Image

param = Parameters()
image = Image.open("demo/output-6.4.2013-12.58.png")
imageData = list(image.getdata())
param.setImageSize(image.size)
close = closure()
close.segmentRegions(imageData, param)'''
