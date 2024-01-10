import pygame


def draw_health_bar(surface, x, y, width, height, color, value, max_value, value_threshold=0):
    # Draw a green bar above the invader to indicate its health
    if max_value > 10:
        pygame.draw.rect(
            surface,
            color,
            (
                x,
                y - 10,
                width * value / max_value,
                2,
            )
        )
    elif max_value > value_threshold:
        for i in range(value):
            pygame.draw.rect(
                surface,
                color,
                (
                    x + i * width / max_value + 2,
                    y - 10,
                    width / max_value - 2,
                    2,
                )
            )
