from queue import Queue, PriorityQueue


class Astar:
    def __init__(self):
        self.path = []

    def find_path(self, start, goal, graph):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

    @staticmethod
    def heuristic(a, b):
        # Manhattan distance on a square grid
        return abs(a.x - b.x) + abs(a.y - b.y)
