from pysmile.renderer import Renderer
from OpenGL.GL import *


class LineRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.line = None

    def render(self, entity, rect):
        if self.line and len(self.line) >= 2:
            glPushMatrix()
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)
            for i in range(len(self.line)-1):
                glVertex2f(self.line[i].x, self.line[i].y)
                glVertex2f(self.line[i+1].x, self.line[i+1].y)

            glEnd()
            glPopMatrix()
