# Sprite classes for platform game

import pygame as pg
from pyjumpup.settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)

    def update(self):
        self.acc = pg.math.Vector2(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACCELERATION

        # apply friction
        self.acc.x += self.vel.x * -PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

