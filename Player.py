import time
import pygame
import os
import heapq

TILE_SIZE = 64
MOVE_DELAY = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height, game_map):
        super().__init__()
        self.sprite_dir = os.path.join('assets', 'sprites')
        self.image = pygame.image.load(os.path.join(self.sprite_dir, "player.png")).convert_alpha()
        self.sprite = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.sprite.get_rect(center=(x, y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score = 0
        self.moving_to_enemy = False
        self.path = []
        self.map = game_map
        self.last_move_time = time.time()
        self.energy = 20
        self.state = ""

    def astar(self, start, target, obstacles):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            if current_node == target:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return path[::-1]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current_node[0] + dx, current_node[1] + dy)
                if neighbor not in obstacles:
                    neighbor_cost = self.map.get_tile_cost(neighbor[0], neighbor[1])
                    tentative_g_score = g_score[current_node] + neighbor_cost

                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current_node
                        g_score[neighbor] = tentative_g_score
                        heapq.heappush(open_set, (tentative_g_score + self.heuristic(neighbor, target), neighbor))

        return []

    @staticmethod
    def get_neighbors(node, obstacles):
        return [(node[0] + dx, node[1] + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)] if
                (node[0] + dx, node[1] + dy) not in obstacles]

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update(self, obstacles, enemies, potions):
        dx, dy = 0, 0

        # Calcula la posición inicial basada en la posición actual del personaje.
        start = (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
        print(start)

        if not self.moving_to_enemy or not self.path:
            closest_enemy = self.find_closest_enemy(enemies)
            closest_potion = self.find_closest_potion(potions)

            target_enemy = (
                closest_enemy.rect.x // TILE_SIZE, closest_enemy.rect.y // TILE_SIZE) if closest_enemy else None
            target_potion = (
                closest_potion.rect.x // TILE_SIZE, closest_potion.rect.y // TILE_SIZE) if closest_potion else None

            obstacle_positions = {(obstacle.rect.x // TILE_SIZE, obstacle.rect.y // TILE_SIZE) for obstacle in
                                  obstacles}

            # Determina si es posible y conveniente moverse hacia el enemigo más cercano.
            if closest_enemy:
                path_to_enemy = self.astar(start, target_enemy, obstacle_positions)
                if self.energy >= len(path_to_enemy) * self.map.get_tile_cost(
                        *start):  # Asume coste energético por movimiento.
                    self.path = path_to_enemy
                    self.moving_to_enemy = True
                    self.state = f"Moving to: {target_enemy}"
                else:
                    self.moving_to_enemy = False
            if not self.moving_to_enemy and closest_potion:  # Si no se mueve al enemigo, considera la poción.
                path_to_potion = self.astar(start, target_potion, obstacle_positions)
                if path_to_potion:
                    self.path = path_to_potion
                    self.state = "Moving to recharge"
            elif not closest_enemy and not closest_potion:
                self.state = "No path or goals found!"

        # Ejecuta el movimiento si hay un camino definido.
        if self.path:
            next_node = self.path.pop(0)
            next_position = (next_node[0] * TILE_SIZE, next_node[1] * TILE_SIZE)
            if next_position != (self.rect.x, self.rect.y):
                self.energy -= 1  # Consume energía por cada movimiento.
            dx = next_position[0] - self.rect.x
            dy = next_position[1] - self.rect.y
        else:
            self.moving_to_enemy = False

        # Actualiza la posición del personaje.
        next_rect = self.rect.move(dx, dy)

        # Verifica colisiones con obstáculos.
        colliding_obstacle = any(next_rect.colliderect(obstacle.rect) for obstacle in obstacles)
        if not colliding_obstacle:
            self.rect = next_rect

        # Verifica y maneja colisiones con enemigos.
        for enemy in enemies[:]:
            if next_rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                self.score += 1
                break

        # Verifica y maneja colisiones con pociones.
        for potion in potions[:]:
            if next_rect.colliderect(potion.rect):
                potions.remove(potion)
                self.energy += 10  # Asume recarga de 10 unidades de energía por poción.
                break

        # Asegura que el personaje no se mueva fuera de los límites permitidos del mapa.
        self.rect.clamp_ip(
            pygame.Rect(TILE_SIZE, TILE_SIZE, self.screen_width - 2 * TILE_SIZE, self.screen_height - 2 * TILE_SIZE))

    def find_closest_enemy(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in enemies:
            distance = abs(enemy.rect.x - self.rect.x) + abs(enemy.rect.y - self.rect.y)
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
        return closest_enemy

    def find_closest_potion(self, potions):
        closest_potion = None
        closest_distance = float('inf')
        for enemy in potions:
            distance = abs(enemy.rect.x - self.rect.x) + abs(enemy.rect.y - self.rect.y)
            if distance < closest_distance:
                closest_potion = enemy
                closest_distance = distance
        return closest_potion

    def draw(self, screen):
        self.rect.x = round(self.rect.x / TILE_SIZE) * TILE_SIZE
        self.rect.y = round(self.rect.y / TILE_SIZE) * TILE_SIZE
        screen.blit(self.sprite, self.rect)

    def get_score(self):
        return self.score

    def get_state(self):
        return self.state

    def get_batery(self):
        return self.energy
