import pygame
from BlockObject import *

class Player(pygame.sprite.Sprite):
    def __init__(self, blockXWidth, gameCoords=(100, 100, 100)):
        super().__init__()
        self.gameX = gameCoords[0]  # integer
        self.gameY = gameCoords[1]
        self.gameZ = gameCoords[2]
        self.direction = "+y"  # facing down to bottom left at first
        # steve image from https://minecraft.gamepedia.com/File:Steve.png
        self.surfPlusY = Player.scale(pygame.image.load("isotex/steve1.png"), blockXWidth)
        # self.surfDownLeft = pygame.image.load("playerdownleft.png")
        # self.surfDownRight = pygame.image.load("playerdownright.png")
        # self.surfUpLeft = pygame.image.load("playerupleft.png")
        # self.surfUpRight = pygame.image.load("playerupright.png")
    
    @staticmethod
    def scale(surf, blockXWidth):
        (xSize, ySize) = surf.get_size()
        factor = blockXWidth/xSize
        newXDim = blockXWidth
        newYDim = int(ySize*factor)
        scaleToDimsNew = (newXDim, newYDim)
        newSurf = pygame.transform.scale(surf, scaleToDimsNew)
        return newSurf

    
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
        returnValLegalPlayerPos = self.getLegalPlayerPos(dx, dy, dz, locationMap)
        if (returnValLegalPlayerPos == False):
            print("Cannot move to:", (self.gameX + dx, self.gameY + dy, self.gameZ + dz), "Current Pos:", (self.gameX, self.gameY, self.gameZ))
            return False # cannot move
        else:
            x = returnValLegalPlayerPos[0]
            y = returnValLegalPlayerPos[1]
            z = returnValLegalPlayerPos[2]
            self.gameX = x
            self.gameY = y
            self.gameZ = z
            print("Moved to:", (x, y, z), "/ Dir:", self.direction)
        
            return True
        # direction dz doesn't matter
        # probably should do bounds checking here also
    
    def getPos(self):
        return (self.gameX, self.gameY, self.gameZ)
    
    def placeBlock(self, block, locationMap, gameBlockGroup, zOffset):
        if (self.getPlaceBlockLocation(locationMap, zOffset) == False):
            print("Block not placed")
            return False # block not placed
        else:
            (x, y, z) = self.getPlaceBlockLocation(locationMap, zOffset) # get locations at which block is to be placed
            locationMap[x, y, z] = block
            gameBlockGroup.add(block)
            print("Block placed at: ", (x, y, z))
            return True  # block successfully placed
    
    def getPlaceBlockLocation(self, locationMap, zOffset):  # gets location at which block has to be placed
        if (self.direction == "+y"): # facing down the y direction
            (x, y, z) = (self.gameX, self.gameY + 1, self.gameZ + zOffset)  # coords being considered; block to be placed is at same level as player
            # player pos is inside the block itself so we need to shift up
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"): # check legal block placement
                return (x, y, z)
            else: return False # false is when cannot place block
        elif (self.direction == "-y"): # facing opposite y direction
            (x, y, z) = (self.gameX, self.gameY - 1, self.gameZ + zOffset)
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"):
                return (x, y, z)
            else: return False
        elif (self.direction == "+x"): # facing down the x direction
            (x, y, z) = (self.gameX + 1, self.gameY, self.gameZ + zOffset)
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"):
                return (x, y, z)
            else: return False
        elif (self.direction == "-x"): # facing opposite z direction
            (x, y, z) = (self.gameX - 1, self.gameY, self.gameZ + zOffset)
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z - 1].name != "empty"):
                return (x, y, z)
            else: return False
        else:
            raise Exception("Block location/name not found")
    
    def getLegalPlayerPos(self, dx, dy, dz, locationMap):  # gets location at which block has to be placed
        if (dx != 0): # move in x
            (x, y, z) = (self.gameX + dx, self.gameY, self.gameZ) # that player about to move to
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z + 1].name == "empty"): # player takes up two z-blocks
                return self.lowerPlayerToGround(x, y, z, locationMap)
            elif (locationMap[x, y, z] != "empty" and locationMap[x, y, z + 1].name == "empty" and locationMap[x, y, z + 2].name == "empty"):
                return self.lowerPlayerToGround(x, y, z + 1, locationMap)
        elif (dy != 0): # move in y
            (x, y, z) = (self.gameX, self.gameY + dy, self.gameZ) # that player about to move to
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z + 1].name == "empty"): # player takes up two z-blocks
                return self.lowerPlayerToGround(x, y, z, locationMap)
            elif (locationMap[x, y, z] != "empty" and locationMap[x, y, z + 1].name == "empty" and locationMap[x, y, z + 2].name == "empty"):
                return self.lowerPlayerToGround(x, y, z + 1, locationMap)
        elif (dz != 0): # move in z
            (x, y, z) = (self.gameX, self.gameY , self.gameZ + dz) # that player about to move to
            if (locationMap[x, y, z].name == "empty" and locationMap[x, y, z + 1].name == "empty"): # player takes up two z-blocks
                return self.lowerPlayerToGround(x, y, z, locationMap)
            elif (locationMap[x, y, z] != "empty" and locationMap[x, y, z + 1].name == "empty" and locationMap[x, y, z + 2].name == "empty"):
                return self.lowerPlayerToGround(x, y, z + 1, locationMap)
        elif (dx == 0 and dy == 0 and dz == 0): # no movement, used for initializing the loweringplayertoground
            (x, y, z) = (self.gameX, self.gameY, self.gameZ)
            return self.lowerPlayerToGround(x, y, z, locationMap)
        return False
    
    def lowerPlayerToGround(self, x, y, z, locationMap):
        tempZ = z
        while (locationMap[x, y, tempZ].name == "empty"): # keep lowering calculated player pos until they reach the ground
            tempZ -= 1
        if (tempZ == z):
            return False
        return (x, y, tempZ + 1)

    
    def destroyBlock(self, locationMap, gameBlockGroup, zOffset):
        (x, y, z) = (self.gameX, self.gameY, self.gameZ + zOffset)
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
        elif (self.direction == "-x"): # looking down at -x
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
        
    def draw(self, screen, surf, gameWidth, gameHeight, blockXWidth):
        drawX = gameWidth/2 + blockXWidth/2 - blockXWidth
        (xSurfSize, ySurfSize) = surf.get_size()
        yRealisticShift = blockXWidth/(2*2) # shift a bit to make steve look like he's on the block
        drawY = gameHeight/2 - ySurfSize + yRealisticShift
        screen.blit(self.surfPlusY, (drawX, drawY))
