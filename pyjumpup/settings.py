# game options/settings
TITLE = 'Jump Up!'
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HIGH_SCORE_FILE = 'highscore.txt'
SPRITESHEET_FILE = 'spritesheet_jumper.png'
VOLUME_JUMP = 0.4
VOLUME_BACKGROUND = 1.0
VOLUME_MENU = 0.3
VOLUME_GAMEOVER = 0.3
VOLUME_BOOST = 1.0

# Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = 0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20

# Game properties
BOOST_POWER = 60
POWERUP_SPAWN_PERCENTAGE = 7

# Starting platforms
PLATFORMS = [
    (0, HEIGHT - 60),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4),
    (125, HEIGHT - 350),
    (350, 200),
    (175, 100)
]

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
