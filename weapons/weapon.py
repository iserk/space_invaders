import numpy as np

from objects.position import Position


class Weapon:
    SPEED = 500
    SHOOT_DELAY = 200
    ACCURACY = 0.8

    def __init__(self, vehicle=None):
        self.name = self.__class__.__name__
        self.shot = None
        self.vehicle = vehicle
        self.prev_shot_time = 0

    def can_shoot(self):
        # return self.vehicle.scene.game.total_time - self.prev_shot_time > self.SHOOT_DELAY
        return self.get_charge() >= 1

    def get_charge(self):
        # return (self.vehicle.scene.game.total_time - self.prev_shot_time) / self.SHOOT_DELAY
        return min(1, (self.vehicle.scene.game.total_time - self.prev_shot_time) / self.SHOOT_DELAY)

    def _send_bullet(self, scene, pos, velocity):
        """Sends a single bullet with the given parameters."""
        return self.shot(
            scene, pos,
            velocity + Position((np.random.default_rng().normal() - 0.5) * self.shot.SPEED * (1 - self.ACCURACY), 0)
        )

    def _perform_shot(self, scene, pos, velocity):
        """Performs a single shot with the given parameters."""
        self._send_bullet(scene, pos, velocity)

    def shoot(self, scene, pos, velocity):
        if not self.can_shoot():
            return

        self._perform_shot(scene, pos, velocity)

        self.prev_shot_time = scene.game.total_time

