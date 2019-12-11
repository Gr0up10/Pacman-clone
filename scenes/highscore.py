from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.scoreboard import ScoreBoard
from objects.text import Text


class HighscoreScene(Scene):

    def __init__(self, game):
        self.button_menu = Btn(game, (10, game.height - 50, 100, 40), Color.WHITE, 30, 'МЕНЮ', self.set_menu_scene)
        super().__init__(game)

    def create_objects(self):
        self.objects = []
        self.objects.append(self.button_menu)

        sc = ScoreBoard()
        self.objects.append(Text(game=self.game, x=self.game.width/4 - 100, y=20, color=Color.ORANGE, text="МЕСТО"))
        self.objects.append(Text(game=self.game, x=self.game.width/4*2-100, y=20, color=Color.ORANGE, text="ИНИЦИАЛЫ"))
        self.objects.append(Text(game=self.game, x=self.game.width/4*3,     y=20, color=Color.ORANGE, text="СЧЕТ"))
        for i in range(0, 10):
            self.objects.append(Text(game=self.game, x=self.game.width // 4 - 100, y=i * 40 + 80,
                                     text="#"+str(i+1), font_size=50))
            self.objects.append(Text(game=self.game, x=self.game.width // 4 * 2 - 100, y=i * 40 + 80,
                                     text=(sc.get_instance(i)[0]), font_size=50))
            self.objects.append(Text(game=self.game, x=self.game.width // 4 * 3, y=i * 40 + 80,
                                     text=str('{:0>3}'.format(sc.get_instance(i)[1])), font_size=50))

    def set_menu_scene(self):
        from scenes.menu import MenuScene
        self.set_next_scene(MenuScene)
