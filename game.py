import pygame
from pysmile.game import Game as PSGame

from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.base import Scene
from scenes.highscore import HighscoreScene
from pysmile.components.exit_on_escape import ExitOnEscape
from pysmile.component import Component


class Game(PSGame):
    """
    DEPRECATED and will be removed soon
    new usage:
    current_scene = SceneClass

    example:
    current_scene = MainScene
    """
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    HIGHSCORE_SCENE_INDEX = 2

    def __init__(self, width=800, height=600):
        pygame.init()
        super().__init__()

        self.screen = None
        self.setup_default_components((width, height))
        self.current_scene = MenuScene
        self.add_component(ExitOnEscape())
        self.scenes = [MenuScene(self), MainScene(self), HighscoreScene(self)]

    def __setattr__(self, key, value):
        if key == "current_scene":
            if isinstance(self.scene, Scene):
                self.scene.removed()

            if isinstance(value, int):
                print("current_scene = "+str(value) +
                      " is deprecated and will be removed soon, use current_scene = " +
                      self.scenes[value].__class__.__name__)
                self.scene = self.scenes[value]
            else:
                self.scene = value(self)

            self.scene.bind_events()
            for comp in self.get_components(Component):
                comp.scene = self.scene
        else:
            object.__setattr__(self, key, value)

    def main_loop(self):
        self.run()

    @property
    def width(self):
        return self.screen_size[0]

    @property
    def height(self):
        return self.screen_size[1]
