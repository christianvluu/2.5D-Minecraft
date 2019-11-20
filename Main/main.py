import pygame
# Minecraft images from:
# "https://www.vexels.com/vectors/preview/144600/isometric-
# landscape-cube-minecraft-style" designed by Vexels

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init()
        # use convert to speed things up
        self.objSurface = pygame.image.load(image).convert()
        #shift objects so they are drwn in the center
        self.cx = pos[0] - self.objSurface.get_width()/2
        self.cy = pos[1] - self.objSurface.get_height()/2

class Game(object):
    def __init__(self, gameDims=(600, 600)):
        self.screen = pygame.display.set_mode(gameDims)
        self.fps = 50
        self.width = gameDims[0]
        self.height = gameDims[1]

    def redrawAll(self, screen):
        raise NotImplementedError

class Minecraft(Game):
    def __init__(self, gameDims=(600,00)):
        super.__init__(gameDims)
        self.background = pygame.image.load("background.png").convert()
        self.screen.blit(self.background, (0, 0))
    
    def drawGameObjects(self, screen):
        for gameObj in self.gameObjects:
            self.screen.blit(gameObj.objSurface, (gameObj.cx, gameObj.cy))
        pygame.display.update()
    
    

