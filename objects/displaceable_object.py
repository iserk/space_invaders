from pygame import Vector2

import utils.time


class DisplaceableObject():
    def __init__(self, pos: Vector2, displacement_pos: Vector2 = Vector2(0, 0), displacement_roll: float = 0):
        self._pos = pos
        self._roll = 0
        self.displacement_pos = displacement_pos
        self.displacement_roll = displacement_roll

    def update(self, dt):
        pass
        self.displacement_pos = Vector2(
            self.displacement_pos[0] * (1 - dt * 10 / utils.time.TIME_UNITS_PER_SECOND),
            self.displacement_pos[1] * (1 - dt * 10 / utils.time.TIME_UNITS_PER_SECOND)
        )
        self.displacement_roll *= (1 - dt * 10 / utils.time.TIME_UNITS_PER_SECOND)

    def reset_position(self):
        self.displacement_pos = Vector2(0, 0)
        self.displacement_roll = 0

    @property
    def pos(self):
        return self._pos + self.displacement_pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def roll(self):
        return self._roll + self.displacement_roll

    @roll.setter
    def roll(self, value):
        self._roll = value

    def displace(self, displacement_pos: Vector2 = Vector2(0, 0), displacement_roll: float = 0):
        self.displacement_pos += displacement_pos
        self.displacement_roll += displacement_roll

    def set_displacement(self, displacement_pos: Vector2 = Vector2(0, 0), displacement_roll: float = 0):
        self.displacement_pos = displacement_pos
        self.displacement_roll = displacement_roll
