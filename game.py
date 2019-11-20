import pygame
from pysmile.game import Game as PSGame

from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.base import Scene
from pysmile.components.exit_on_escape import ExitOnEscape
from pysmile.component import Component


class Game(PSGame):
    """
    DEPRECATED
    new usage:
    current_scene = SceneClass

    example:
    current_scene = MainScene
    """
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    HIGHSCORE_SCENE_INDEX = 3

    def __init__(self, width=800, height=600):
        super().__init__()

        self.screen = None
        pygame.init()

        self.setup_default_components((width, height))
        self.add_component(ExitOnEscape())

        self.scenes = [MenuScene(self), MainScene(self), FinalScene(self)]

        self.current_scene = MenuScene

    def __setattr__(self, key, value):
        if key == "current_scene":
            if isinstance(self.scene, Scene):
                self.scene.removed()

            if isinstance(value, int):
                print("current_scene = index is deprecated, use current_scene = SceneClass, " +
                      "for example current_scene = MenuScene")
                self.scene = self.scenes[value]
            else:
                self.scene = value(self)

            self.scene.bind_events()
            for comp in self.get_components(Component):
                print(comp)
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
