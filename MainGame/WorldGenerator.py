# World Generator using pseudo-random methods, Gaussian Blur and 2D Convolution
# Matrices

# Gaussian Blur Resources:
# https://www.imageeprocessing.com/2014/04/gaussian-filter-without-using-matlab.html


##### NOTE THAT THIS IS NOT THE ONLY CODE THAT IS RESPONSIBLE FOR GENERATING THE RANDOM MAP
##### THERE IS STILL MORE CODE IN THE INITIALIZATION OF THE MINECRAFT GAME CLASS THAT
##### IS RESPONSIBLE FOR GENERATE THE ENTIER WORLD

import random, math
import numpy as np

class WorldGenerator(object):
    def __init__(self, seed, gameDims=(200, 200), sigma=0.85): # seed can be any combination of letter/numbers in any format
        self.seed = seed
        self.sigma = sigma
        self.gameDims = gameDims
        random.seed(self.seed) # setting the same seed
        self.k = 1/(2*math.pi*(sigma**2)) # constant for the 2D Gaussian Kernel based on kernel map formula linked above
        self.convolutionMatrixSize = (3, 3)
        self.convolutionMatrix = self.generateConvolutionMatrix(self.convolutionMatrixSize, self.sigma)
        # self.worldMap = self.generateRandomMap(self.gameDims, self.convolutionMatrixSize)
    
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
    
    def generateRandomMap(self):
        worldMap = np.zeros((self.gameDims[0] + 2, self.gameDims[1] + 2), dtype=float)
        # we will remove the edges of the convolved map later
        
        # generate un-convolved matrix
        for x in range(0, self.gameDims[0] + 2): # need to make orig. world bigger to remove it later
            for y in range(0, self.gameDims[0] + 2):
                worldMap[x, y] = random.randrange(0, 15, 1)
        
        # # convolving matrix
        # newWorldMap = np.copy(worldMap)
        # halfConvSize = self.convolutionMatrixSize[0]//2
        # for x in range(halfConvSize, self.gameDims[0] - halfConvSize):
        #     for y in range(halfConvSize, self.gameDims[1] - halfConvSize):
        #         tempMatrix = np.zeros(self.convolutionMatrixSize, dtype=float) # small location of matrix extracted
        #         for x1 in range(-halfConvSize, halfConvSize + 1):
        #             for y1 in range(-halfConvSize, halfConvSize + 1):
        #                 tempMatrix[x1 + halfConvSize, y1 + halfConvSize] = worldMap[x + x1, y + y1]
        #         newWorldMap[x, y] = round(np.sum(np.multiply(tempMatrix, self.convolutionMatrix)))
        
        # convolving matrix ver.2
        finalWorldMap =  np.zeros(self.gameDims, dtype=int)
        halfConvSize = self.convolutionMatrixSize[0]//2
        for x in range(1, self.gameDims[0] + 2 - 1): # weird math here to remove unecessary edges from map
            for y in range(1, self.gameDims[1] + 2 - 1): # weird math here to remove unecessary edges from map
                tempMatrix = np.zeros(self.convolutionMatrixSize, dtype=float) # small location of matrix extracted
                for x1 in range(-halfConvSize, halfConvSize + 1):
                    for y1 in range(-halfConvSize, halfConvSize + 1):
                        tempMatrix[x1 + halfConvSize, y1 + halfConvSize] = worldMap[x + x1, y + y1]
                finalWorldMap[x - 1, y - 1] = round(np.sum(np.multiply(tempMatrix, self.convolutionMatrix))) - 7 # shift down by seven so that height variation
                # exists underground
        
        # # cut out only the usable newWorldMap
        # finalWorldMap =  np.zeros(self.gameDims, dtype=int)
        # for x in range(1, self.gameDims[0] - 1):
        #     for y in range(1, self.gameDims[1] - 1):
        #         finalWorldMap[x - 1, y - 1] = newWorldMap[x, y]
        print(finalWorldMap)
        return finalWorldMap