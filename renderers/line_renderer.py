from pysmile.renderer import Renderer
from OpenGL.GL import *


class LineRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.lines = []

    def render(self, entity, rect):
        glPushMatrix()
        glBegin(GL_LINES)
        for line in self.lines:
            glColor3f(*line[1][:3])
            for i in range(len(line[0])-1):
                glVertex2f(line[0][i].x,   line[0][i].y)
                glVertex2f(line[0][i+1].x, line[0][i+1].y)

        glEnd()
        glPopMatrix()
