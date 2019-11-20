from objects.ghost_base import GhostBase
from scenes.base import Scene
from objects.field import Field
from objects.grain import Grain


class MainScene(Scene):
    def create_objects(self):
        self.objects.append(Field(self.game, 32))
        self.objects.append(GhostBase(self.game))
        self.objects.append(Grain(self.game))
