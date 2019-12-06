class PlaySoundEvent:
    def __init__(self, sound, count=0, pause_after=None):
        self.sound = sound
        self.pause_after = pause_after
        self.count = count
