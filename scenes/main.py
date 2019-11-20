from objects.ghost_base import GhostBase
from scenes.base import Scene
from objects.grain import Grain


class MainScene(Scene):
    def create_objects(self):
        self.objects.append(GhostBase(self.game))
        self.objects.append(Grain(self.game))
