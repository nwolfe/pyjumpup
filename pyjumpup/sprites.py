# Sprite classes for platform game

import pygame as pg
from pyjumpup.settings import *


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)

    def update(self):
        self.acc = pg.math.Vector2(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACCELERATION

        # apply friction
        self.acc += self.vel * -PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.center = self.pos