from constants import Color
from objects.button import Btn
from scenes.base import Scene


class HighscoreScene(Scene):
    '''def __init__(self, game):
        super().__init__(game)
        self.highscore = None'''

    def create_objects(self):
        self.button_menu = Btn(self.game, (10, self.game.height - 50, 100, 40), Color.WHITE, 30, 'МЕНЮ', self.set_menu_scene)
        self.objects = [self.button_menu]



    def set_menu_scene(self):
        self.set_next_scene(0)
