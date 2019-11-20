import pygame
# Template adapted from
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/pygamegame.py
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