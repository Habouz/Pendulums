import pygame as pg
import pygame.gfxdraw as pgg
import numpy as np

path = str(input("Do you want to show the path? (Y/N/F) "))
gravity = float(input('Enter the gravity strength. (Default: 1) '))
resistance = float(input('Enter the resistance strength. (Default: 0) '))
stiffness = float(input('Enter the stiffness strength. (Default: 1) '))
g = gravity * 0.002
res = resistance * 0.0005
k = stiffness * 0.0005
spendulum_number = int(input('Enter the number of Single Pendulums. '))
ependulum_number = int(input('Enter the number of Elastic Pendulums. '))
dpendulum_number = int(input('Enter the number of Double Pendulums. '))

pg.init( )
screen = pg.display.set_mode((1200, 1000))


class SinglePendulum:
    def __init__(self, angle, velocity, mass, length):
        self.angle = angle
        self.velocity = velocity
        self.mass = mass
        self.length = length
        self.acc = 0
        self.x = self.length * np.sin(self.angle) + 600
        self.y = self.length * np.cos(self.angle) + 300
        self.array = [[int(self.x), int(self.y)]]

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

    def path(self):
        self.array.reverse()
        self.array.append([self.x, self.y])
        if len(self.array) > 100 and path == "F":
            self.array.pop(0)
        elif len(self.array) > 1000:
            self.array.pop(0)
        self.array.reverse()
        pg.draw.aalines(screen, (255, 255, 255), False, self.array)


class ElasticPendulum:

    def __init__(self, angle, delta_x, velocity_n, velocity_x, mass, length):
        self.angle = angle
        self.delta_x = delta_x
        self.velocity_n = velocity_n
        self.velocity_x = velocity_x
        self.mass = mass
        self.length = length
        self.x = (self.length + self.delta_x) * np.sin(self.angle) + 600
        self.y = (self.length + self.delta_x) * np.cos(self.angle) + 300
        self.accelerationx = 0
        self.accelerationn = 0
        self.array = [[int(self.x), int(self.y)]]

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

    def path(self):
        self.array.reverse()
        self.array.append([self.x, self.y])
        if len(self.array) > 100 and path == "F":
            self.array.pop(0)
        elif len(self.array) > 1000:
            self.array.pop(0)
        self.array.reverse()
        pg.draw.aalines(screen, (255, 255, 255), False, self.array)


class DoublePendulum:

    def __init__(self, angle1, angle2, velocity1, velocity2, mass1, mass2, length1, length2):
        self.angle1 = angle1
        self.angle2 = angle2
        self.velocity1 = velocity1
        self.velocity2 = velocity2
        self.acceleration1 = 0
        self.acceleration2 = 0
        self.mass1 = mass1
        self.mass2 = mass2
        self.length1 = length1
        self.length2 = length2
        self.x1 = 600 + self.length1 * np.sin(self.angle1)
        self.y1 = 300 + self.length1 * np.cos(self.angle1)
        self.x2 = self.x1 + self.length2 * np.sin(self.angle2)
        self.y2 = self.y1 + self.length2 * np.cos(self.angle2)
        self.array = [[int(self.x2), int(self.y2)]]

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

    def path(self):
        self.array.reverse()
        self.array.append([self.x2, self.y2])
        if len(self.array) > 100 and path == "F":
            self.array.pop(0)
        elif len(self.array) > 1000:
            self.array.pop(0)
        self.array.reverse()
        pg.draw.aalines(screen, (255, 255, 255), False, self.array)


single_pendulum = [SinglePendulum(np.pi / 1.5 - n * 0.1, 0, 10, 100) for n in range(
    1, spendulum_number+1)]
elastic_pendulum = [ElasticPendulum(np.pi / 1.5 - n * 0.1, 0, 0, 0, 10, 100) for n in range(
    1, ependulum_number+1)]
double_pendulum = [DoublePendulum(np.pi / 1.5 - n * 0.1, np.pi / 2, 0, 0, 10, 10, 100, 100) for n in range(
    1, dpendulum_number+1)]

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in single_pendulum:
        i.motraw()
        if path == "Y" or "F":
            i.path()
    for i in elastic_pendulum:
        i.motraw()
        if path == "Y" or "F":
            i.path()
    for i in double_pendulum:
        i.motraw()
        if path == "Y" or "F":
            i.path()
    pg.display.update()
