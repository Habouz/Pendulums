import pygame as pg
import pygame.gfxdraw as pgg
import numpy as np

res = 0
g = 0.002
k = 0.0005

pg.init( )
screen = pg.display.set_mode((1200, 1000))


class ElasticPendulum:

    def __init__(self, angle, velocity_x, velocity_n, mass, length, delta_x):
        self.angle = angle
        self.velocity_n = velocity_n
        self.velocity_x = velocity_x
        self.mass = mass
        self.length = length
        self.x = 0
        self.y = 0
        self.accelerationx = 0
        self.delta_x = delta_x
        self.accelerationn = 0

    def draw(self):
        self.x = (self.length + self.delta_x) * np.sin(self.angle) + 600
        self.y = (self.length + self.delta_x) * np.cos(self.angle) + 300
        pgg.aacircle(screen, int(self.x), int(self.y), self.mass, (255, 255, 255))
        pg.draw.aaline(screen, (255, 255, 255), (600, 300), (self.x, self.y))

    def mot(self):
        self.accelerationn = (-g * np.sin(self.angle)) / (self.length + self.delta_x) - (
            2 * self.velocity_x * self.velocity_n) / (
                self.length + self.delta_x) - res * self.velocity_n
        self.accelerationx = (self.length + self.delta_x) * self.velocity_n * self.velocity_n - (
            k * self.delta_x) / self.mass + g * np.cos(
                self.angle) - res * self.velocity_x
        self.velocity_n += self.accelerationn
        self.velocity_x += self.accelerationx
        self.angle += self.velocity_n
        self.delta_x += self.velocity_x

    def motraw(self):
        self.mot()
        self.draw()


obj = [ElasticPendulum(np.pi / 2 + n * 0.1, 0, 0, 10, 100, n) for n in range(0, 5)]
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in obj:
        i.motraw()
    pg.display.update()
