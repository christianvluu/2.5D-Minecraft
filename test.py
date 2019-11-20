import pygame
import numpy as np
import time
pygame.init()
screen = pygame.display.set_mode((550, 550))
image1 = pygame.image.load("cat.png")
print(repr(image1))
pygame.Surface.blit(image1, (550/2, 550/2))
pygame.Surface.update()