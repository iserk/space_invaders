import pygame


def draw_health_bar(surface, x, y, width, height, color, value, max_value, value_threshold=0):
    # Draw a green bar above the invader to indicate its health
    if max_value > 10:
        pygame.draw.rect(
            surface,
            color,
            (
                x + 1,
                y - 10,
                width * value / max_value - 2,
                2,
            )
        )
    elif max_value > value_threshold:
        for i in range(round(value)):
            pygame.draw.rect(
                surface,
                color,
                (
                    x + i * width / max_value + 1,
                    y - 10,
                    width / max_value - 2,
                    2,
                )
            )


def draw_stats(vehicle, camera):
    # draw_health_bar(surface, x, y, width, height, color, value, max_value, value_threshold=0)
    draw_health_bar(
        camera.screen,
        vehicle.pos.x - vehicle.sprite.width / 2,
        vehicle.pos.y - vehicle.sprite.height / 2,
        vehicle.sprite.width,
        2,
        (0, 255, 0),
        value=vehicle.hit_points,
        max_value=vehicle.MAX_HIT_POINTS,
        value_threshold=1
    )
    draw_health_bar(
        camera.screen,
        vehicle.pos.x - vehicle.sprite.width / 2,
        vehicle.pos.y - vehicle.sprite.height / 2 - 4,
        vehicle.sprite.width,
        2,
        (160, 160, 160),
        vehicle.armor,
        vehicle.MAX_ARMOR
    )
    draw_health_bar(
        camera.screen,
        vehicle.pos.x - vehicle.sprite.width / 2,
        vehicle.pos.y - vehicle.sprite.height / 2 - 8,
        vehicle.sprite.width,
        2,
        (0, 128, 255),
        vehicle.shield, vehicle.MAX_SHIELD
    )