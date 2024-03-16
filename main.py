import pygame
import random
import Mapa
import Obstacle
import Player
import Enemy

# Definir el tamaño de los azulejos
TILE_SIZE = 64


# Función para generar obstáculos y enemigos
def generate_obstacles_and_enemies():
    occupied_positions = set()
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
    # ------------------------->
    print("Obstáculos generados:")
    for obstacle in obstacles:
        print(obstacle.rect.x, obstacle.rect.y)

    print("Enemigos generados:")
    for enemy in enemies:
        print(enemy.rect.x, enemy.rect.y)
    # ------------------------->
    return obstacles, enemies


# Función principal del juego
def main():
    # Inicializar pygame
    pygame.init()
    pygame.mixer.init()

    # Configurar la pantalla
    screen = pygame.display.set_mode((832, 832))
    pygame.display.set_caption("Juego IA")
    clock = pygame.time.Clock()
    running = True

    # Crear instancias de mapa, jugador, obstáculos y enemigos
    mapa = Mapa.Mapa()
    player = Player.Player(416, 416, 832, 832, mapa)
    obstacles, enemies = generate_obstacles_and_enemies()

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
            continue

        pygame.key.set_repeat(1, 250)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the map
        mapa.draw(screen)

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw player
        player.draw(screen)
        player.update(obstacles, enemies)

        # Draw score
        my_font = pygame.font.SysFont('Arial', 30)
        text_surface = my_font.render(f'Puntuacion: {player.get_score()}', False, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        print("Player position:", (player.rect.x // TILE_SIZE, player.rect.y // TILE_SIZE))
        closest_enemy = player.find_closest_enemy(enemies)
        print("Closest enemy:", closest_enemy)
        if closest_enemy:
            print("Enemy position:", (closest_enemy.rect.x // TILE_SIZE, closest_enemy.rect.y // TILE_SIZE))

        pygame.display.flip()
        clock.tick(2)

    pygame.quit()


# Verificar si este archivo es el programa principal y ejecutar la función principal
if __name__ == "__main__":
    main()
