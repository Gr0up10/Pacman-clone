from pysmile.component import Component
from pysmile.events.update import UpdateEvent


class ObjectUpdate(Component):
    def __init__(self, object):
        self.object = object
        self.entity = None

    def update(self, _):
        self.object.process_logic()

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
