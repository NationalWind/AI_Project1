import heapq
from queue import PriorityQueue

def get_neighbors(x, y, n, m):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m:
            neighbors.append((nx, ny))
    return neighbors

def bfs(grid, start, goal, n, m):
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in get_neighbors(current[0], current[1], n, m):
            if grid[neighbor[0]][neighbor[1]] != '-1' and neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def dfs(grid, start, goal, n, m):
    stack = [start]
    came_from = {start: None}
    visited = set()
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        for neighbor in get_neighbors(current[0], current[1], n, m):
            if grid[neighbor[0]][neighbor[1]] != '-1' and neighbor not in visited:
                stack.append(neighbor)
                if neighbor not in came_from:
                    came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def ucs(grid, start, goal, n, m):
    priority_queue = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)
        if current == goal:
            break
        for neighbor in get_neighbors(current[0], current[1], n, m):
            if grid[neighbor[0]][neighbor[1]] == '-1':
                continue
            new_cost = current_cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor))
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def greedy_bfs(grid, start, goal, n, m):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    priority_queue = [(heuristic(start, goal), start)]
    came_from = {start: None}
    visited = set()
    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        for neighbor in get_neighbors(current[0], current[1], n, m):
            if grid[neighbor[0]][neighbor[1]] != '-1' and neighbor not in visited:
                heapq.heappush(priority_queue, (heuristic(neighbor, goal), neighbor))
                if neighbor not in came_from:
                    came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def a_star(grid, start, goal, n, m):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    priority_queue = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        if current == goal:
            break
        for neighbor in get_neighbors(current[0], current[1], n, m):
            if grid[neighbor[0]][neighbor[1]] == '-1':
                continue
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (priority, neighbor))
                came_from[neighbor] = current
    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return None
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def find_path_level1( n, m, start, goal,grid):
    algorithms = {
        "BFS": bfs,
       # "DFS": dfs,
       # "UCS": ucs,
       # "GreedyBFS": greedy_bfs,
        #"A*": a_star
    }
    
    paths = {}
    for name, algorithm in algorithms.items():
        path = algorithm(grid, start, goal, n, m)
        paths[name] = path
    return paths

