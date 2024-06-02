import pygame
import sys
from sphere import Sphere
from material import Material
from light_source import LightSource
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class LabeledSphere(Sphere):
    """Klasa rozszerzająca Sphere o funkcję podpisu."""
    def __init__(self, center, radius, material, label):
        super().__init__(center, radius, material)
        self.label = label

    def draw(self, screen, light_source, spheres, font):
        super().draw(screen, light_source, spheres)
        label_surface = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.center[0] - self.radius, self.center[1] + self.radius + 10))

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Definicja materiałów
    materials = [
        Material((30, 30, 30), (255, 0, 0), (255, 255, 255), 800),  # Металл красный
        Material((20, 20, 20), (0, 200, 0), (60, 60, 60), 30),  # Гума зеленая
        Material((30, 30, 30), (0, 0, 255), (150, 150, 200), 100),  # Пластик синий
        Material((20, 20, 20), (255, 255, 0), (50, 50, 50), 5)  # Дерево желтое
    ]

    # Tworzenie sfer z etykietami
    spheres = [
        LabeledSphere((200, 300, 0), 100, materials[0], "Metal czerwony"),
        LabeledSphere((450, 300, 0), 100, materials[1], "Guma zielona"),
        LabeledSphere((700, 300, 0), 100, materials[2], "Plastik niebieski"),
        LabeledSphere((950, 300, 0), 100, materials[3], "Drewno żółte")
    ]

    light = LightSource((400, 100, 100), (255, 255, 255), 1.0, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    light.intensity = min(light.intensity + 0.1, 2.0)  # Увеличиваем интенсивność
                elif event.key == pygame.K_DOWN:
                    light.intensity = max(light.intensity - 0.1, 0.1)  # Уменьшаем интенсивność
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    light.position = list(pygame.mouse.get_pos()) + [100]

        screen.fill((0, 0, 0))
        light.draw(screen)
        for sphere in spheres:
            sphere.draw(screen, light, spheres, font)

        # Wyświetlenie informacji
        info_text = f"Light Intensity: {light.intensity:.1f}, Position: {light.position[0]}, {light.position[1]}"
        text_surface = font.render(info_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run_game()
