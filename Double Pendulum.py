import pygame as pg
import pygame.gfxdraw as pgg
import numpy as np

g = 0.002
res = 0

pg.init()
screen = pg.display.set_mode((1200, 1000))


class DoublePendulum:

    def __init__(self, angle1, angle2, velocity1, velocity2, length1, length2, mass1, mass2):
        self.angle1 = angle1
        self.angle2 = angle2
        self.velocity1 = velocity1
        self.velocity2 = velocity2
        self.acceleration1 = 0
        self.acceleration2 = 0
        self.length1 = length1
        self.length2 = length2
        self.mass1 = mass1
        self.mass2 = mass2
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def draw(self):
        self.x1 = 600 + self.length1 * np.sin(self.angle1)
        self.y1 = 300 + self.length1 * np.cos(self.angle1)
        self.x2 = self.x1 + self.length2 * np.sin(self.angle2)
        self.y2 = self.y1 + self.length2 * np.cos(self.angle2)
        pgg.aacircle(screen, int(self.x1), int(self.y1), 10, (255, 255, 255))
        pgg.aacircle(screen, int(self.x2), int(self.y2), 10, (255, 255, 255))
        pg.draw.aaline(screen, (255, 255, 255), (600, 300), (int(self.x1), int(self.y1)), 10)
        pg.draw.aaline(screen, (255, 255, 255), (int(self.x1), int(self.y1)), (int(self.x2), int(self.y2)), 10)

    def mot(self):
        self.acceleration1 = (-g * (2 * self.mass1 + self.mass2) * np.sin(self.angle1) - self.mass2 * g * np.sin(
            self.angle1 + self.angle2) - 2 * np.sin(
                self.angle1 - self.angle2) * self.mass2 * (
                    self.velocity2 * self.velocity2 * self.length2 + self.velocity1 * self.velocity1 * (
                        self.length1 * np.cos(
                            self.angle1 - self.angle2)))) / (
                                self.length1 * (
                                    2 * self.mass1 + self.mass2 - self.mass2 * np.cos(
                                        2 * self.angle1 - 2 * self.angle2))) - (
                                            res * self.velocity1)
        self.acceleration2 = (2 * np.sin(self.angle1 - self.angle2) * (
            self.velocity1 * self.velocity1 * self.length1 * (self.mass1 + self.mass2) + g * (
                self.mass1 + self.mass2) * np.cos(
                    self.angle1) + self.velocity2 * self.velocity2 * self.length2 * self.mass2 * np.cos(
                        self.angle1 - self.angle2))) / (
                            self.length1 * (
                                2 * self.mass1 + self.mass2 - self.mass2 * np.cos(
                                    2 * self.angle1 - 2 * self.angle2))) - res * self.velocity2
        self.velocity1 += self.acceleration1
        self.velocity2 += self.acceleration2
        self.angle1 += self.velocity1
        self.angle2 += self.velocity2

    def motraw(self):
        self.mot( )
        self.draw( )


obj = [DoublePendulum(np.pi / 1.5 - n * 0.1, np.pi / 2, 0, 0, 100, 100, 10, 10) for n in range(1, 6)]
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in obj:
        i.motraw()
    pg.display.update()
