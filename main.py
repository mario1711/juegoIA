import time

import pygame
import random
import Obstacle
import Player
import Enemy
import Mapa
import Battery

TILE_SIZE = 64


def generate_obstacles_and_enemies():
    potions = [Battery.Battery(128, 128),  # arriba-izquierda
               Battery.Battery(768, 128),  # arriba-derecha
               Battery.Battery(448, 448),  # centro
               Battery.Battery(768, 768),  # abajo-derecha
               Battery.Battery(128, 768)]  # abajo-izquierda

    occupied_positions = set()
    for p in potions:
        occupied_positions.add((p.rect.centery // 64, p.rect.centerx // 64))

    obstacles = []
    for _ in range(20):
        while True:
            x, y = random.randint(2, 11), random.randint(2, 11)
            if (x, y) not in occupied_positions and not (5 <= x <= 7 and 5 <= y <= 7):
                occupied_positions.add((x, y))
                obstacle = Obstacle.Obstacle(x * 64, y * 64)
                obstacles.append(obstacle)
                break

    enemies = []
    for _ in range(5):
        while True:
            x, y = random.randint(2, 11), random.randint(2, 11)
            if (x, y) not in occupied_positions and not (5 <= x <= 7 and 5 <= y <= 7):
                if not any(obstacle.rect.collidepoint(x * 64, y * 64) for obstacle in obstacles):
                    occupied_positions.add((x, y))
                    enemy = Enemy.Enemy(x * 64, y * 64)
                    enemies.append(enemy)
                    break

    return obstacles, enemies, potions


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((832, 832))
    pygame.display.set_caption("Juego IA")
    clock = pygame.time.Clock()
    running = True

    mapa = Mapa.Map()
    player = Player.Player(448, 448, 832, 832, mapa)

    obstacles, enemies, potions = generate_obstacles_and_enemies()

    all_enemies_destroyed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not enemies:
            all_enemies_destroyed = True

        if all_enemies_destroyed:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Arial', 50)
            text_surface = font.render("¡Has ganado!", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(5)
            running = False

        pygame.key.set_repeat(1, 250)

        player.update(obstacles, enemies, potions)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the map
        mapa.draw(screen)

        # Draw obstacles
        for i in obstacles:
            i.draw(screen)

        # Draw enemies
        for i in enemies:
            i.draw(screen)

        # Draw player
        player.draw(screen)

        for p in potions:
            p.draw(screen)

        # Draw score
        my_font = pygame.font.SysFont('Arial', 30)
        text_surface = my_font.render(f'Puntuacion: {player.get_score()}', False, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        state = my_font.render(f'State: {player.get_state()}', False, (255, 255, 255))
        screen.blit(state, (500, 10))

        energy = my_font.render(f'Energy: {player.get_batery()}', False, (255, 255, 255))
        screen.blit(energy, (10, 792))

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


if __name__ == "__main__":
    main()
