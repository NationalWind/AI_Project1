from queue import PriorityQueue, Queue
from collections import deque

def find_path_level1(n, m, grid, algorithm='bfs'):
   
    if algorithm not in ['bfs', 'dfs', 'ucs', 'a_star', 'gbfs']:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    start, goal = find_start_goal(grid)
    
    
    if algorithm == 'bfs':
        frontier = Queue()
        frontier.put((start, 0))  # (position, cells)
        visited = set()
    elif algorithm == 'dfs':
        frontier = deque()
        frontier.append((start, 0))  # (position, cells)
        visited = set()  # For graph search
    else:  # UCS, A*, GBFS
        frontier = PriorityQueue()
        frontier.put((0, 0, start))  # (cost, cells, position)

    came_from = {start: None}
    cost_so_far = {start: (0, 0)}  # (cost, cells)

    while not frontier.empty():
        if algorithm == 'bfs' or algorithm == 'dfs':
            current, current_cells = frontier.get() if algorithm == 'bfs' else frontier.pop()
            current_cost = 0
        else:  # UCS, A*, GBFS
            current_cost, current_cells, current = frontier.get()

        if current == goal:
            break

    
        if algorithm == 'dfs':
            if current in visited:
                continue
            visited.add(current)

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_node = (next_row, next_col)

            if 0 <= next_row < n and 0 <= next_col < m:
                if grid[next_row][next_col] == -1: 
                    continue

                move_cost = 1  
                if isinstance(grid[next_row][next_col], int) and grid[next_row][next_col] > 0:
                    move_cost += grid[next_row][next_col]

                new_cost = current_cost + move_cost
                new_cells = current_cells + 1

                
                if algorithm == 'bfs' or algorithm == 'dfs':
                    if next_node not in visited:  
                        frontier.put((next_node, new_cells) if algorithm == 'bfs' else frontier.append((next_node, new_cells)))
                        came_from[next_node] = current
                else:
                    if next_node not in cost_so_far or (new_cost < cost_so_far[next_node][0] or (new_cost == cost_so_far[next_node][0] and new_cells < cost_so_far[next_node][1])):
                        cost_so_far[next_node] = (new_cost, new_cells)
                        priority = new_cost + heuristic(next_node, goal, algorithm)
                        frontier.put((priority, new_cells, next_node))
                        came_from[next_node] = current


    path = []
    if goal in came_from:
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

    return path

def find_start_goal(grid):
    start = None
    goal = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'G':
                goal = (r, c)
    return start, goal

def heuristic(node, goal, algorithm):
    if algorithm in ['a_star', 'gbfs']:
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    return 0  
