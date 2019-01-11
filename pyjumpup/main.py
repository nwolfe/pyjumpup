# Jumpy! - platform game

import pygame as pg
from pyjumpup.settings import *
from pyjumpup.sprites import *


class Game:
    def __init__(self):
        # Initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False

        # Game variables; see #new()
        self.all_sprites = None
        self.platforms = None
        self.player = None

    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for platform in PLATFORMS:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        # Check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                # for dev purposes; remove later
                if event.key == pg.K_ESCAPE:
                    self.playing = self.running = False

    def draw(self):
        # Game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        # Game splash/start screen
        pass

    def show_game_over_screen(self):
        # Game over/continue
        pass


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_game_over_screen()

pg.quit()
