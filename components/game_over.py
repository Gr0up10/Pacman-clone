from pysmile.component import Component
from scenes.menu import MenuScene


class GameOverComponent(Component):
    def __init__(self):
        super().__init__()
        self.entity = None
        self.grains_count = 0
        self.max_grains_count = 0

    def collect_grain(self):
        self.grains_count += 1
        if self.grains_count >= self.max_grains_count:
            self.entity.current_scene = MenuScene