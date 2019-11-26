import pygame, time
import numpy as np
import json
import os
# Pygame usage from http://blog.lukasperaza.com/getting-started-with-pygame/
# and Official Documentation https://www.pygame.org/docs/ 
from pygametemplate import *
from WorldGenerator import *
from BlockObject import *
from PlayerObject import *
from MouseCursorObject import *
from ButtonObject import *

class Minecraft(PygameGame):
    blockTex = None
    blockLib = None
    blockXWidth = None

    def __init__(self, seed, sigma):
        self.height = 550
        self.width = 550
        super().__init__(title="Minecraft", width=self.width, height=self.height)
        self.locationMap = np.full((200, 200, 200), BlockObject("empty"))
        # use self.location[x,y,z] to refer to a point
        self.gameDims = (200, 200, 200)
        self.margin = 25
        self.renderDist = 5  # blocks from user
        Minecraft.blockXWidth = (self.width - 2*self.margin)//(2*self.renderDist)
        self.isPlaying = False
        # background from http://www.tassal.com.au/sustainability/blue-background-png/
        self.background = pygame.image.load("background.png")
        self.gameBlockGroup = pygame.sprite.Group()
        self.initBlockLibrary()  # group textures
        self.perspective = 1 # default perspective, with origin up top
        self.seed = seed
        self.sigma = sigma
        self.player = Player(Minecraft.blockXWidth, (self.gameDims[0]//2, self.gameDims[1]//2, self.gameDims[2]//2 + 1)) # player pos is above the block player is standing on
        self.startScreen() # display the startscreen
    
    def startGameRandomWorld(self):
        self.createRandomWorld(self.locationMap, self.gameBlockGroup, self.gameDims, self.seed, self.sigma)
        self.player.move(0, 0, 0, self.locationMap) # init the player drop down to world
    
    def startGameFlatlandWorld(self):
        self.createFlatWorld(self.locationMap, self.gameBlockGroup, self.gameDims)
        self.player.move(0, 0, 0, self.locationMap) # init the player drop down to world

    def startScreen(self):
        self.startScreenElements = pygame.sprite.Group()
        self.buttonCollisions = []
        self.mouseCursor = MouseCursor((-1, -1)) # init off the screen
        # background for intro taken from: https://i.ytimg.com/vi/s6gS3RZ_kXw/maxresdefault.jpg
        introBackground = pygame.transform.scale(pygame.image.load("minecraftintro.png"), (self.width, self.height))
        self.screen.blit(introBackground, (0,0))
        buttonDims = (120, 30)
        randomWorldPos = (self.width/2 - 130, self.height/2)
        flatlandWorldPos = (self.width/2 + 10, self.height/2)
        self.randomWorldButton = Button("randomworldbutton.png", buttonDims, randomWorldPos)
        self.startScreenElements.add(self.randomWorldButton)
        self.flatlandWorldButton = Button("flatlandworldbutton.png", buttonDims, flatlandWorldPos)
        self.startScreenElements.add(self.flatlandWorldButton)
        self.startScreenElements.draw(self.screen)
        if (self.isPlaying):
            self.startGame() # start the game
    
    def clickButton(self, x, y):
        self.buttonCollisions = pygame.sprite.spritecollide(self.mouseCursor, self.startScreenElements, False, pygame.sprite.collide_rect_ratio(1))
        for collision in self.buttonCollisions:
            if (collision == self.randomWorldButton):
                self.isPlaying = True
                self.startGameRandomWorld()
            elif (collision == self.flatlandWorldButton):
                self.isPlaying = True
                self.startGameFlatlandWorld()

    def initBlockLibrary(self):
        scaleToDims = (Minecraft.blockXWidth, Minecraft.blockXWidth)
        Minecraft.blockLib = {
        # textures purchased from
        # https://www.yandidesigns.com/2017/07/how-to-make-flat-isometric-block-like-minecraft-affinity-designer.html
            "dirt":
                Minecraft.scale(pygame.image.load("isotex/dirt.png"), scaleToDims),
            "interiorStone":
                Minecraft.scale(pygame.image.load("isotex/interiorstone.png"), scaleToDims),
            "grassDirt":
                Minecraft.scale(pygame.image.load("isotex/grassdirt.png"), scaleToDims),
            "grass":
                Minecraft.scale(pygame.image.load("isotex/grass.png"), scaleToDims),
            "snow":
                Minecraft.scale(pygame.image.load("isotex/snow.png"), scaleToDims),
            "sand":
                Minecraft.scale(pygame.image.load("isotex/sand.png"), scaleToDims),
            "stone":
                Minecraft.scale(pygame.image.load("isotex/stone.png"), scaleToDims),
            "sandStone":
                Minecraft.scale(pygame.image.load("isotex/sandstone.png"), scaleToDims),
            "stoneDirt":
                Minecraft.scale(pygame.image.load("isotex/stonedirt.png"), scaleToDims),
            "stoneSnow":
                Minecraft.scale(pygame.image.load("isotex/stonesnow.png"), scaleToDims),
            "dirtSand":
                Minecraft.scale(pygame.image.load("isotex/dirtsand.png"), scaleToDims),
            "dirtRock":
                Minecraft.scale(pygame.image.load("isotex/dirtrock.png"), scaleToDims),
            "grassStone":
                Minecraft.scale(pygame.image.load("isotex/grassstone.png"), scaleToDims),
            "empty": "NOTHING"
        }
    
    @staticmethod
    def scale(surf, scaleToDims):
        # scales surface to correct dimensions for drawing
        newSurf = pygame.transform.scale(surf, scaleToDims)
        return newSurf

    def createRandomWorld(self, locationMap, gameBlockGroup, gameDims, seed, sigma):
        worldGen = WorldGenerator(seed, (gameDims[0], gameDims[1]), sigma) # only xDim and yDim needed
        heightMap = worldGen.generateRandomMap()
        xSize = gameDims[0]
        ySize = gameDims[1]
        zSize = gameDims[2]
        for x in range(0, xSize):
            for y in range(0, ySize):
                newBlock = BlockObject("grassDirt")
                z = heightMap[x, y] + gameDims[2]//2 # shifting the zero coordinate up to the center of the map
                locationMap[x, y, z] = newBlock
                gameBlockGroup.add(newBlock)
                for lowerZ in range(z - 4, z):
                    newBlock = BlockObject("dirt")
                    locationMap[x, y, lowerZ] = newBlock
                    gameBlockGroup.add(newBlock)
                for lowerZ in range(0, z - 4):
                    newBlock = BlockObject("stone")
                    locationMap[x, y, lowerZ] = newBlock
                    gameBlockGroup.add(newBlock)

    def createFlatWorld(self, locationMap, gameBlockGroup, gameDims = (200, 200, 200)):
        xSize = gameDims[0]
        ySize = gameDims[1]
        zSize = gameDims[2]
        self.screen.blit(self.background, (0, 0))
        # world center is at xSize//2, ySize//2, zSize//2
        dirtThickness = 2  # goes from center down
        stoneThickness = 3
        for x in range(0, xSize):
            for y in range(0, ySize):
                newBlock = BlockObject("grassDirt")
                locationMap[x, y, zSize//2] = newBlock
                gameBlockGroup.add(newBlock)
                for z in range(zSize//2 - dirtThickness, zSize//2):
                    newBlock = BlockObject("dirt")
                    locationMap[x, y, z] = newBlock
                    gameBlockGroup.add(newBlock)
                for z in range(zSize//2 - dirtThickness - stoneThickness, zSize//2 - dirtThickness):
                    newBlock = BlockObject("sand")
                    locationMap[x, y, z] = newBlock
                    gameBlockGroup.add(newBlock)
        
        # blocks created for orientation at start
        for x in range(xSize//2 - 2, xSize//2 + 3, 2):
            for y in range(ySize//2 - 2, xSize//2 + 3, 2):
                self.gameBlockGroup.remove(BlockObject("grassDirt"))
                centerBlock = BlockObject("stone")  # init at center of map
                self.locationMap[x, y, 100] = centerBlock
                self.gameBlockGroup.add(centerBlock)

    def drawWorld(self, screen, playerPos, perspective): # perspective is either 1 (default), 2, 3, 4 (rotating map from bird-eye view clockwise)
        self.screen.blit(self.background, (0, 0))
        posX = playerPos[0]
        posY = playerPos[1]
        posZ = playerPos[2] - 1  # player pos is above the block player is standing on so need to -1 to draw
        if (perspective == 1):
            for x in range(posX - self.renderDist, posX + self.renderDist + 1):
                for y in range(posY - self.renderDist, posY + self.renderDist + 1):
                    for z in range(posZ - self.renderDist, posZ + self.renderDist + 1):
                        if (x <= posX and y <= posY):
                            self.player.draw(screen, self.player.surfPlusY, self.width, self.height, Minecraft.blockXWidth)
                        self.drawBlock(screen, self.locationMap[x, y, z], (x, y, z),
                            playerPos, perspective)
        elif (perspective == 2):
            for x in range(posX - self.renderDist, posX + self.renderDist + 1):
                for y in range(posY + self.renderDist, posY - self.renderDist - 1, -1):
                    for z in range(posZ - self.renderDist, posZ + self.renderDist):
                        if (x <= posX and y >= posY):
                            self.player.draw(screen, self.player.surfPlusY, self.width, self.height, Minecraft.blockXWidth)
                        self.drawBlock(screen, self.locationMap[x, y, z], (x, y, z),
                            playerPos, perspective)
    
    def drawBlock(self, screen, block, centerPos, playerPos, perspective):
        posX = playerPos[0]
        posY = playerPos[1]
        posZ = playerPos[2] - 1  # player pos is above the block player is standing on so need to -1 to draw
        x = centerPos[0]
        y = centerPos[1]
        z = centerPos[2]
        if (block.name == "empty"):
            return 0
        blockSurface = Minecraft.blockLib[block.name]
        #drawX = ((x - posX) - (y - posY))*Minecraft.blockXWidth/2 + self.width/2 + self.margin - Minecraft.blockXWidth
        if (perspective == 1): # default perspective, with origin at center top
            # Isometric drawing VERY HEAVILY adapted from http://clintbellanger.net/articles/isometric_math/
            drawX = ((x - posX) - (y - posY))*Minecraft.blockXWidth/2 + self.width/2 + Minecraft.blockXWidth/2 - Minecraft.blockXWidth
            drawY = ((x - posX) + (y - posY))*Minecraft.blockXWidth/(2*2) + self.height/2 - Minecraft.blockXWidth/(2*2) - (z - posZ)*Minecraft.blockXWidth/2
        elif (perspective == 2): # rotated map 90 degrees top down view
            drawX = ((posX - x) + (posY - y))*Minecraft.blockXWidth/2 + self.width/2 + Minecraft.blockXWidth/2 - Minecraft.blockXWidth
            drawY = ((x - posX) + (posY -y))*Minecraft.blockXWidth/(2*2) + self.height/2 - Minecraft.blockXWidth/(2*2) - (z - posZ)*Minecraft.blockXWidth/2
        self.screen.blit(blockSurface, (drawX, drawY))
        if (posX == x and posY == y): #this is the column of blocks player is standing on
            darkBlockSurface = blockSurface.copy()
# method of darkening images from here https://www.reddit.com/r/pygame/comments/4b8mnz/is_it_possible_to_make_an_image_darker/
            dark = pygame.Surface(blockSurface.get_size()).convert_alpha()
            dark.fill((0,0,0, 255//2))
            darkBlockSurface.blit(dark, (0,0))
            self.screen.blit(darkBlockSurface, (drawX, drawY))
        pygame.draw.line(screen, (255, 255, 255), (self.width/2, 0), (self.width/2, self.height))
        pygame.draw.line(screen, (255, 255, 255), (0, self.height/2), (self.width, self.height/2))

# copied and adapted from: https://python-decompiler.com/article/2010-09/how-to-write-a-multidimensional-array-to-a-text-file
    def saveWorld(self):
        newArray = np.full((200, 200, 200), -1)
        for x in range(0, self.gameDims[0]):
            for y in range(0, self.gameDims[1]):
                for z in range(0, self.gameDims[2]):
                    if (self.locationMap[x, y, z].name == "empty"):
                        newArray[x, y, z] = 0
                    elif (self.locationMap[x, y, z].name == "dirt"):
                        newArray[x, y, z] = 1
                    elif (self.locationMap[x, y, z].name == "grassDirt"):
                        newArray[x, y, z] = 2
                    elif (self.locationMap[x, y, z].name == "stone"):
                        newArray[x, y, z] = 3
                    elif (self.locationMap[x, y,z].name == "sand"):
                        newArray[x, y, z] = 4
                    # for key, value in Minecraft.blockLib:
                    #     if (key == self.locationMap[x, y, z].name):
                    #         nameArray[x, y, z] = 
        
        outfile = open("test.txt", "w")
            # I'm writing a header here just for the sake of readability
            # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write("# World shape: {0}\n".format(newArray.shape))

        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for data_slice in newArray:

            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 7 characters in width
            # with 2 decimal places.  
            np.savetxt(outfile, data_slice, fmt="%d")

            # Writing out a break to indicate different slices...
            outfile.write('# New slice\n')

# copied and adapted from: https://python-decompiler.com/article/2010-09/how-to-write-a-multidimensional-array-to-a-text-file
    def openWorld(self, filePath):
        infile = open(filePath, "r")
        newArray = np.loadtxt(filePath).reshape(self.gameDims)
        for x in range(0, self.gameDims[0]):
            for y in range(0, self.gameDims[1]):
                for z in range(0, self.gameDims[2]):
                    if (newArray[x, y, z] == "empty"):
                        self.locationMap[x, y, z] = BlockObject("empty")
                    elif (newArray[x, y, z] == "dirt"):
                        self.locationMap[x, y, z] = BlockObject("dirt")
                    elif (newArray[x, y, z] == "grassDirt"):
                        self.locationMap[x, y, z] = BlockObject("grassDirt")
                    elif (newArray[x, y, z] == "stone"):
                        self.locationMap[x, y, z] = BlockObject("stone")
                    elif (newArray[x, y, z] == "sand"):
                        self.locationMap[x, y, z] = BlockObject("sand")



    def mousePressed(self, x, y):
        if (not self.isPlaying):
            self.mouseCursor.rect.x = x
            self.mouseCursor.rect.y = y
            self.clickButton(x, y)

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDragged(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if (self.isPlaying):
            if (keyCode == pygame.K_w and modifier == 0): # 1 is holding shift down
                if (self.perspective == 1):
                    self.player.move(-1, 0, 0, self.locationMap)
                elif (self.perspective == 2):
                    self.player.move(0, 1, 0, self.locationMap)
            elif (keyCode == pygame.K_s and modifier == 0):
                if (self.perspective == 1):
                    self.player.move(1, 0, 0, self.locationMap)
                elif (self.perspective == 2):
                    self.player.move(0, -1, 0, self.locationMap)
            elif (keyCode == pygame.K_d and modifier == 0):
                if (self.perspective == 1):
                    self.player.move(0, -1, 0, self.locationMap)
                elif (self.perspective == 2):
                    self.player.move(-1, 0, 0, self.locationMap)
            elif (keyCode == pygame.K_a and modifier == 0):
                if (self.perspective == 1):
                    self.player.move(0, 1, 0, self.locationMap)
                elif (self.perspective == 2):
                    self.player.move(+1, 0, 0, self.locationMap)
            elif (keyCode == pygame.K_e and modifier == 0):  # move up into sky
                self.player.move(0, 0, 1, self.locationMap)
            elif (keyCode == pygame.K_q and modifier == 0):  # move down into ground
                self.player.move(0, 0, -1, self.locationMap)
            
            elif (keyCode == pygame.K_UP and modifier == 1): # 1 is left shift
                if (self.perspective == 1):
                    self.player.direction = "-x"
                elif (self.perspective == 2):
                    self.player.direction = "+y"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 0) # 0 is zOffset
            elif (keyCode == pygame.K_DOWN and modifier == 1):
                if (self.perspective == 1):
                    self.player.direction = "+x"
                elif (self.perspective == 2):
                    self.player.direction = "-y"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 0)
            elif (keyCode == pygame.K_RIGHT and modifier == 1):
                if (self.perspective == 1):
                    self.player.direction = "-y"
                elif (self.perspective == 2):
                    self.player.direction = "-x"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 0)
            elif (keyCode == pygame.K_LEFT and modifier == 1):
                if (self.perspective == 1):
                    self.player.direction = "+y"
                elif (self.perspective == 2):
                    self.player.direction = "+x"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 0)
            
            elif (keyCode == pygame.K_UP and modifier == 256): # 256 is left alt
                if (self.perspective == 1):
                    self.player.direction = "-x"
                elif (self.perspective == 2):
                    self.player.direction = "+y"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 1)
            elif (keyCode == pygame.K_DOWN and modifier == 256):
                if (self.perspective == 1):
                    self.player.direction = "+x"
                elif (self.perspective == 2):
                    self.player.direction = "-y"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 1)
            elif (keyCode == pygame.K_RIGHT and modifier == 256):
                if (self.perspective == 1):
                    self.player.direction = "-y"
                elif (self.perspective == 2):
                    self.player.direction = "-x"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 1)
            elif (keyCode == pygame.K_LEFT and modifier == 256):
                if (self.perspective == 1):
                    self.player.direction = "+y"
                elif (self.perspective == 2):
                    self.player.direction = "+x"
                self.player.destroyBlock(self.locationMap, self.gameBlockGroup, 1)
            
            # use arrow keys to place block, if NOT holding left control, place block at feet level
            elif (keyCode == pygame.K_UP and modifier == 0): # 0 is no modifier
                if (self.perspective == 1):
                    self.player.direction = "-x"
                elif (self.perspective == 2):
                    self.player.direction = "+y"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 0)
            elif (keyCode == pygame.K_DOWN and modifier == 0):
                if (self.perspective == 1):
                    self.player.direction = "+x"
                elif (self.perspective == 2):
                    self.player.direction = "-y"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 0)
            elif (keyCode == pygame.K_RIGHT and modifier == 0):
                if (self.perspective == 1):
                    self.player.direction = "-y"
                elif (self.perspective == 2):
                    self.player.direction = "-x"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 0)
            elif (keyCode == pygame.K_LEFT and modifier == 0):
                if (self.perspective == 1):
                    self.player.direction = "+y"
                elif (self.perspective == 2):
                    self.player.direction = "+x"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 0)
            
            # use arrow keys to place block, if holding left control also, place block at head level
            elif (keyCode == pygame.K_UP and modifier == 64): # 64 is no left control
                if (self.perspective == 1):
                    self.player.direction = "-x"
                elif (self.perspective == 2):
                    self.player.direction = "+y"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 1)
            elif (keyCode == pygame.K_DOWN and modifier == 64):
                if (self.perspective == 1):
                    self.player.direction = "+x"
                elif (self.perspective == 2):
                    self.player.direction = "-y"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 1)
            elif (keyCode == pygame.K_RIGHT and modifier == 64):
                if (self.perspective == 1):
                    self.player.direction = "-y"
                elif (self.perspective == 2):
                    self.player.direction = "-x"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 1)
            elif (keyCode == pygame.K_LEFT and modifier == 64):
                if (self.perspective == 1):
                    self.player.direction = "+y"
                elif (self.perspective == 2):
                    self.player.direction = "+x"
                self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup, 1)
            
            elif (keyCode == pygame.K_r and modifier == 64): # reset game by CTRL + r
                self.__init__(self.seed, self.sigma)
            
            elif (keyCode == pygame.K_s and modifier == 64): # save game by CTRL + s
                self.saveWorld()
            
            elif (keyCode == pygame.K_1):
                self.perspective = 1
            elif (keyCode == pygame.K_2):
                self.perspective = 2

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        if (self.isPlaying):
            self.drawWorld(screen, self.player.getPos(), self.perspective)
    
game = Minecraft(123, 1) # input is seed and sigma
        
game.run()