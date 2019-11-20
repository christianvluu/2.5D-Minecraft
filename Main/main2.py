import pygame, time
import numpy as np
# Pygame usage from http://blog.lukasperaza.com/getting-started-with-pygame/
# and Official Documentation https://www.pygame.org/docs/ 
from pygametemplate import *

class BlockObject(pygame.sprite.Sprite):
    def __init__(self, name, gameCoords=(-1, -1, -1)): # -1 is empty block
        super().__init__()
        self.name = name  # string - use keys of Miencraft.blockLib
        self.gameX = gameCoords[0]  # int
        self.gameY = gameCoords[1]
        self.gameZ = gameCoords[2]


class Player(pygame.sprite.Sprite):
    def __init__(self, gameCoords=(100, 100, 100)):
        super().__init__()
        self.gameX = gameCoords[0]  # integer
        self.gameY = gameCoords[1]
        self.gameZ = gameCoords[2]
        self.direction = "y"  # facing down to bottom left at first
        # self.surfDownLeft = pygame.image.load("playerdownleft.png")
        # self.surfDownRight = pygame.image.load("playerdownright.png")
        # self.surfUpLeft = pygame.image.load("playerupleft.png")
        # self.surfUpRight = pygame.image.load("playerupright.png")
    
    def move(self, dx, dy, dz, locationMap):
        self.gameX += dx
        self.gameY += dy
        self.gameZ += dz
        # keep track of where the player is facing (helpful for placing and
        # destroying blocks) Also useful for movement also
        if (dy > 0):
            self.direction = "y"
        elif (dy < 0):
            self.direction = "-y"
        elif (dx > 0):
            self.direction = "x"
        elif (dx < 0):
            self.direction = "-x"
        # direction dz doesn't matter
        print("player pos: ", self.gameX, self.gameY, self.gameZ, self.direction)
        # should implement isLegalMove into move here...
        # probably should do bounds checking here also
    
    def getPos(self):
        return (self.gameX, self.gameY, self.gameZ)
    
    def placeBlock(self, block, locationMap):
        pass  #place down block in front of player


class Minecraft(PygameGame):
    blockTex = None
    blockLib = None

    def __init__(self):
        super().__init__(title="Minecraft")
        self.locationMap = np.full((200, 200, 200), BlockObject("empty"))
        # use self.location[x,y,z] to refer to a point
        self.gameDims = (200, 200, 200)
        self.margin = 25
        self.renderDist = 5  # blocks from user
        self.blockXWidth = (self.width - 2*self.margin)//(2*self.renderDist)
        self.background = pygame.image.load("background.png")
        self.screen.blit(self.background, (0, 0))
        self.gameBlockGroup = pygame.sprite.Group()
        self.initBlockLibrary()  # group textures
        self.createFlatWorld(
            xSize=self.gameDims[0],
            ySize=self.gameDims[1],
            zSize=self.gameDims[2])
        self.player = Player((self.gameDims[0]//2, self.gameDims[1]//2, self.gameDims[2]//2))

    @staticmethod
    def initBlockTexture():
        # DIRT, GRASSDIRT, COBBLESTONE, WOOD, IRON
        # sid = side (short name)
        Minecraft.blockTex = {
            "dirtTop": pygame.image.load("textures/dirt.png").convert(),
            "dirtSidL": pygame.image.load("textures/dirt.png").convert(),
            "dirtSidR": pygame.image.load("textures/dirt.png").convert(),
            "stonTop": pygame.image.load("textures/stone.png").convert(),
            "stonSidL": pygame.image.load("textures/stone.png").convert(),
            "stonSidR": pygame.image.load("textures/stone.png").convert(),
            "bricTop": pygame.image.load("textures/brick.png").convert(),
            "bricSidL": pygame.image.load("textures/brick.png").convert(),
            "bricSidR": pygame.image.load("textures/brick.png").convert(),
            "pumpTop":
                pygame.image.load("textures/pumpkin_top.png").convert(),
            "pumpSidL":
                pygame.image.load("textures/pumpkin_side.png").convert(),
            "pumpSidR":
                pygame.image.load("textures/pumpkin_side.png").convert(),
            "grasTop": pygame.image.load("textures/grass_top.png").convert(),
            "grasSidL": pygame.image.load("textures/grass_side.png").convert(),
            "grasSidR": pygame.image.load("textures/grass_side.png").convert()}
    
    def initBlockLibrary(self):
        Minecraft.blockLib = {
        # textures purchased from
        # https://www.yandidesigns.com/2017/07/how-to-make-flat-isometric-block-like-minecraft-affinity-designer.html
            "dirt":
                self.scale(pygame.image.load("isotex/dirt.png")),
            "interiorStone":
                self.scale(pygame.image.load("isotex/interiorstone.png")),
            "grassDirt":
                self.scale(pygame.image.load("isotex/grassdirt.png")),
            "grass":
                self.scale(pygame.image.load("isotex/grass.png")),
            "snow":
                self.scale(pygame.image.load("isotex/snow.png")),
            "sand":
                self.scale(pygame.image.load("isotex/sand.png")),
            "stone":
                self.scale(pygame.image.load("isotex/stone.png")),
            "sandStone":
                self.scale(pygame.image.load("isotex/sandstone.png")),
            "stoneDirt":
                self.scale(pygame.image.load("isotex/stonedirt.png")),
            "stoneSnow":
                self.scale(pygame.image.load("isotex/stonesnow.png")),
            "dirtSand":
                self.scale(pygame.image.load("isotex/dirtsand.png")),
            "dirtRock":
                self.scale(pygame.image.load("isotex/dirtrock.png")),
            "grassStone":
                self.scale(pygame.image.load("isotex/grassstone.png"))
        }
    
    def scale(self, surf):
        # scales surface to correct dimensions for drawing
        newDims = (self.blockXWidth, self.blockXWidth)  # for resizing image
        newSurf = pygame.transform.scale(surf, newDims)
        return newSurf

    def createFlatWorld(self, xSize=200, ySize=200, zSize=200):
        self.screen.blit(self.background, (0, 0))
        # world center is at xSize//2, ySize//2, zSize//2
        dirtThickness = 2  # goes from center down
        stoneThickness = 3
        for x in range(0, xSize):
            for y in range(0, ySize):
                newBlock = BlockObject("grassDirt", (x, y, zSize//2))
                self.locationMap[x, y, zSize//2] = newBlock
                self.gameBlockGroup.add(newBlock)
                for z in range(zSize//2 - dirtThickness, zSize//2):
                    newBlock = BlockObject("dirt", (x, y, z))
                    self.locationMap[x, y, z] = newBlock
                    self.gameBlockGroup.add(newBlock)
                for z in range(zSize//2 - dirtThickness - stoneThickness, zSize//2 - dirtThickness):
                    newBlock = BlockObject("sand", (x, y, z))
                    self.locationMap[x, y, z] = newBlock
                    self.gameBlockGroup.add(newBlock)
        
         # for debugging
        for x in range(xSize//2 - 2, xSize//2 + 3, 2):
            for y in range(ySize//2 - 2, xSize//2 + 3, 2):
                self.gameBlockGroup.remove(BlockObject("grassDirt"))
                centerBlock = BlockObject("stone", (x, y, 100))  #init at center of map
                self.locationMap[x, y, 100] = centerBlock
                self.gameBlockGroup.add(centerBlock)

    def drawWorld(self, screen, playerPos):
        self.screen.blit(self.background, (0, 0))
        posX = playerPos[0]
        posY = playerPos[1]
        posZ = playerPos[2]
        for x in range(posX - self.renderDist, posX + self.renderDist):
            for y in range(posY - self.renderDist, posY + self.renderDist):
                for z in range(posZ - self.renderDist, posZ + self.renderDist):
                    self.drawBlock(screen, self.locationMap[x, y, z], (x, y, z),
                        playerPos)

# Isometric drawing VERY HEAVILY adapted from http://clintbellanger.net/articles/isometric_math/
    def drawBlockColors(self, screen, blockObj, centerPos, playerPos):
        posX = playerPos[0]
        posY = playerPos[1]
        posZ = playerPos[2]
        x = centerPos[0]
        y = centerPos[1]
        z = centerPos[2]
        # right corner top surface
        x0 = ((x - posX) - (y - posY))*self.blockXWidth/2 + self.width/2 + self.blockXWidth/2
        y0 = ((x - posX) + (y - posY))*self.blockXWidth/(2*2) + self.height/2 - (z - posZ)*self.blockXWidth/2
        # bottom corner top surface
        x1 = x0 - self.blockXWidth/2
        y1 = y0 + self.blockXWidth/(2*2)
        # left corner top surface
        x2 = x0 - self.blockXWidth
        y2 = y0
        # top corner top surface
        x3 = x0 - self.blockXWidth/2
        y3 = y0 - self.blockXWidth/(2*2)
        posTopSurface = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] # draw from right corner CLOCKWISE
        pygame.draw.polygon(screen, (255, 255, 255), posTopSurface)
        pygame.draw.line(screen, (255, 255, 255), (self.width/2, 0), (self.width/2, self.height))
        pygame.draw.line(screen, (255, 255, 255), (0, self.height/2), (self.width, self.height/2))

        # top right corner left surface
        x0Left = x1
        y0Left = y1
        # bottom right corner left surface
        x1Left = x0Left
        y1Left = y0Left + self.blockXWidth/2
        # bottom left corner left surface
        x2Left = x1Left - self.blockXWidth/2
        y2Left = y0Left + self.blockXWidth/(2*2)
        # top left corner left surface
        x3Left = x2Left
        y3Left = y2Left - self.blockXWidth/2
        posLeftSurface = [(x0Left, y0Left), (x1Left, y1Left), (x2Left, y2Left), (x3Left, y3Left)]
        pygame.draw.polygon(screen, (0, 0, 0), posLeftSurface)

        # top right corner right surface
        x0Right = x0
        y0Right = y0
        # bottom right corner right surface
        x1Right = x0Right
        y1Right = y0Right + self.blockXWidth/2
        # bottom left corner right surface
        x2Right = x1Right - self.blockXWidth/2
        y2Right = y1Right + self.blockXWidth/(2*2)
        # top left corner right surface
        x3Right = x2Right
        y3Right = y2Right - self.blockXWidth/2
        posRightSurface = [(x0Right, y0Right), (x1Right, y1Right), (x2Right, y2Right), (x3Right, y3Right)]
        pygame.draw.polygon(screen, (255, 0, 0), posRightSurface)

    def drawBlock(self, screen, block, centerPos, playerPos):
        posX = playerPos[0]
        posY = playerPos[1]
        posZ = playerPos[2]
        x = centerPos[0]
        y = centerPos[1]
        z = centerPos[2]
        if (block.name == "empty"):
            return 0
        blockSurface = Minecraft.blockLib[block.name]
        #drawX = ((x - posX) - (y - posY))*self.blockXWidth/2 + self.width/2 + self.margin - self.blockXWidth
        drawX = ((x - posX) - (y - posY))*self.blockXWidth/2 + self.width/2 + self.blockXWidth/2 - self.blockXWidth  #new test
        drawY = ((x - posX) + (y - posY))*self.blockXWidth/(2*2) + self.height/2 - self.blockXWidth/(2*2) - (z - posZ)*self.blockXWidth/2
        self.screen.blit(blockSurface, (drawX, drawY))
        pygame.draw.line(screen, (255, 255, 255), (self.width/2, 0), (self.width/2, self.height))
        pygame.draw.line(screen, (255, 255, 255), (0, self.height/2), (self.width, self.height/2))

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDragged(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if (keyCode == pygame.K_UP):
            self.player.move(-1, 0, 0, self.locationMap)
        elif (keyCode == pygame.K_DOWN):
            self.player.move(1, 0, 0, self.locationMap)
        elif (keyCode == pygame.K_RIGHT):
            self.player.move(0, -1, 0, self.locationMap)
        elif (keyCode == pygame.K_LEFT):
            self.player.move(0, 1, 0, self.locationMap)
        elif (keyCode == pygame.K_w):  # move up into sky
            self.player.move(0, 0, 1, self.locationMap)
        elif (keyCode == pygame.K_s):  # move down into ground
            self.player.move(0, 0, -1, self.locationMap)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        self.drawWorld(screen, self.player.getPos())
    
game = Minecraft()
        
game.run()