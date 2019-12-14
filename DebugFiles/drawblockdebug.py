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
