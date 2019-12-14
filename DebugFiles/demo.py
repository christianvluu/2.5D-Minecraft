import pygame

gameDims = (600, 600)
surf = pygame.Surface(gameDims)

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(gameDims)

playing = True
while playing:
    time = clock.tick(fps) # waits for the next frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
pygame.quit()