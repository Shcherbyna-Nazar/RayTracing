import pygame
import math

from graphics import apply_phong_lighting


class Sphere:
    def __init__(self, center, radius, material):
        self.center = center  # Центр сферы в виде (x, y, z)
        self.radius = radius  # Радиус сферы
        self.material = material  # Материал сферы

    def draw(self, screen, light_source, spheres):
        steps = 100  # Количество шагов для отрисовки
        for i in range(steps):
            theta = 2 * math.pi * i / steps
            for j in range(steps // 2):  # Только верхняя полусфера видима
                phi = math.pi * j / steps
                x = self.radius * math.sin(phi) * math.cos(theta) + self.center[0]
                y = self.radius * math.sin(phi) * math.sin(theta) + self.center[1]
                z = self.radius * math.cos(phi) + self.center[2]

                # Перспективная проекция
                camera_z = 1000
                projection_factor = camera_z / (camera_z - z)
                screen_x = SCREEN_WIDTH / 2 + projection_factor * (x - SCREEN_WIDTH / 2)
                screen_y = SCREEN_HEIGHT / 2 + projection_factor * (y - SCREEN_HEIGHT / 2)

                # Нормаль в данной точке сферы
                normal = (math.sin(phi) * math.cos(theta), math.sin(phi) * math.sin(theta), math.cos(phi))

                # Расчет освещения для точки с учетом возможной тени
                color = self.calculate_lighting(light_source, spheres, (x, y, z), normal)
                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), 2)  # Рисуем маленький круг как точку на сфере

    def calculate_lighting(self, light_source, spheres, point, normal):
        shadow = False
        min_distance = float('inf')
        for sphere in spheres:
            if sphere != self:
                intersects, distance = ray_intersects_sphere(point, light_source.position, sphere.center, sphere.radius)
                if intersects and distance < min_distance:
                    min_distance = distance
                    shadow = True

        if shadow:
            shadow_intensity = min(1, min_distance / 100)  # Уменьшаем интенсивность тени с расстоянием
            return [int(c * shadow_intensity) for c in apply_phong_lighting(self.material, light_source, point, normal)]
        else:
            return apply_phong_lighting(self.material, light_source, point, normal)


def ray_intersects_sphere(origin, light_pos, sphere_center, sphere_radius):
    direction = [light_pos[i] - origin[i] for i in range(3)]
    a = sum(d * d for d in direction)
    oc = [origin[i] - sphere_center[i] for i in range(3)]
    b = 2.0 * sum(oc[i] * direction[i] for i in range(3))
    c = sum(oc[i] * oc[i] for i in range(3)) - sphere_radius ** 2
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return False, None  # Нет пересечения
    else:
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        if t1 > 0 and t2 > 0:
            return True, min(t1, t2)  # Возвращаем расстояние до ближайшей точки пересечения
        return False, None


# Глобальные переменные для ширины и высоты экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
