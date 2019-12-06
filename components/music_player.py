import pygame
from pysmile.component import Component
from pysmile.events.update import UpdateEvent

from events.play_sound import PlaySoundEvent


class MusicPlayerComponent(Component):
    def __init__(self):
        super().__init__()
        self.entity = None
        self.pause_after = None
        self.pause_song = None

    def play(self, event):
        self.pause_after = event.pause_after
        if self.pause_song == event.sound:
            pygame.mixer_music.unpause()
            return

        pygame.mixer_music.load(event.sound)
        pygame.mixer_music.play(event.count)
        if self.pause_after:
            self.pause_song = event.sound

        print(pygame.mixer_music.get_busy())

    def update(self, _):
        if self.pause_after and self.pause_after != 0:
            self.pause_after -= 1
            if self.pause_after <= 0:
                pygame.mixer_music.pause()
                self.pause_after = 0

    def removed(self):
        self.entity.event_manager.bind(PlaySoundEvent, self.play)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(PlaySoundEvent, self.play)
        entity.event_manager.bind(UpdateEvent, self.update)
