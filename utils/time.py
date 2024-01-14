import time
import math

import pygame

from settings import TIME_UNITS_PER_SECOND


def get_time():
    # return pygame.time.get_ticks()
    return time.time() * TIME_UNITS_PER_SECOND


prev_time = get_time()


def get_delta_time():
    global prev_time
    delta = get_time() - prev_time
    prev_time = get_time()
    return delta

