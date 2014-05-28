import pygame
import math
from pygame.locals import *

from input import Joystick, Keyboard
from objects import Car, Spidometer

#TODO: angle mod?
#TODO: blit_center?
#drawable
#updatable

import os
position = 5, 5
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

RED = pygame.Color(127, 0, 0)
BLUE = pygame.Color(0, 0, 127)
GREEN = pygame.Color(0, 127, 0)
BLACK = pygame.Color(0, 0, 0)

# try:
carImage = pygame.image.load('data/car.png')
indicatorImage = pygame.image.load('data/indicator.png')
speedImage = pygame.image.load('data/speed.png')#TODO: rename
# except pygame.error as e:
    # print 'ERROR', e

pygame.joystick.init()



class Game(object):
    screen = None

    car = None
    spidometer = None

    lastPos = None

    running = True

    def stop(self):
        self.running = False

    def loop(self):
        timeLast = pygame.time.get_ticks()
        while self.running:
            map(self.handle_event, pygame.event.get())
            self.screen.fill(BLACK)
            self.car.draw()

            timeNow = pygame.time.get_ticks()
            delta = timeNow - timeLast
            timeLast = timeNow

            self.car.update(delta)

            self.spidometer.draw()

            pygame.display.update()
            self.fpsClock.tick(60)

    def handle_event(self, event):
        print event
        if event.type == QUIT:
            self.stop()
        elif event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                self.stop()
        elif event.type == MOUSEMOTION:
            pos = event.pos
            buttons = event.buttons
            if buttons[0] or buttons[1] or buttons[2]:
                if self.lastPos != None:
                    color = pygame.Color(buttons[0] * 127, buttons[1] * 127, buttons[2] * 127)
                    pygame.draw.line(self.screen, color, self.lastPos, pos)
                    pos = event.pos
            self.lastPos = pos
        elif event.type == JOYBUTTONDOWN:
            button = event.button
            if button == 7:
                self.stop()


    def run(self):
        pygame.init()
        pygame.display.set_caption('THE game')
        self.fpsClock = pygame.time.Clock()


        # resolution = (640, 480)
        # fullscreen = True
        resolution = (800, 900)
        fullscreen = False

        flags = 0
        if fullscreen:
            flags |= FULLSCREEN | HWSURFACE
            modes = pygame.display.list_modes()
            if len(modes) > 0:
                resolution = modes[0]
            else:
                raise Exception()
        flags = FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode(resolution, flags)


        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            controller = Joystick(pygame.joystick.Joystick(0))
        else:
            controller = Keyboard()

        self.car = Car(controller, carImage, self.screen, 0, (100, 100))

        sx = self.screen.get_width() - speedImage.get_width() / 2 - 50
        sy = self.screen.get_height() - speedImage.get_height() / 2 - 50
        self.spidometer = Spidometer(self.car, self.screen, indicatorImage, speedImage, (sx, sy), -45, 225, 1.5)


        self.loop()
        pygame.joystick.quit()
        pygame.quit()
