import pygame
import os
from settings import SOUNDS_DIR

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self._load_sounds()

    def _load_sounds(self):
        sound_files = {
            'move': 'move.wav',
            'capture': 'capture.wav',
            'promote': 'promote.wav',
            'check': 'check.wav',
            'game_end': 'game_end.wav'
        }
        for name, filename in sound_files.items():
            path = os.path.join(SOUNDS_DIR, filename)
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except (FileNotFoundError, pygame.error):
                print(f"Sound not found: {path}. Continuing without sound.")
                self.sounds[name] = None

    def play(self, name):
        if self.enabled and self.sounds.get(name):
            self.sounds[name].play()

    def toggle(self):
        self.enabled = not self.enabled