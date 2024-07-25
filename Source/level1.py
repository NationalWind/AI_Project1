import heapq
from collections import deque

# Node class to represent each point in the grid
class Node:
    def __init__(self, state, path_cost=0, parent=None):
        self.state = state  # state is a tuple (i, j)
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost

# Breadth-first search implementation
def bfs(n, m, start_state, goal_state, grid):
    node = Node(start_state)
    frontier = deque([node])
    reached = {node.state: node}
    while frontier:
        node = frontier.popleft()
        if node.state == goal_state:
            return node
        for child in expand(node, n, m, grid):
            s = child.state
            if s not in reached:
                reached[s] = child
                frontier.append(child)
    return None

# Depth-first search implementation
def dfs(n, m, start_state, goal_state, grid):
    node = Node(start_state)
    frontier = [node]  
    reached = {node.state: node}  

    while frontier:
        node = frontier.pop()
        if node.state == goal_state:
            return node
        
        for child in expand(node, n, m, grid):
            s = child.state
            if s not in reached:  
                reached[s] = child  
                frontier.append(child)  

    return None 


# Uniform-cost search implementation
def ucs(n, m, start_state, goal_state, grid):
    node = Node(start_state)
    frontier = []
    heapq.heappush(frontier, node)
    reached = {node.state: node}
    while frontier:
        node = heapq.heappop(frontier)
        if node.state == goal_state:
            return node
        for child in expand(node, n, m, grid):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                heapq.heappush(frontier, child)
    return None

# Greedy best-first search implementation
def gbfs(n, m, start_state, goal_state, grid):
    def heuristic(state):
        # Manhattan distance heuristic
        return abs(state[0] - goal_state[0]) + abs(state[1] - goal_state[1])
    
    node = Node(start_state)
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state), node))
    reached = {node.state: node}
    while frontier:
        _, node = heapq.heappop(frontier)
        if node.state == goal_state:
            return node
        for child in expand(node, n, m, grid):
            s = child.state
            if s not in reached:
                reached[s] = child
                heapq.heappush(frontier, (heuristic(s), child))
    return None

# A* search implementation
def a_star(n, m, start_state, goal_state, grid):
    def heuristic(node):
        # Combined cost of path and heuristic estimate
        return node.path_cost + abs(goal_state[0] - node.state[0]) + abs(goal_state[1] - node.state[1])
    
    node = Node(start_state)
    frontier = []
    heapq.heappush(frontier, (heuristic(node), node))
    reached = {node.state: node}
    while frontier:
        _, node = heapq.heappop(frontier)
        if node.state == goal_state:
            return node
        for child in expand(node, n, m, grid):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                heapq.heappush(frontier, (heuristic(child), child))
    return None

# Function to expand nodes and avoid obstacles
def expand(node, n, m, grid):
    children = []
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    i, j = node.state
    for move in moves:
        u, v = i + move[0], j + move[1]
        # Check boundaries and obstacle presence
        if 0 <= u < n and 0 <= v < m and grid[u][v] != -1:  # Ensure grid[u][v] is treated as an integer
            child = Node((u, v), node.path_cost + 1, node)
            children.append(child)
    return children

# Function to trace the path from the goal node to the start
def trace(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# Main function to find the path using specified algorithm
def find_path_level1(n, m, start_coord, goal_coord, grid, algorithm='dfs'):
    if algorithm == 'bfs':
        node = bfs(n, m, start_coord, goal_coord, grid)
    elif algorithm == 'dfs':
        node = dfs(n, m, start_coord, goal_coord, grid)
    elif algorithm == 'ucs':
        node = ucs(n, m, start_coord, goal_coord, grid)
    elif algorithm == 'gbfs':
        node = gbfs(n, m, start_coord, goal_coord, grid)
    elif algorithm == 'a_star':
        node = a_star(n, m, start_coord, goal_coord, grid)
    else:
        raise ValueError("Unknown algorithm specified.")

    if node is not None:
        path = trace(node)
        return path
    else:
        return None
