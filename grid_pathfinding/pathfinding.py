import heapq
from collections import deque
import time
import sys

class GridPathfinder:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
        
    def is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0
    
    def heuristic(self, a, b):
        # Manhattan distance for grid
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def bfs(self):
        start_time = time.time()
        visited = set()
        queue = deque([(self.start, [self.start])])
        visited.add(self.start)
        
        max_memory = 0
        
        while queue:
            max_memory = max(max_memory, len(queue) + len(visited))
            current, path = queue.popleft()
            
            if current == self.end:
                end_time = time.time()
                return {
                    'path': path,
                    'time': end_time - start_time,
                    'nodes_visited': len(visited),
                    'max_memory': max_memory,
                    'algorithm': 'BFS'
                }
            
            for dx, dy in self.directions:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if self.is_valid(next_x, next_y) and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        
        end_time = time.time()
        return {
            'path': None,
            'time': end_time - start_time,
            'nodes_visited': len(visited),
            'max_memory': max_memory,
            'algorithm': 'BFS'
        }
    
    def dfs(self):
        start_time = time.time()
        visited = set()
        stack = [(self.start, [self.start])]
        visited.add(self.start)
        
        max_memory = 0
        
        while stack:
            max_memory = max(max_memory, len(stack) + len(visited))
            current, path = stack.pop()
            
            if current == self.end:
                end_time = time.time()
                return {
                    'path': path,
                    'time': end_time - start_time,
                    'nodes_visited': len(visited),
                    'max_memory': max_memory,
                    'algorithm': 'DFS'
                }
            
            for dx, dy in self.directions:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if self.is_valid(next_x, next_y) and next_pos not in visited:
                    visited.add(next_pos)
                    stack.append((next_pos, path + [next_pos]))
        
        end_time = time.time()
        return {
            'path': None,
            'time': end_time - start_time,
            'nodes_visited': len(visited),
            'max_memory': max_memory,
            'algorithm': 'DFS'
        }
    
    def dijkstra(self):
        start_time = time.time()
        
        # Priority queue: (distance, current_pos)
        pq = [(0, self.start)]
        
        # Distance from start to each node
        distances = {}
        for i in range(self.rows):
            for j in range(self.cols):
                distances[(i, j)] = float('inf')
        distances[self.start] = 0
        
        # To reconstruct the path
        came_from = {}
        
        visited = set()
        max_memory = 0
        
        while pq:
            max_memory = max(max_memory, len(pq) + len(visited) + len(distances))
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == self.end:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path.reverse()
                
                end_time = time.time()
                return {
                    'path': path,
                    'time': end_time - start_time,
                    'nodes_visited': len(visited),
                    'max_memory': max_memory,
                    'algorithm': 'Dijkstra'
                }
            
            for dx, dy in self.directions:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if self.is_valid(next_x, next_y):
                    new_dist = current_dist + 1  # Grid movement cost is 1
                    
                    if new_dist < distances[next_pos]:
                        distances[next_pos] = new_dist
                        came_from[next_pos] = current
                        heapq.heappush(pq, (new_dist, next_pos))
        
        end_time = time.time()
        return {
            'path': None,
            'time': end_time - start_time,
            'nodes_visited': len(visited),
            'max_memory': max_memory,
            'algorithm': 'Dijkstra'
        }
    
    def a_star(self):
        start_time = time.time()
        
        # Priority queue: (f_score, current_pos)
        pq = [(0, self.start)]
        
        # g_score: distance from start to current node
        g_score = {}
        for i in range(self.rows):
            for j in range(self.cols):
                g_score[(i, j)] = float('inf')
        g_score[self.start] = 0
        
        # f_score: g_score + heuristic
        f_score = {}
        for i in range(self.rows):
            for j in range(self.cols):
                f_score[(i, j)] = float('inf')
        f_score[self.start] = self.heuristic(self.start, self.end)
        
        # To reconstruct the path
        came_from = {}
        
        visited = set()
        max_memory = 0
        
        while pq:
            max_memory = max(max_memory, len(pq) + len(visited) + len(g_score))
            current_f, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == self.end:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path.reverse()
                
                end_time = time.time()
                return {
                    'path': path,
                    'time': end_time - start_time,
                    'nodes_visited': len(visited),
                    'max_memory': max_memory,
                    'algorithm': 'A*'
                }
            
            for dx, dy in self.directions:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if self.is_valid(next_x, next_y):
                    tentative_g = g_score[current] + 1  # Grid movement cost is 1
                    
                    if tentative_g < g_score[next_pos]:
                        came_from[next_pos] = current
                        g_score[next_pos] = tentative_g
                        f_score[next_pos] = tentative_g + self.heuristic(next_pos, self.end)
                        heapq.heappush(pq, (f_score[next_pos], next_pos))
        
        end_time = time.time()
        return {
            'path': None,
            'time': end_time - start_time,
            'nodes_visited': len(visited),
            'max_memory': max_memory,
            'algorithm': 'A*'
        }
    
    def run_all_algorithms(self):
        results = []
        algorithms = [self.bfs, self.dfs, self.dijkstra, self.a_star]
        
        for algo in algorithms:
            result = algo()
            results.append(result)
        
        return results
