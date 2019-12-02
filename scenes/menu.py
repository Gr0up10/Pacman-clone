from constants import Color
from objects.button import Btn
from scenes.base import Scene
from scenes.main import MainScene
from scenes.highscore import HighscoreScene


class MenuScene(Scene):
    def create_objects(self):
        self.button_start = Btn(self.game, (350, 255, 100, 40), Color.WHITE, 20, "Запуск игры", self.set_main_scene)
        self.button_highscore = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 25, 'Highscores', self.highscore)
        self.button_exit = Btn(self.game, (350, 355, 100, 40), Color.WHITE, 30, 'Выход', self.exit)
        self.objects = [self.button_start, self.button_exit, self.button_highscore]

    def set_main_scene(self):
        self.set_next_scene(MainScene)

    def exit(self):
        self.game.exit()

    def highscore(self):
        self.set_next_scene(HighscoreScene)
