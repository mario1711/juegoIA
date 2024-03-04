import pygame

import Obstacle
import Player
import Enemy
import random
import Mapa


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((832, 832))
    pygame.display.set_caption("Juego IA")
    clock = pygame.time.Clock()
    running = True

    player = Player.Player(screen.get_width() / 2, screen.get_height() / 2, 832, 832)
    mapa = Mapa.Mapa()

    obstacles = []
    occupied_positions = set()  # Para mantener un registro de las posiciones ocupadas por los obstáculos

    for _ in range(20):
        # Generar una nueva posición aleatoria hasta encontrar una que no esté ocupada
        while True:
            x, y = random.randint(2, 11), random.randint(2, 11)
            if (x, y) not in occupied_positions and not (5 <= x <= 7 and 5 <= y <= 7):
                occupied_positions.add((x, y))  # Registrar la nueva posición como ocupada
                obstacle = Obstacle.Obstacle(x * 64, y * 64)
                obstacles.append(obstacle)
                break

    # Generar posiciones de enemigos
    enemies = []

    for _ in range(5):
        while True:
            x, y = random.randint(2, 11), random.randint(2, 11)
            if (x, y) not in occupied_positions and not (5 <= x <= 7 and 5 <= y <= 7):
                occupied_positions.add((x, y))
                enemy = Enemy.Enemy(x * 64, y * 64)
                enemies.append(enemy)
                break

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.key.set_repeat(1, 250)

        keys = pygame.key.get_pressed()
        screen.fill((255, 255, 255))
        mapa.draw(screen)
        player.update(keys, obstacles, enemies)
        player.draw(screen)
        my_font = pygame.font.SysFont('Arial', 30)
        text_surface = my_font.render(f'Puntuacion: {player.get_score()}', False, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        for i in obstacles:
            i.draw(screen)

        for i in enemies:
            i.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
