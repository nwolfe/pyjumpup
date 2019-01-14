# Sprite classes for platform game

import random
import pygame as pg
from pyjumpup.settings import *


# Utility class for loading and parsing spritesheets
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        image.set_colorkey(BLACK)
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.pos = pg.math.Vector2(40, HEIGHT - 100)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.standing_frames = None
        self.walk_frames_r = None
        self.walk_frames_l = None
        self.jump_frame = None
        self._load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def _load_images(self):
        # bunny1_ready.png, bunny1_stand.png
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        # bunny1_walk1.png, bunny1_walk2.png
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        # bunny1_jump.png
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)

    def update(self):
        self.animate()
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
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + (0.5 * self.acc)
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
        self.rect.midbottom = self.pos

    def animate(self):
        self.walking = self.vel.x != 0
        now = pg.time.get_ticks()
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        elif not self.jumping:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.platforms)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < POWERUP_SPAWN_PERCENTAGE:
            Powerup(self.game, self)


class Powerup(pg.sprite.Sprite):
    def __init__(self, game, platform):
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.powerups)
        self.game = game
        self.platform = platform
        self.type = random.choice(['boost'])
        # powerup_jetpack.png
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        # Keep the powerup on top of the platform in case it moves
        self.rect.bottom = self.platform.rect.top - 5
        if not self.game.platforms.has(self.platform):
            self.kill()
