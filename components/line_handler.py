from pysmile.component import Component
from pysmile.components.renderer import RendererComponent
from pysmile.math.vector2 import Vector2
from pysmile.renderer import Renderer

from events.debug_line import DrawDebugLineEvent


class LineHandlerComponent(Component):
    def __init__(self):
        self.entity = None

    def draw_line(self, event):
        line_rend = self.entity.get_component(RendererComponent).renderer
        line_rend.line = event.line

    def applied_on_entity(self, entity):
        self.entity = entity
        self.entity.event_manager.bind(DrawDebugLineEvent, self.draw_line)

    def removed(self):
        self.entity.event_manager.unbind(DrawDebugLineEvent, self.draw_line)