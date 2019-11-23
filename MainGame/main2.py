import pygame, time
import numpy as np
# Pygame usage from http://blog.lukasperaza.com/getting-started-with-pygame/
# and Official Documentation https://www.pygame.org/docs/ 
from pygametemplate import *

class BlockObject(pygame.sprite.Sprite):
    def __init__(self, name): # -1 is empty block
        super().__init__()
        self.name = name  # string - use keys of Minecraft.blockLib
        # location of block is stored in locationMap
        # self.gameX = gameCoords[0]  # int
        # self.gameY = gameCoords[1]
        # self.gameZ = gameCoords[2]


class Player(pygame.sprite.Sprite):
    def __init__(self, gameCoords=(100, 100, 100)):
        super().__init__()
        self.gameX = gameCoords[0]  # integer
        self.gameY = gameCoords[1]
        self.gameZ = gameCoords[2]
        self.direction = "+y"  # facing down to bottom left at first
        # steve image from https://minecraft.gamepedia.com/File:Steve.png
        self.surfPlusY = Minecraft.scale(pygame.image.load("isotex/steve1.png"), Minecraft.blockXWidth)
        # self.surfDownLeft = pygame.image.load("playerdownleft.png")
        # self.surfDownRight = pygame.image.load("playerdownright.png")
        # self.surfUpLeft = pygame.image.load("playerupleft.png")
        # self.surfUpRight = pygame.image.load("playerupright.png")
    
    def move(self, dx, dy, dz, locationMap):
        # keep track of where the player is facing (helpful for placing and
        # destroying blocks) Also useful for movement also
        if (dy > 0):
            self.direction = "+y"
        elif (dy < 0):
            self.direction = "-y"
        elif (dx > 0):
            self.direction = "+x"
        elif (dx < 0):
            self.direction = "-x"
        if (self.getLegalPlayerPos(dx, dy, dz, locationMap) == False):
            print("Cannot move to:", (self.gameX + dx, self.gameY + dy, self.gameZ + dz), "Current Pos:", (self.gameX, self.gameY, self.gameZ))
            return False # cannot move
        else:
            (x, y, z) = self.getLegalPlayerPos(dx, dy, dz, locationMap)
            self.gameX = x
            self.gameY = y
            self.gameZ = z
            print("Moved to:", (x, y, z), "/ Dir:", self.direction)
        
            return True
        # direction dz doesn't matter
        # probably should do bounds checking here also
    
    def getPos(self):
        return (self.gameX, self.gameY, self.gameZ)
    
    def placeBlock(self, block, locationMap, gameBlockGroup):
        if (self.getPlaceBlockLocation(locationMap) == False):
            print("Block not placed")
            return False # block not placed
        else:
            (x, y, z) = self.getPlaceBlockLocation(locationMap) # get locations at which block is to be placed
            locationMap[x, y, z] = block
            gameBlockGroup.add(block)
            print("Block placed at: ", (x, y, z))
            return True  # block successfully placed
    
    def getPlaceBlockLocation(self, locationMap):  # gets location at which block has to be placed
        if (self.direction == "+y"): # facing down the y direction
            (x, y, z) = (self.gameX, self.gameY + 1, self.gameZ)  # coords being considered; block to be placed is at same level as player
            # player pos is inside the block itself so we need to shift up
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"): # check legal block placement
                return (x, y, z)
            else: return False # false is when cannot place block
        elif (self.direction == "-y"): # facing opposite y direction
            (x, y, z) = (self.gameX, self.gameY - 1, self.gameZ)
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"):
                return (x, y, z)
            else: return False
        elif (self.direction == "+x"): # facing down the x direction
            (x, y, z) = (self.gameX + 1, self.gameY, self.gameZ)
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"):
                return (x, y, z)
            else: return False
        elif (self.direction == "-y"): # facing opposite z direction
            (x, y, z) = (self.gameX, self.gameY - 1, self.gameZ)
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"):
                return (x, y, z)
            else: return False
        else:
            raise Exception("Block location/name not found")
    
    def getLegalPlayerPos(self, dx, dy, dz, locationMap):  # gets location at which block has to be placed
        if (dx != 0): # move in x
            (x, y, z) = (self.gameX + dx, self.gameY, self.gameZ) # that player about to move to
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z + 1].name == "empty"): # player takes up two z-blocks
                return (x, y, z)
            else: return False
        elif (dy != 0): # move in y
            (x, y, z) = (self.gameX, self.gameY + dy, self.gameZ) # that player about to move to
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z + 1].name == "empty"): # player takes up two z-blocks
                return (x, y, z)
            else: return False
        elif (dz != 0): # move in z
            (x, y, z) = (self.gameX, self.gameY , self.gameZ + dz) # that player about to move to
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z + 1].name == "empty"): # player takes up two z-blocks
                return (x, y, z)
            else: return False
    
    def destroyBlock(self, locationMap, gameBlockGroup):
        (x, y, z) = (self.gameX, self.gameY, self.gameZ)
        if (self.direction == "+y"): # looking down at +y
            if (locationMap[x, y + 1, z].name != "empty"):
                emptyBlock = BlockObject("empty")
                gameBlockGroup.remove(locationMap[x, y + 1, z])
                locationMap[x, y + 1, z] = emptyBlock
                gameBlockGroup.add(emptyBlock)
                print("Block Destroyed")
                return True
            else:
                print("No blocks to destroy")
                return False
        elif (self.direction == "-y"): # looking down at -y
            if (locationMap[x, y - 1, z].name != "empty"):
                emptyBlock = BlockObject("empty")
                gameBlockGroup.remove(locationMap[x, y - 1, z])
                locationMap[x, y - 1, z] = emptyBlock
                gameBlockGroup.add(emptyBlock)
                print("Block Destroyed")
                return True
            else:
                print("No blocks to destroy")
                return False
        elif (self.direction == "+x"): # looking down at +x
            if (locationMap[x + 1, y, z].name != "empty"):
                emptyBlock = BlockObject("empty")
                gameBlockGroup.remove(locationMap[x + 1, y, z])
                locationMap[x + 1, y, z] = emptyBlock
                gameBlockGroup.add(emptyBlock)
                print("Block Destroyed")
                return True
            else:
                print("No blocks to destroy")
                return False
        elif (self.direction == "+y"): # looking down at -x
            if (locationMap[x - 1, y, z].name != "empty"):
                emptyBlock = BlockObject("empty")
                gameBlockGroup.remove(locationMap[x - 1, y, z])
                locationMap[x - 1, y, z] = emptyBlock
                gameBlockGroup.add(emptyBlock)
                print("No blocks to destroy")
                return True
            else:
                print("Block NOT destroyed")
                return False
        


class Minecraft(PygameGame):
    blockTex = None
    blockLib = None
    blockXWidth = None

    def __init__(self):
        super().__init__(title="Minecraft")
        self.locationMap = np.full((200, 200, 200), BlockObject("empty"))
        # use self.location[x,y,z] to refer to a point
        self.gameDims = (200, 200, 200)
        self.margin = 25
        self.renderDist = 5  # blocks from user
        Minecraft.blockXWidth = (self.width - 2*self.margin)//(2*self.renderDist)
        # background from http://www.tassal.com.au/sustainability/blue-background-png/
        self.background = pygame.image.load("background.png")
        self.screen.blit(self.background, (0, 0))
        self.gameBlockGroup = pygame.sprite.Group()
        self.initBlockLibrary()  # group textures
        self.perspective = 1 # default perspective, with origin up top
        self.createFlatWorld(
            xSize=self.gameDims[0],
            ySize=self.gameDims[1],
            zSize=self.gameDims[2])
        self.player = Player((self.gameDims[0]//2, self.gameDims[1]//2, self.gameDims[2]//2 + 1)) # player pos is above the block player is standing on
    
    def initBlockLibrary(self):
        Minecraft.blockLib = {
        # textures purchased from
        # https://www.yandidesigns.com/2017/07/how-to-make-flat-isometric-block-like-minecraft-affinity-designer.html
            "dirt":
                Minecraft.scale(pygame.image.load("isotex/dirt.png"), Minecraft.blockXWidth),
            "interiorStone":
                Minecraft.scale(pygame.image.load("isotex/interiorstone.png"), Minecraft.blockXWidth),
            "grassDirt":
                Minecraft.scale(pygame.image.load("isotex/grassdirt.png"), Minecraft.blockXWidth),
            "grass":
                Minecraft.scale(pygame.image.load("isotex/grass.png"), Minecraft.blockXWidth),
            "snow":
                Minecraft.scale(pygame.image.load("isotex/snow.png"), Minecraft.blockXWidth),
            "sand":
                Minecraft.scale(pygame.image.load("isotex/sand.png"), Minecraft.blockXWidth),
            "stone":
                Minecraft.scale(pygame.image.load("isotex/stone.png"), Minecraft.blockXWidth),
            "sandStone":
                Minecraft.scale(pygame.image.load("isotex/sandstone.png"), Minecraft.blockXWidth),
            "stoneDirt":
                Minecraft.scale(pygame.image.load("isotex/stonedirt.png"), Minecraft.blockXWidth),
            "stoneSnow":
                Minecraft.scale(pygame.image.load("isotex/stonesnow.png"), Minecraft.blockXWidth),
            "dirtSand":
                Minecraft.scale(pygame.image.load("isotex/dirtsand.png"), Minecraft.blockXWidth),
            "dirtRock":
                Minecraft.scale(pygame.image.load("isotex/dirtrock.png"), Minecraft.blockXWidth),
            "grassStone":
                Minecraft.scale(pygame.image.load("isotex/grassstone.png"), Minecraft.blockXWidth)
        }
    
    @staticmethod
    def scale(surf, scaleToDims):
        # scales surface to correct dimensions for drawing
        newDims = (scaleToDims, scaleToDims)  # for resizing image
        newSurf = pygame.transform.scale(surf, newDims)
        return newSurf

    def createFlatWorld(self, xSize=200, ySize=200, zSize=200):
        self.screen.blit(self.background, (0, 0))
        # world center is at xSize//2, ySize//2, zSize//2
        dirtThickness = 2  # goes from center down
        stoneThickness = 3
        for x in range(0, xSize):
            for y in range(0, ySize):
                newBlock = BlockObject("grassDirt")
                self.locationMap[x, y, zSize//2] = newBlock
                self.gameBlockGroup.add(newBlock)
                for z in range(zSize//2 - dirtThickness, zSize//2):
                    newBlock = BlockObject("dirt")
                    self.locationMap[x, y, z] = newBlock
                    self.gameBlockGroup.add(newBlock)
                for z in range(zSize//2 - dirtThickness - stoneThickness, zSize//2 - dirtThickness):
                    newBlock = BlockObject("sand")
                    self.locationMap[x, y, z] = newBlock
                    self.gameBlockGroup.add(newBlock)
        
         # for debugging
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
            for x in range(posX - self.renderDist, posX + self.renderDist):
                for y in range(posY - self.renderDist, posY + self.renderDist):
                    for z in range(posZ - self.renderDist, posZ + self.renderDist):
                        self.drawBlock(screen, self.locationMap[x, y, z], (x, y, z),
                            playerPos)
        elif (perspective == 2):
            for x in range(posX - self.renderDist, posX + self.renderDist):
                for y in range(posY + self.renderDist - 1, posY - self.renderDist - 1, -1):
                    for z in range(posZ - self.renderDist, posZ + self.renderDist):
                        self.drawBlock(screen, self.locationMap[x, y, z], (x, y, z),
                            playerPos)

# Isometric drawing VERY HEAVILY adapted from http://clintbellanger.net/articles/isometric_math/
    def drawBlockColors(self, screen, blockObj, centerPos, playerPos):
        posX = playerPos[0]
        posY = playerPos[1]
        posZ = playerPos[2] - 1  # player pos is above the block player is standing on so need to -1 to draw
        x = centerPos[0]
        y = centerPos[1]
        z = centerPos[2]
        # right corner top surface
        x0 = ((x - posX) - (y - posY))*Minecraft.blockXWidth/2 + self.width/2 + Minecraft.blockXWidth/2
        y0 = ((x - posX) + (y - posY))*Minecraft.blockXWidth/(2*2) + self.height/2 - (z - posZ)*Minecraft.blockXWidth/2
        # bottom corner top surface
        x1 = x0 - Minecraft.blockXWidth/2
        y1 = y0 + Minecraft.blockXWidth/(2*2)
        # left corner top surface
        x2 = x0 - Minecraft.blockXWidth
        y2 = y0
        # top corner top surface
        x3 = x0 - Minecraft.blockXWidth/2
        y3 = y0 - Minecraft.blockXWidth/(2*2)
        posTopSurface = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] # draw from right corner CLOCKWISE
        pygame.draw.polygon(screen, (255, 255, 255), posTopSurface)
        pygame.draw.line(screen, (255, 255, 255), (self.width/2, 0), (self.width/2, self.height))
        pygame.draw.line(screen, (255, 255, 255), (0, self.height/2), (self.width, self.height/2))

        # top right corner left surface
        x0Left = x1
        y0Left = y1
        # bottom right corner left surface
        x1Left = x0Left
        y1Left = y0Left + Minecraft.blockXWidth/2
        # bottom left corner left surface
        x2Left = x1Left - Minecraft.blockXWidth/2
        y2Left = y0Left + Minecraft.blockXWidth/(2*2)
        # top left corner left surface
        x3Left = x2Left
        y3Left = y2Left - Minecraft.blockXWidth/2
        posLeftSurface = [(x0Left, y0Left), (x1Left, y1Left), (x2Left, y2Left), (x3Left, y3Left)]
        pygame.draw.polygon(screen, (0, 0, 0), posLeftSurface)

        # top right corner right surface
        x0Right = x0
        y0Right = y0
        # bottom right corner right surface
        x1Right = x0Right
        y1Right = y0Right + Minecraft.blockXWidth/2
        # bottom left corner right surface
        x2Right = x1Right - Minecraft.blockXWidth/2
        y2Right = y1Right + Minecraft.blockXWidth/(2*2)
        # top left corner right surface
        x3Right = x2Right
        y3Right = y2Right - Minecraft.blockXWidth/2
        posRightSurface = [(x0Right, y0Right), (x1Right, y1Right), (x2Right, y2Right), (x3Right, y3Right)]
        pygame.draw.polygon(screen, (255, 0, 0), posRightSurface)

    def drawBlock(self, screen, block, centerPos, playerPos):
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
        drawX = ((x - posX) - (y - posY))*Minecraft.blockXWidth/2 + self.width/2 + Minecraft.blockXWidth/2 - Minecraft.blockXWidth
        drawY = ((x - posX) + (y - posY))*Minecraft.blockXWidth/(2*2) + self.height/2 - Minecraft.blockXWidth/(2*2) - (z - posZ)*Minecraft.blockXWidth/2
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
        elif (keyCode == pygame.K_SPACE):
            self.player.placeBlock(BlockObject("stone"), self.locationMap, self.gameBlockGroup)
        elif (keyCode == pygame.K_1):
            self.perspective = 1
        elif (keyCode == pygame.K_2):
            self.perspective = 2
        elif (keyCode == pygame.K_d):
            self.player.destroyBlock(self.locationMap, self.gameBlockGroup)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        self.drawWorld(screen, self.player.getPos(), self.perspective)
    
game = Minecraft()
        
game.run()