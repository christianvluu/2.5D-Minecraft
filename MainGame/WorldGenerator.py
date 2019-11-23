# World Generator using pseudo-random methods, Gaussian Blur and 2D Convolution
# Matrices

# Gaussian Blur Resources:
# https://www.imageeprocessing.com/2014/04/gaussian-filter-without-using-matlab.html

import random, math
import numpy as np

class WorldGenerator(object):
    def __init__(self, worldMap, seed, sigma, gameDims=(24, 24)): # seed can be any combination of letter/numbers in string format
        if (not isinstance(seed, str)):
            raise Exception("Seed not appropriate")
        self.seed = seed
        self.sigma = sigma
        random.seed(self.seed) # setting the same seed
        self.k = 1/(2*math.pi*(sigma**2)) # constant for the 2D Gaussian Kernel
        convolutionMatrixSize = (3, 3)
        self.convolutionMatrix = self.generateConvolutionMatrix(convolutionMatrixSize, self.sigma)
        self.worldMap = self.generateRandomMap(gameDims, convolutionMatrixSize)
    
    def generateConvolutionMatrix(self, matrixDims, sigma):
        yMatrix = np.zeros(matrixDims, dtype=float)
        xMatrix = np.zeros(matrixDims, dtype=float)
        for i in range(0, matrixDims[0]):
            xMatrix[0, i] = -1
            xMatrix[2, i] = 1
            yMatrix[i, 0] = -1
            yMatrix[i, 2] = 1
        convolutionMatrix = np.zeros(matrixDims, dtype=float)
        for i0 in range(0, matrixDims[0]):
            for i1 in range(0, matrixDims[1]):
                x = xMatrix[i0, i1]
                y = yMatrix[i0, i1]
                val = self.k*(math.e**((-((x**2)+(y**2))/(2*(sigma**2)))))
                convolutionMatrix[i0, i1] = val
        print(np.sum(convolutionMatrix))
        print(convolutionMatrix)
        return convolutionMatrix
    
    def generateRandomMap(self, gameDims, convolutionMatrixSize):
        worldMap = np.zeros((gameDims[0] + 2, gameDims[1] + 2), dtype=float)
        # we will remove the edges of the convolved map later
        
        # generate un-convolved matrix
        for x in range(0, gameDims[0] + 2):
            for y in range(0, gameDims[0] + 2):
                worldMap[x, y] = random.randrange(0, 10, 1)
        
        # convolving matrix
        newWorldMap = np.copy(worldMap)
        halfConvSize = convolutionMatrixSize[0]//2
        for x in range(halfConvSize, gameDims[0] - halfConvSize):
            for y in range(halfConvSize, gameDims[1] - halfConvSize):
                tempMatrix = np.zeros(convolutionMatrixSize, dtype=float) # small location of matrix extracted
                for x1 in range(-halfConvSize, halfConvSize + 1):
                    for y1 in range(-halfConvSize, halfConvSize + 1):
                        tempMatrix[x1 + halfConvSize, y1 + halfConvSize] = worldMap[x + x1, y + y1]
                newWorldMap[x, y] = math.floor(np.sum(np.multiply(tempMatrix, self.convolutionMatrix)))
        
        # cut out only the usable newWorldMap
        finalWorldMap =  np.zeros(gameDims, dtype=int)
        for x in range(1, gameDims[0] + 1):
            for y in range(1, gameDims[1] + 1):
                finalWorldMap[x-1, y-1] = newWorldMap[x, y]
        print(newWorldMap)
        print(finalWorldMap)
        return finalWorldMap
    
test = WorldGenerator(0, "casey is dumb!", 0.85)