# Template adapted from
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/pygamegame.py
import pygame, time
import numpy as np


class PygameGame(object):
    def mousePressed(self, x, y):
        raise NotImplementedError

    def mouseReleased(self, x, y):
        raise NotImplementedError

    def mouseMotion(self, x, y):
        raise NotImplementedError

    def mouseDragged(self, x, y):
        raise NotImplementedError

    def keyPressed(self, keyCode, modifier):
        raise NotImplementedError

    def keyReleased(self, keyCode, modifier):
        raise NotImplementedError

    def timerFired(self, dt):
        raise NotImplementedError

    def redrawAll(self, screen):
        raise NotImplementedError

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=550, height=550, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        clock = pygame.time.Clock()
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        #self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDragged(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            # self.screen.fill(self.bgColor)
            self.redrawAll(self.screen)
            pygame.display.update()

        pygame.quit()


class BlockObject(pygame.sprite.Sprite):
    def __init__(self, name, gameCoords=(-1, -1, -1)): # -1 is empty block
        super().__init__()
        self.name = name  # string - use keys of Miencraft.blockLib
        self.gameX = gameCoords[0]  # int
        self.gameY = gameCoords[1]
        self.gameZ = gameCoords[2]


class Player(pygame.sprite.Sprite):
    def __init__(self, gameCoords=(100, 100, 100)):
        super.__init()
        self.gameX = gameCoords[0]  # integer
        self.gameY = gameCoords[1]
        self.gameZ = gameCoords[2]
        # self.surfDownLeft = pygame.image.load("playerdownleft.png")
        # self.surfDownRight = pygame.image.load("playerdownright.png")
        # self.surfUpLeft = pygame.image.load("playerupleft.png")
        # self.surfUpRight = pygame.image.load("playerupright.png")


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

    def drawWorld(self, screen, posX, posY, posZ):
        # posX, posY, posZ is center of drawing; current location of player
        # for loops chosen CAREFULLY to be able to blit surfaces properly...
        curr = time.time()
        for x in range(posX - self.renderDist, posX + self.renderDist):
            for y in range(posY - self.renderDist, posY + self.renderDist):
                for z in range(posZ - self.renderDist, posZ + self.renderDist):
                    self.drawBlock(screen, self.locationMap[x, y, z], x, y, z,
                        posX, posY, posZ)
        print(time.time() - curr)

# Very heavily adapted from http://clintbellanger.net/articles/isometric_math/
    def drawBlockColors(self, screen, blockObj, x, y, z, posX, posY, posZ):
        # right corner top surface
        x0 = ((x - posX) - (y - posY))*self.blockXWidth/2 + self.width/2 + self.margin
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

    def drawBlock(self, screen, block, x, y, z, posX, posY, posZ):
        if (block.name == "empty"):
            return 0
        blockSurface = Minecraft.blockLib[block.name]
        drawX = ((x - posX) - (y - posY))*self.blockXWidth/2 + self.width/2 + self.margin - self.blockXWidth
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
        # self.drawBlock(self.screen, "HEELLO", 99, 99, 100, 100, 100, 100)
        #self.drawBlock(self.screen, "HEELLO", 100, 100, 100, 100, 100, 100)
        # self.drawBlock(self.screen, "HEELLO", 101, 101, 100, 100, 100, 100)
        # self.drawBlock(self.screen, "HEELLO", 102, 102, 100, 100, 100, 100)
        # self.drawBlock(self.screen, "HEELLO", 101, 100, 100, 100, 100, 100)
        self.drawWorld(self.screen, 100, 100, 100)

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass
    
game = Minecraft()
        
game.run()