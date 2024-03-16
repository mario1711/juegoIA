import pygame
import os
import heapq
import math

TILE_SIZE = 64
MAP_SIZE = 13


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height, mapa):
        super().__init__()
        self.sprite_dir = os.path.join('assets', 'sprites')
        self.sound_dir = os.path.join('assets', 'sounds')
        self.image = pygame.image.load(os.path.join(self.sprite_dir, "player.png")).convert_alpha()
        self.sprite = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.sprite.get_rect(center=(x, y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score = 0
        self.blood_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "blood.mp3"))
        self.moving_to_enemy = False
        self.path = []
        self.mapa = mapa

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
                    print(path)
                return path[::-1]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current_node[0] + dx, current_node[1] + dy)
                if neighbor in obstacles:
                    continue
                new_cost = g_score[current_node] + 1  # Assuming uniform cost for simplicity
                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, target)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current_node

        return []

    @staticmethod
    def get_neighbors(node, obstacles):
        neighbors = [(node[0] + dx, node[1] + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
        valid_neighbors = [neighbor for neighbor in neighbors if neighbor not in obstacles]
        return valid_neighbors

    @staticmethod
    def heuristic(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def update(self, obstacles, enemies):
        if self.moving_to_enemy and self.path:
            # Obtener la posición del siguiente nodo en el camino
            next_node = self.path[0]
            next_position = (next_node[0] * TILE_SIZE, next_node[1] * TILE_SIZE)

            # Calcular el desplazamiento necesario para moverse hacia el siguiente nodo
            dx = next_position[0] - self.rect.x
            dy = next_position[1] - self.rect.y

            # Normalizar el desplazamiento para mantener una velocidad constante
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                dx = dx / distance
                dy = dy / distance

            # Aplicar el desplazamiento con una velocidad constante
            speed = 2
            dx *= speed
            dy *= speed

            # Mover al jugador
            self.rect.x += dx
            self.rect.y += dy

            # Verificar si el jugador ha llegado al nodo objetivo
            if abs(self.rect.x - next_position[0]) < 1 and abs(self.rect.y - next_position[1]) < 1:
                # Si ha llegado, eliminar el nodo del camino
                self.path.pop(0)

        # Si no hay más nodos en el camino, detener el movimiento
        if not self.path:
            self.moving_to_enemy = False

        # Si no está moviéndose hacia un enemigo, buscar el enemigo más cercano
        if not self.moving_to_enemy:
            closest_enemy = self.find_closest_enemy(enemies)
            if closest_enemy:
                start = (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
                target = (closest_enemy.rect.x // TILE_SIZE, closest_enemy.rect.y // TILE_SIZE)
                obstacle_positions = {(obstacle.rect.x // TILE_SIZE, obstacle.rect.y // TILE_SIZE) for obstacle in
                                      obstacles}
                self.path = self.astar(start, target, obstacle_positions)
                if self.path:
                    self.moving_to_enemy = True

        # Verificar colisiones con los límites de la pantalla
        self.rect.clamp_ip(
            pygame.Rect(TILE_SIZE, TILE_SIZE, self.screen_width - 2 * TILE_SIZE, self.screen_height - 2 * TILE_SIZE))

        # Verificar colisiones con los obstáculos
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Si hay una colisión, retroceder al último nodo en el camino
                self.path = []
                break

        # Verificar colisiones con los enemigos
        for enemy in enemies[:]:
            if self.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                self.score += 1
                pygame.mixer.Sound.play(self.blood_sound)
                break

    def find_closest_enemy(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in enemies:
            distance = math.sqrt((enemy.rect.x - self.rect.x) ** 2 + (enemy.rect.y - self.rect.y) ** 2)
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
        return closest_enemy

    def draw(self, screen):
        self.rect.x = round(self.rect.x / TILE_SIZE) * TILE_SIZE
        self.rect.y = round(self.rect.y / TILE_SIZE) * TILE_SIZE
        screen.blit(self.sprite, self.rect)

    def get_score(self):
        return self.score
