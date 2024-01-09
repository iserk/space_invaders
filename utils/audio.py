import pygame

import settings


def sound(path, volume=1, abs_volume=None):
    snd = pygame.mixer.Sound(path)
    snd.set_volume(abs_volume if abs_volume is not None else settings.SFX_VOLUME * settings.MASTER_VOLUME * volume)
    return snd


def music(path, volume=1, abs_volume=None):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(abs_volume if abs_volume is not None else settings.MUSIC_VOLUME * settings.MASTER_VOLUME * volume)
    return pygame.mixer.music