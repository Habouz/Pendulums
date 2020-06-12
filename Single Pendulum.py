import pygame as pg
import pygame.gfxdraw as pgg
import numpy as np

g = 0.002
res = 0.001

pg.init( )
screen = pg.display.set_mode((1200, 1000))


class SinglePendulum:
    def __init__(self, angle, velocity, mass, length):
        self.angle = angle
        self.velocity = velocity
        self.mass = mass
        self.length = length
        self.acc = 0
        self.x = 0
        self.y = 0

    def draw(self):
        self.x = self.length * np.sin(self.angle) + 600
        self.y = self.length * np.cos(self.angle) + 300
        pgg.aacircle(screen, int(self.x), int(self.y), self.mass, (255, 255, 255))
        pg.draw.aaline(screen, (255, 255, 255), (600, 300), (self.x, self.y))

    def mot(self):
        self.acc = -(g / self.length) * np.sin(self.angle) - res * self.velocity
        self.velocity += self.acc
        self.angle += self.velocity

    def motraw(self):
        self.mot()
        self.draw()


obj = [SinglePendulum(n * 0.3, 0, 10, 100) for n in range(1, 9)]
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in obj:
        i.motraw()
    pg.display.update()
