import math
import pygame
from pygame.locals import *

class Controller(object):
    def get_values(self):
        self.prepare()
        #TODO: validate values
        return (self.get_acceleration(), self.get_rotation())

    def prepare(self):
        pass

    def get_acceleration(self):
        raise NotImplementedError

    def get_rotation(self):
        raise NotImplementedError


class Joystick(Controller):
    ROTATION_DEADZONE = 0#0.05
    ACCELERATION_DEADZONE = 0

    def __init__(self, joystick):
        self.joystick = joystick
        joystick.init()

    def get_acceleration(self):
        value = self.joystick.get_axis(2)
        if math.fabs(value) < self.ACCELERATION_DEADZONE:
            value = 0
        return value

    def get_rotation(self):
        value = self.joystick.get_axis(0)
        if math.fabs(value) < self.ROTATION_DEADZONE:
            value = 0
        return value * 0.5


#TODO: rotation value increasing while holding down the key
#TODO: ticks
class Keyboard(Controller):
    rotation = 0

    ROTATION_SPEED = 0.05
    ROTATION_RETURN_SPEED = 0.1

    def prepare(self):
        self.keys = pygame.key.get_pressed()

    def get_rotation(self):
        value = 0
        if self.keys[K_a]:
            value -= 1
        if self.keys[K_d]:
            value += 1
        print 'keyboard', value, self.rotation
        r_abs = math.fabs(self.rotation)
        if value == 0:
            step = min(self.ROTATION_RETURN_SPEED, r_abs) * (1 if self.rotation > 0 else -1) #TODO: sign
            self.rotation -= step
        elif (self.rotation < 0 and value > 0) or (self.rotation > 0 and value < 0):
            self.rotation = 0
        else:
            self.rotation += value * self.ROTATION_SPEED
            r_abs = math.fabs(self.rotation)
            if r_abs > 1:
                self.rotation /= r_abs
        return self.rotation

    def get_acceleration(self):
        value = 0
        if self.keys[K_w]:
            value += 1
        if self.keys[K_s]:
            value -= 1
        return value
