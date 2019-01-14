# Jumpy! - platform game
#
# Credits:
# - Art from Kenney.nl
# - Happy Tune by http://opengameart.org/users/syncopika
# - Yippee by http://opengameart.org/users/snabisch

import pygame as pg
from pyjumpup.settings import *
from pyjumpup.sprites import *
import random
import os


RESOURCE_DIR = os.path.join(os.getcwd(), '..', 'resources')
IMG_DIR = os.path.join(RESOURCE_DIR, 'img')
SND_DIR = os.path.join(RESOURCE_DIR, 'snd')


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
        self.font_name = pg.font.match_font(FONT_NAME)

        # Game variables; see #new()
        self.all_sprites = None
        self.powerups = None
        self.platforms = None
        self.mobs = None
        self.player = None
        self.score = None
        self.highscore = None
        self.mob_timer = None

        # High score persistence, resources
        self.directory = None
        self.spritesheet = None
        self.jump_sound = None
        self.boost_sound = None
        self.load_data()

    def load_data(self):
        # load high score file
        self.directory = os.getcwd()
        try:
            with open(os.path.join(self.directory, HIGH_SCORE_FILE), 'r') as file:
                self.highscore = int(file.read())
        except:
            self.highscore = 0

        # load spritesheet image
        self.spritesheet = Spritesheet(os.path.join(IMG_DIR, SPRITESHEET_FILE))
        # load sounds
        self.jump_sound = pg.mixer.Sound(os.path.join(SND_DIR, 'Jump33.wav'))
        self.jump_sound.set_volume(VOLUME_JUMP)
        self.boost_sound = pg.mixer.Sound(os.path.join(SND_DIR, 'Boost16.wav'))
        self.boost_sound.set_volume(VOLUME_BOOST)

    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        for platform in PLATFORMS:
            Platform(self, *platform)
        pg.mixer_music.load(os.path.join(SND_DIR, 'HappyTune.ogg'))
        pg.mixer_music.set_volume(VOLUME_BACKGROUND)
        self.mob_timer = 0
        self.run()

    def run(self):
        # Game loop
        pg.mixer_music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer_music.fadeout(500)

    def update(self):
        # Game loop - update
        self.all_sprites.update()

        # Spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_FREQUENCY + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # Hit a mob?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False

        # Check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # Only snap to the *lowest* platform
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # Only snap to top if majority of body is above platform (horizontal)
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    # Only snap to top if *feet* are higher than middle of platform (vertical)
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False

        # Scroll when player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(4, abs(self.player.vel.y))
            for mob in self.mobs:
                mob.rect.y += max(4, abs(self.player.vel.y))
            for platform in self.platforms:
                platform.rect.y += max(4, abs(self.player.vel.y))
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.score += 10

        # Player hits a powerup
        powerup_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = - BOOST_POWER
                self.player.jumping = False

        # Fall to your death!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False

        # Spawn new platforms to keep some average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30))

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
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # Game splash/start screen
        pg.mixer_music.load(os.path.join(SND_DIR, 'Yippee.ogg'))
        pg.mixer_music.set_volume(VOLUME_MENU)
        pg.mixer_music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Arrows to move, Space to jump', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press any key to play', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: %s" % self.highscore, 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_keypress()
        pg.mixer_music.fadeout(500)

    def show_game_over_screen(self):
        # Game over/continue
        if not self.running:
            return
        pg.mixer_music.load(os.path.join(SND_DIR, 'Yippee.ogg'))
        pg.mixer_music.set_volume(VOLUME_GAMEOVER)
        pg.mixer_music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text('GAME OVER', 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: %s" % self.score, 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press any key to play again', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('NEW HIGH SCORE!', 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(os.path.join(self.directory, HIGH_SCORE_FILE), 'w') as file:
                file.write(str(self.highscore))
        else:
            self.draw_text("High Score: %s" % self.highscore, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_keypress()
        pg.mixer_music.fadeout(500)

    def wait_for_keypress(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    # For dev-only; remove later
                    if event.key == pg.K_ESCAPE:
                        self.playing = self.running = False
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_game_over_screen()

pg.quit()
