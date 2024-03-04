import pygame
import os
import heapq

TILE_SIZE = 64


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
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

            for neighbor in self.get_neighbors(current_node, obstacles):
                tentative_g_score = g_score[current_node] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score + self.heuristic(neighbor, target), neighbor))

        return []

    @staticmethod
    def get_neighbors(node, obstacles):
        # Obtener los nodos vecinos válidos (no obstáculos)
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (node[0] + dx, node[1] + dy)
            if neighbor not in obstacles:
                neighbors.append(neighbor)
        return neighbors

    @staticmethod
    def heuristic(a, b):
        # Calcular la distancia heurística (por ejemplo, distancia Manhattan)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update(self, keys, obstacles, enemies):
        dx, dy = 0, 0

        # Obtener la dirección del movimiento de las teclas presionadas
        if keys[pygame.K_UP]:
            dy = -TILE_SIZE
        elif keys[pygame.K_DOWN]:
            dy = TILE_SIZE
        elif keys[pygame.K_LEFT]:
            dx = -TILE_SIZE
        elif keys[pygame.K_RIGHT]:
            dx = TILE_SIZE

        if keys[pygame.K_SPACE]:
            closest_enemy = self.find_closest_enemy(enemies)
            if closest_enemy:
                path = self.astar((self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE),
                                  (closest_enemy.rect.x // TILE_SIZE, closest_enemy.rect.y // TILE_SIZE),
                                  set((obstacle.rect.x // TILE_SIZE, obstacle.rect.y // TILE_SIZE) for obstacle in
                                      obstacles))
                if path:
                    next_node = path[0]
                    dx = (next_node[0] - self.rect.x // TILE_SIZE) * TILE_SIZE
                    dy = (next_node[1] - self.rect.y // TILE_SIZE) * TILE_SIZE
                    self.rect.move_ip(dx, dy)

        # Calcular la próxima posición del jugador
        next_rect = self.rect.move(dx, dy)

        # Verificar colisiones con los obstáculos
        if not any(next_rect.colliderect(obstacle.rect) for obstacle in obstacles):
            self.rect = next_rect

        # Verificar colisiones con los enemigos
        for enemy in enemies[:]:  # Usamos [:] para hacer una copia de la lista y evitar problemas al eliminar elementos
            if next_rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                self.score += 1
                pygame.mixer.Sound.play(self.blood_sound)
                break

        # Verificar los límites de la pantalla
        self.rect.clamp_ip(
            pygame.Rect(TILE_SIZE, TILE_SIZE, self.screen_width - 2 * TILE_SIZE, self.screen_height - 2 * TILE_SIZE))

    def find_closest_enemy(self, enemies):
        # Encontrar el enemigo más cercano al jugador
        closest_enemy = None
        closest_distance = float('inf') 
        for enemy in enemies:
            distance = abs(enemy.rect.x - self.rect.x) + abs(enemy.rect.y - self.rect.y)
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
