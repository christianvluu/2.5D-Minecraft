import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, imageLoc, buttonDims, pos): # x and y is position on screen
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imageLoc), buttonDims)
        self.rect = self.image.get_rect()
        # declaring variables for sprites: http://programarcadegames.com/index.php?chapter=introduction_to_sprites
        self.rect.x = pos[0]
        self.rect.y = pos[1]