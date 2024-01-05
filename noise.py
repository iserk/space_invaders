import math
import random


def perlin_noise(x):
    # Basic Perlin noise function for demonstration
    return math.sin(x)


def fractal_noise(x, octaves=10, persistence=0.8):
    total = 0
    frequency = 1
    amplitude = 1
    max_value = 0
    for i in range(octaves):
        total += perlin_noise(x * frequency) * amplitude

        max_value += amplitude
        amplitude *= persistence
        frequency *= 2

    return total / max_value


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # print(fractal_noise(0.5))
    # plot fractal noise

    x = [i for i in range(1000)]
    y = [fractal_noise(i / 100) for i in x]
    # y = [random.uniform(-1, 1) for i in x]
    plt.plot(x, y)
    plt.show()
#
# # # Example usage
# # x_value = 10
# # noise_value = fractal_noise(x_value)
# # print("Fractal Noise for x =", x_value, "is", noise_value)
