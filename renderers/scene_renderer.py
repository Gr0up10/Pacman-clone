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
        screen = pygame.Surface(rect.size)
        screen.set_colorkey((0, 0, 0))
        screen.fill((0, 0, 0, 0))
        if len(self.objects) > 0:
            self.objects[0].game.screen = screen

            for obj in self.objects:
                obj.process_draw()

            return screen
        return screen
