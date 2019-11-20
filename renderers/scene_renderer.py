import pygame
from pysmile.renderer import PyGameRenderer


class SceneRenderer(PyGameRenderer):
    def __init__(self):
        super().__init__()
        self.objects = []

    def set_objects(self, objs):
        self.objects = objs
        self.need_redraw = True

    def render(self, entity, rect):
        if len(self.objects) > 0:
            self.objects[0].game.screen = pygame.Surface(rect.size)
            for obj in self.objects:
                obj.process_draw()
            return self.objects[0].game.screen
        return pygame.Surface(rect.size)
