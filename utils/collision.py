import pygame


def subtract_vectors(v1, v2):
    return pygame.Vector2(v1.x, v1.y) - pygame.Vector2(v2.x, v2.y)


def dot_product(v1, v2):
    return pygame.Vector2(v1.x, v1.y).dot(pygame.Vector2(v2.x, v2.y))


def normalize_vector(v):
    return pygame.Vector2(v.x, v.y).normalize() if v.length() > 0 else v


def perpendicular_vector(v):
    return pygame.Vector2(-v[1], v[0])


def project_polygon(axis, polygon):
    if not polygon:  # Check if the polygon list is empty
        return 0, 0  # Return a default value, or handle as appropriate

    initial_projection = dot_product(axis, polygon[0])
    min_proj = initial_projection
    max_proj = initial_projection
    for vertex in polygon:
        projection = dot_product(axis, vertex)
        min_proj = min(min_proj, projection)
        max_proj = max(max_proj, projection)
    return min_proj, max_proj


def overlap_intervals(interval1, interval2):
    return max(interval1[0], interval2[0]) <= min(interval1[1], interval2[1])


def sat_collision_check(poly1, poly2):
    for poly in [poly1, poly2]:
        for i in range(len(poly)):
            edge = subtract_vectors(poly[i], poly[(i + 1) % len(poly)])
            normal = normalize_vector(perpendicular_vector(edge))

            projection1 = project_polygon(normal, poly1)
            projection2 = project_polygon(normal, poly2)

            if not overlap_intervals(projection1, projection2):
                return False  # No collision
    return True  # Collision detected
