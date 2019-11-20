import pygame
from pysmile.renderer import Renderer


class SceneRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.objects = []

    def render(self, entity, rect):
        print(len(self.objects))
        if len(self.objects) > 0:
            print(self.objects)
            self.objects[0].game.screen = pygame.Surface(*rect.size)
            for obj in self.objects:
                obj.process_draw()
            return self.objects[0].game.screen
        return pygame.Surface(*rect.size)
