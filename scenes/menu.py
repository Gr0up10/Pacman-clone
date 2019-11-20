from constants import Color
from objects.button import Btn
from scenes.base import Scene


class MenuScene(Scene):
    def create_objects(self):
        self.button_start = Btn(self.game, (350, 255, 100, 40), Color.WHITE, "Запуск игры", self.set_main_scene)
        self.button_highscore = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Highscores', self.highscore)
        self.button_exit = Btn(self.game, (350, 355, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.button_start, self.button_exit, self.button_highscore]

    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True

    def highscore(self):
        self.set_next_scene(self.game.HIGHSCORE_SCENE_INDEX)
