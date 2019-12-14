from pysmile.component import Component
from pysmile.components.renderer import RendererComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2
from pysmile.renderer import Renderer

from events.debug_line import DrawDebugLineEvent


class LineHandlerComponent(Component):
    def __init__(self):
        self.entity = None
        self.lines = 0

    def draw_line(self, event):
        line_rend = self.entity.get_component(RendererComponent).renderer
        lines = line_rend.lines
        for i in range(len(lines)):
            if lines[i][1] == event.color:
                lines[i] = (event.line, lines[i][1])
                return

        lines.append((event.line, event.color))

    def applied_on_entity(self, entity):
        self.entity = entity
        self.entity.event_manager.bind(DrawDebugLineEvent, self.draw_line)

    def removed(self):
        self.entity.event_manager.unbind(DrawDebugLineEvent, self.draw_line)
