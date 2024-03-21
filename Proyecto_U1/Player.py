import time
import pygame
import os
import heapq
from collections import deque

TILE_SIZE = 64
MOVE_DELAY = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height, game_map):
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
        self.trail = []
        self.map = game_map
        self.last_move_time = time.time()
        self.state = "Going to nearest enemy"

    def astar(self, start, target, obstacles):
        print("--------------------------")
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
                if neighbor not in obstacles:
                    neighbor_cost = self.map.get_tile_cost(neighbor[0], neighbor[1])
                    print(f"Hacia el nodo: {neighbor} : {neighbor_cost}")
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

    @staticmethod
    def bfs_search(start, target, obstacles):
        queue = deque()
        visited = set()
        queue.append((start, []))

        while queue:
            current_node, path = queue.popleft()

            if current_node == target:
                return path

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Solo movimientos ortogonales
                neighbor = (current_node[0] + dx, current_node[1] + dy)
                if neighbor not in obstacles and neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)

        return []

    def update(self, obstacles, enemies):
        dx, dy = 0, 0

        current_time = time.time()
        if current_time - self.last_move_time >= MOVE_DELAY and self.moving_to_enemy and self.path:
            next_node = self.path.pop(0)
            next_position = (next_node[0] * TILE_SIZE, next_node[1] * TILE_SIZE)
            dx = next_position[0] - self.rect.x
            dy = next_position[1] - self.rect.y
            self.last_move_time = current_time

        if not self.path:
            self.moving_to_enemy = False

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

        next_rect = self.rect.move(dx, dy)

        colliding_obstacle = any(next_rect.colliderect(obstacle.rect) for obstacle in obstacles)
        if not colliding_obstacle:
            self.rect = next_rect

        for enemy in enemies[:]:
            if next_rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                self.score += 1
                break

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

    def draw(self, screen):
        self.rect.x = round(self.rect.x / TILE_SIZE) * TILE_SIZE
        self.rect.y = round(self.rect.y / TILE_SIZE) * TILE_SIZE
        screen.blit(self.sprite, self.rect)

    def get_score(self):
        return self.score

    def get_state(self):
        return self.state
