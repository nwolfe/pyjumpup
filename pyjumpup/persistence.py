import os
import appdirs
from pyjumpup.settings import *


class Persistence:
    def __init__(self):
        self.directory = appdirs.user_data_dir('pyjumpup', 'python')
        os.makedirs(self.directory, exist_ok=True)

    def load_highscore(self):
        try:
            with open(os.path.join(self.directory, HIGH_SCORE_FILE), 'r') as file:
                return int(file.read())
        except:
            return 0

    def save_highscore(self, highscore):
        with open(os.path.join(self.directory, HIGH_SCORE_FILE), 'w') as file:
            file.write(str(highscore))
