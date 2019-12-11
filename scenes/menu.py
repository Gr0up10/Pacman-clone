from pysmile.components.animation import AnimationComponent
from pysmile.components.renderer import RendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.renderers.image_renderer import ImageRenderer

from constants import Color
from objects.button import Btn
from scenes.base import Scene
from scenes.highscore import HighscoreScene

from pysmile.entity import Entity
from pysmile.math.vector2 import Vector2
from pysmile.gl.shader import Shader


class MenuScene(Scene):
    def __init__(self,game, blur=6, stblur=0.1, endbl=4,
                 x=406, y=255, dist=100,l=200, font=40 ):
        self.entity = None
        self.blur = blur
        self.stepbl = stblur
        self.endbl = endbl
        self.go = False
        self.backgr = True

        self.x=x
        self.y=y
        self.dist=dist
        self.l = l
        self.h = self.dist - 20
        self.font = font
        super().__init__(game)


    def create_objects(self):
        self.button_start = Btn(self.game, (self.x, self.y + self.dist*0, self.l, self.h), Color.WHITE, self.font, "Запуск игры", self.Blured)
        self.button_highscore = Btn(self.game, (self.x, self.y + self.dist, self.l, self.h), Color.WHITE, self.font, 'Highscores', self.highscore)
        self.button_exit = Btn(self.game, (self.x, self.y + self.dist*2, self.l, self.h), Color.WHITE, self.font, 'Выход', self.exit)
        self.objects = [self.button_start, self.button_exit, self.button_highscore]


    def Blured(self):
        image_back=Entity()
        self.add_entity(image_back)
        image_back.add_component(TransformComponent(Vector2(0, 0)))
        shader = Shader.init_from_files("assets/shaders/blur/blur.vert", "assets/shaders/blur/blur.frag")
        shader.inject_rect = True
        shader.uniform_alpha = 1.0
        image_back.add_component(RendererComponent(ImageRenderer("/home/prom/PycharmProjects/pacman/assets/images/background.png"), self.game.screen_size, shader))
        image_back.add_component(AnimationComponent(step=self.stepbl, end=self.endbl, function=lambda x: shader.set_uniform("alpha", 10.0-x-self.blur), completion = self.next))



    def next(self):
        from scenes.main import MainScene
        self.set_next_scene(MainScene)


    def exit(self):
        self.game.exit()

    def highscore(self):
        self.set_next_scene(HighscoreScene)










