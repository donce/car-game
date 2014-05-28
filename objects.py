import math
import pygame


#TODO: extract 'drawable' subclass (with draw method)
class Object(object):
    def __init__(self, surface, angle=0, pos=(0, 0)):
        self.surface = surface
        self.angle = angle
        self.pos = pos

    def draw(self, surface, pos=(0, 0)):
        raise NotImplementedError

    def forward(self, distance):
        x = self.pos[0]
        y = self.pos[1]
        nx = x - math.cos(self.angle / 180.0 * 3.14) * distance
        ny = y + math.sin(self.angle / 180.0 * 3.14) * distance
        self.pos = (nx, ny)


class ImageObject(Object):
    def __init__(self, image, surface, angle=0, pos=(0, 0)):
        super(ImageObject, self).__init__(surface, angle, pos)
        self.image = image

    def draw(self):
        rotated = pygame.transform.rotate(self.image, self.angle)
        pos = (self.pos[0] - rotated.get_width() / 2, self.pos[1] - rotated.get_height() / 2)
        self.surface.blit(rotated, pos)


# class Updatable(object):
#     def update(self, time):
#         raise NotImplementedError


#TODO: updatable
class Car(ImageObject):
    controller = None
    speed = 0

    def __init__(self, controller, image, surface, angle=0, pos=(0, 0)):
        super(Car, self).__init__(image, surface, angle, pos)
        self.controller = controller

    def update(self, time):
        acceleration, rotation = self.controller.get_values()
        self.speed -= self.speed * 0.001 * time
        self.speed += acceleration * 0.001 * time
        self.angle -= rotation * self.speed * time
        self.forward(self.speed * time)


#TODO: drawable?
class Spidometer(object):
    def __init__(self, car, screen, front_image, back_image, position, angle_begin, angle_end, speed_max):
        self.car = car
        self.screen = screen
        self.front_image = front_image
        self.back_image = back_image
        self.position = position
        self.angle_begin = angle_begin
        self.angle_end = angle_end
        self.speed_max = speed_max

    def draw(self):
        px = self.position[0]
        py = self.position[1]
        self.screen.blit(self.back_image, (px - self.back_image.get_width() / 2, py - self.back_image.get_height() / 2))
        progress = math.fabs(self.car.speed) / self.speed_max
        if progress > 1:
            progress = 1
        angle = self.angle_begin + (self.angle_end - self.angle_begin) * progress
        rotated = pygame.transform.rotate(self.front_image, -angle)
        self.screen.blit(rotated, (px - rotated.get_width() / 2, py - rotated.get_height() / 2))
