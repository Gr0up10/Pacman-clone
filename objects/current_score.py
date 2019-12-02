import pygame
from pysmile.colors import Colors
from objects.text import Text

from objects.base import DrawObject


class CurrentScore(DrawObject):

    def __init__(self, game, x=200, y=20):
        super().__init__(game)

        self.text = Text(game=game, text="0", font_size=50, color=Colors.white, font_name="assets/fonts/Emulogic.ttf", x=x, y=y)

    def process_draw(self):
        self.text.process_draw()

    # Дефолтное поведение - рандомные направления
    def process_logic(self):
        pass

    def update(self, points):
        self.text.update_text(str(points))