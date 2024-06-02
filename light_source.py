import pygame


class LightSource:
    def __init__(self, position, color, intensity, radius):
        self.position = list(position)  # [x, y, z]
        self.color = color
        self.intensity = intensity
        self.radius = radius

    def draw(self, screen):
        # Расчет цвета с учетом интенсивности
        intensity_color = [min(255, int(self.color[i] * self.intensity)) for i in range(3)]
        pygame.draw.circle(screen, intensity_color, (int(self.position[0]), int(self.position[1])), self.radius)
