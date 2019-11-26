import pygame

class BlockObject(pygame.sprite.Sprite):
    def __init__(self, name): # -1 is empty block
        super().__init__()
        self.name = name  # string - use keys of Minecraft.blockLib
        # location of block is stored in locationMap
        # self.gameX = gameCoords[0]  # int
        # self.gameY = gameCoords[1]
        # self.gameZ = gameCoords[2]