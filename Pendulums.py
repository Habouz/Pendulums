import pygame as pg
import pygame.gfxdraw as pgg
import numpy as np

path = str(input("Do you want to show the path? (Y/N/F) "))
gravity = float(input('Enter the gravity strength. (Default: 1) '))
resistance = float(input('Enter the resistance strength. (Default: 0) '))
stiffness = float(input('Enter the stiffness strength. (Default: 1) '))
g = gravity * 0.002
res = resistance * 0.0005
k = stiffness * 0.001
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
        self.vectored_velocity = []

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

    def mouse_interference(self):
        self.angle = np.arctan2(mouse_x-600, mouse_y-300)
        self.velocity = 0

    def mouse_release(self):
        self.vectored_velocity = np.array([self.y-300, -self.x+600])
        self.velocity = self.vectored_velocity.dot(np.array([general_velocity_x, general_velocity_y])) * 0.00001


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
        self.vectored_velocity_x = []
        self.vectored_velocity_n = []

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
        if self.delta_x > self.length * 2:
            self.velocity_x -= self.delta_x*0.000001
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

    def mouse_interference(self):
        self.angle = mouse_angle
        self.delta_x = mouse_distance - self.length
        self.velocity_n = self.velocity_x = 0

    def mouse_release(self):
        self.vectored_velocity_n = np.array([self.y - 300, -self.x + 600])
        self.vectored_velocity_x = np.array([self.x - 600, self.y - 300])
        self.velocity_n = self.vectored_velocity_n.dot([general_velocity_x, general_velocity_y]) * 0.000001


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
        self.vectored_velocity = []
        self.cache_angle = 0
        self.cache_y = 0

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
            self.angle1 - 2 * self.angle2) - 2 * np.sin(
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

    def mouse_interference(self):
        if mouse_distance < self.length1 + self.length2:
            self.angle1 = np.arccos((self.length1**2 - self.length2 ** 2 + mouse_distance ** 2) / (
                2 * self.length1 * mouse_distance)) + mouse_angle
            self.x1 = 600 + self.length1 * np.sin(self.angle1)
            self.angle2 = np.arcsin((mouse_x-self.x1)/self.length2)
            self.y1 = 300 + self.length1 * np.cos(self.angle1)
            if mouse_y < self.y1:
                self.angle2 = np.pi - np.arcsin((mouse_x-self.x1)/self.length2)
        else:
            self.angle1 = self.angle2 = mouse_angle
        self.velocity1 = 0
        self.velocity2 = 0

    def mouse_release(self):
        self.vectored_velocity = np.array([self.y1 - 300, -self.x1 + 600])
        self.velocity1 = self.velocity2 = self.vectored_velocity.dot(
            [general_velocity_x, general_velocity_y]) * 0.000001


single_pendulum = [SinglePendulum(np.pi / 1.5 - n * 0.1, 0, 10, 100) for n in range(
    1, spendulum_number+1)]
elastic_pendulum = [ElasticPendulum(np.pi / 1.5 - n * 0.1, 0, 0, 0, 10, 100) for n in range(
    1, ependulum_number+1)]
double_pendulum = [DoublePendulum(np.pi / 1.5 - n * 0.1, np.pi / 2, 0, 0, 10, 10, 100, 100) for n in range(
    1, dpendulum_number+1)]

iterator = 0
mouse_angle = 0
general_velocity_x = general_velocity_y = 0
mouse_x = mouse_y = 0
mouse_status = 0
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_status = 1
        if event.type == pg.MOUSEBUTTONUP:
            mouse_status = 0
            general_velocity_x, general_velocity_y = pg.mouse.get_rel()
            for i in single_pendulum:
                i.mouse_release()
            for i in elastic_pendulum:
                i.mouse_release()
            for i in double_pendulum:
                i.mouse_release()
    screen.fill((0, 0, 0))
    if mouse_status == 1:
        for i in single_pendulum:
            i.mouse_interference()
        for i in elastic_pendulum:
            i.mouse_interference()
        for i in double_pendulum:
            i.mouse_interference()
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
    if iterator % 20 == 0:
        pg.mouse.get_rel()
    iterator += 1
    mouse_x, mouse_y = pg.mouse.get_pos( )
    mouse_angle = np.arctan2(mouse_x - 600, mouse_y - 300)
    mouse_distance = np.sqrt((mouse_x - 600) ** 2 + (mouse_y - 300) ** 2)
    pg.display.update()
