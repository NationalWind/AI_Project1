import pygame
import sys
import time
import re
import math
from queue import PriorityQueue
import random 
from level1 import find_path_level1
from level3 import find_path_level3
from level2 import find_path_level2
import level4


# Define level and input file
input_file = 'Source/input1_level1.txt'  # Change the input file name here

# Function to get level from filename
def get_level_from_filename(filename):
    match = re.search(r'_level(\d+)', filename)
    if match:
        level = int(match.group(1))
        return level
    else:
        return None

level = get_level_from_filename(input_file)

# Function to read input file for Level 1
def read_input_file_level1(file_path):
    with open(file_path, 'r') as f:
        n, m = map(int, f.readline().strip().split())
        city_map = []
        for _ in range(n):
            line = f.readline().strip()
            row = []
            for char in line:
                if char == '0':
                    row.append(0)
                elif char == '1':
                    row.append(-1)
                elif char == 'S':
                    row.append('S')
                elif char == 'G':
                    row.append('G')
                elif char.isdigit():
                    row.append(int(char))
            city_map.append(row)
    
        return n, m, city_map

# Function to read input file for Level 2
def read_input_file_level2(file_path):
    with open(file_path, 'r') as f:
        n, m, t = map(int, f.readline().strip().split())
        city_map = []
        toll_booths = {}
        for i in range(n):
            line = f.readline().strip().split()
            row = []
            for j, char in enumerate(line):
                if char == '0':
                    row.append(0)
                elif char == '-1':
                    row.append(-1)
                elif char == 'S':
                    row.append('S')
                elif char == 'G':
                    row.append('G')
                elif char.isdigit():
                    toll_time = int(char)
                    row.append(toll_time)
                    toll_booths[(i, j)] = toll_time
            city_map.append(row)
        return n, m, t, city_map, toll_booths

def read_input_file_level3(file_path):
    with open(file_path, 'r') as f:
        n, m, committed_time, fuel_capacity = map(int, f.readline().strip().split())
        city_map = []
        grid = []
        gas_stations = {}  # Use a dictionary to store refuel times
        toll_booths = {}
        
        for i in range(n):
            line = f.readline().strip().split()
            row = []
            for j, char in enumerate(line):
                if char == '0':
                    row.append(0)
                elif char == '-1':
                    row.append(-1)
                elif char == 'S':
                    row.append('S')
                elif char == 'G':
                    row.append('G')
                elif char.startswith('F'):
                    refuel_time = int(char[1:])  # Extract refuel time
                    row.append((i, j))  # Store position
                    gas_stations[(i, j)] = refuel_time
                elif char.isdigit():
                    toll_time = int(char)
                    row.append(toll_time)
                    toll_booths[(i, j)] = toll_time
            city_map.append(row)
            grid.append(line)
        
        return n, m, committed_time, fuel_capacity, city_map, gas_stations, toll_booths, grid

def read_input_file_level4(file_path):
    with open(file_path, 'r') as f:
        n, m, committed_time, fuel_capacity = map(int, f.readline().strip().split())
        city_map = []
        gas_stations = {}  # Use a dictionary to store refuel times
        toll_booths = {}
        vehicles = {}  # Store vehicle positions and destinations
        goals = {}  # Store goal positions

        grid = [[] for _ in range(n)]

        start_pattern = re.compile(r'^S(\d+)$')
        goal_pattern = re.compile(r'^G(\d+)$')
        
        for i in range(n):
            line = f.readline().strip().split()
            grid[i] = line
            row = []
            for j, char in enumerate(line):
                if char == '0':
                    row.append(0)
                elif char == '-1':
                    row.append(-1)
                elif char == 'S':
                    row.append('S')
                elif char == 'G':
                    row.append('G')
                elif char.startswith('F'):
                    refuel_time = int(char[1:])  # Extract refuel time
                    row.append((i, j))  # Store position
                    gas_stations[(i, j)] = refuel_time
                elif char.isdigit():
                    toll_time = int(char)
                    row.append(toll_time)
                    toll_booths[(i, j)] = toll_time
                elif start_pattern.match(char):
                    vehicle_id = int(start_pattern.match(char).group(1))
                    row.append(char)
                    vehicles[vehicle_id] = {'position': (i, j), 'destination': None}
                elif goal_pattern.match(char):
                    goal_id = int(goal_pattern.match(char).group(1))
                    row.append(char)
                    goals[goal_id] = (i, j)
                    
            city_map.append(row)
        
        start_goal = [[[-1, -1], [-1, -1]] for _ in range(10)]

        for i in range(n):
            for j in range(m):
                c = grid[i][j]
                if c == "S":
                    c = "S0"
                if c == "G":
                    c = "G0"

                if c[0] == "S":
                    start_goal[int(c[1])][0] = [i, j]
                if c[0] == "G":
                    start_goal[int(c[1])][1] = [i, j]

        while start_goal and start_goal[-1][0] == [-1, -1]:
            start_goal.pop()

        return n, m, committed_time, fuel_capacity, city_map, gas_stations, toll_booths, vehicles, goals, grid, start_goal

# Function for uniform cost search pathfinding algorithm (test GUI)
def uniform_cost_search(city_map, start, goal):
    n = len(city_map)
    m = len(city_map[0])
    frontier = PriorityQueue()
    frontier.put((0, start))  # (cost, (row, col))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current_cost, current = frontier.get()
        
        if current == goal:
            break
        
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row = current[0] + direction[0]
            next_col = current[1] + direction[1]
            next_node = (next_row, next_col)
            
            if 0 <= next_row < n and 0 <= next_col < m:
                if city_map[next_row][next_col] == -1:
                    continue
                
                new_cost = current_cost + 1  # Assuming cost for each move is 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    frontier.put((priority, next_node))
                    came_from[next_node] = current
    
    # Reconstruct path
    path = []
    if goal in came_from:
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
    
    return path


# Initialize Pygame
pygame.init()

# Set up the display with a larger size
screen_size = (800, 800)
SCREEN_WIDTH, SCREEN_HEIGHT = screen_size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Delivery Route Visualization")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 224)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (1, 50, 32)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_PINK = (255, 182, 193)

# Read input file based on level
if level == 1:
    n, m, city_map = read_input_file_level1(input_file)
elif level == 2:
    n, m, t, city_map, toll_booths = read_input_file_level2(input_file)
elif level == 3:
    n, m, committed_time, fuel_capacity, city_map, gas_stations, toll_booths, grid = read_input_file_level3(input_file)
elif level == 4:
    n, m, committed_time, fuel_capacity, city_map, gas_stations, toll_booths, vehicles, goals, grid, start_goal = read_input_file_level4(input_file)
else:
    print(f"Unsupported level: {level}")
    pygame.quit()
    sys.exit()

# Find start and goal positions
start_pos = None
goal_pos = None
for row in range(n):
    for col in range(m):
        if city_map[row][col] == 'S':
            start_pos = (row, col)
        elif city_map[row][col] == 'G':
            goal_pos = (row, col)

# Cell size
cell_size = 45

# Offset to position the map in the center of the screen
offset_x = (screen_size[0] - m * cell_size) // 2
offset_y = (screen_size[1] - n * cell_size) // 2

# Set font for drawing text
font = pygame.font.SysFont('Arial', 20)

# Draw the map function for level 1
def draw_map_level1(screen, city_map, cells_traversed=None):
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            color = WHITE
            if city_map[row][col] == -1:
                color = DARK_BLUE
            elif city_map[row][col] == 'S':
                color = LIGHT_GREEN
            elif city_map[row][col] == 'G':
                color = LIGHT_PINK

            pygame.draw.rect(screen, color, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size), 1)

            # Draw text for special positions (S and G)
            if city_map[row][col] == 'S' or city_map[row][col] == 'G':
                text_surface = font.render(city_map[row][col], True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)
    if cells_traversed is not None:
        cells_text = font.render(f"Cells Traversed: {cells_traversed}", True, BLACK)
        screen.blit(cells_text, (20, 50))

# Draw the map function
def draw_map_level2(screen, city_map, elapsed_time=None, cells_traversed=None):
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            color = WHITE
            if city_map[row][col] == -1:
                color = DARK_BLUE
            elif city_map[row][col] == 'S':
                color = LIGHT_GREEN  
            elif city_map[row][col] == 'G':
                color = LIGHT_PINK
            elif isinstance(city_map[row][col], int) and city_map[row][col] > 0:
                color = LIGHT_BLUE  

            pygame.draw.rect(screen, color, (offset_x + col*cell_size, offset_y + row*cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (offset_x + col*cell_size, offset_y + row*cell_size, cell_size, cell_size), 1)

            # Draw text for special positions (S and G)
            if city_map[row][col] == 'S' or city_map[row][col] == 'G':
                text_surface = font.render(city_map[row][col], True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col*cell_size + cell_size // 2, offset_y + row*cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)

            # Draw text for toll booths
            elif isinstance(city_map[row][col], int) and city_map[row][col] > 0:
                text_surface = font.render(str(city_map[row][col]), True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col*cell_size + cell_size // 2, offset_y + row*cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)
    # Display elapsed time and cells traversed
    if elapsed_time is not None:
        time_text = font.render(f"Elapsed Time: {elapsed_time} seconds", True, BLACK)
        screen.blit(time_text, (20, 20))
    if cells_traversed is not None:
        cells_text = font.render(f"Cells Traversed: {cells_traversed}", True, BLACK)
        screen.blit(cells_text, (20, 50))

def draw_map_level3(screen, city_map, fuel_remaining=None, elapsed_time=None):
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            color = WHITE
            cell_value = city_map[row][col]
            if cell_value == -1:
                color = DARK_BLUE
            elif cell_value == 'S':
                color = LIGHT_GREEN
            elif cell_value == 'G':
                color = LIGHT_PINK
            elif isinstance(cell_value, int) and cell_value > 0:
                color = LIGHT_BLUE  # Toll booth
            elif isinstance(city_map[row][col], tuple) and city_map[row][col] in gas_stations:
                color = LIGHT_YELLOW  # Gas station
            
            pygame.draw.rect(screen, color, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size), 1)

            # Draw text for special positions (S and G)
            if cell_value == 'S' or cell_value == 'G':
                text_surface = font.render(cell_value, True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)

            # Draw text for toll booths and gas stations
            elif isinstance(cell_value, int) and cell_value > 0:
                text_surface = font.render(str(cell_value), True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)
            elif isinstance(city_map[row][col], tuple) and city_map[row][col] in gas_stations:
                text_surface = font.render(f"F{gas_stations[city_map[row][col]]}", True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)
    # Display elapsed time
    if elapsed_time is not None:
        time_text = font.render(f"Elapsed Time: {elapsed_time} seconds", True, BLACK)
        screen.blit(time_text, (20, 20))

    # Display remaining fuel
    if fuel_remaining is not None:
        fuel_text = font.render(f"Fuel Remaining: {fuel_remaining} liters", True, BLACK)
        screen.blit(fuel_text, (20, 40))
         
# Draw the path function
def draw_path(screen, segments, color, current_position):
    # Highlight current position
    if current_position:
        pygame.draw.rect(screen, YELLOW, (offset_x + current_position[1] * cell_size, offset_y + current_position[0] * cell_size, cell_size, cell_size), 3)
        
    if not segments:
        return

    for segment in segments:
        start = segment[0]
        end = segment[1]
        start_pos = (offset_x + start[1] * cell_size + cell_size // 2, offset_y + start[0] * cell_size + cell_size // 2)
        end_pos = (offset_x + end[1] * cell_size + cell_size // 2, offset_y + end[0] * cell_size + cell_size // 2)
        pygame.draw.line(screen, color, start_pos, end_pos, 3)


# Main loop
running = True
current_position = start_pos
elapsed_time = 0
segments = []
path_found = False
if level in [3, 4]:
    fuel_remaining = fuel_capacity
curr_id = 1
total_steps = 0
i = 0
pygame.time.set_timer(pygame.USEREVENT + 1, 200)

# for level 4
if level == 4:
    n_agents = len(start_goal)
    t = committed_time
    f = fuel_capacity
    cur_state = [(*start_goal[i][0], 0, t, -1, f) for i in range(n_agents)]
    prev_state = cur_state
    gantt = [[[] for _ in range(n_agents)] for _ in range(t + 1)]

    def draw_text(text, position, font_size=36, color=BLACK):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

    def draw_map_level4():
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                color = WHITE
                cell_value = grid[row][col]
                cell_value_map = city_map[row][col]
                if cell_value == "-1":
                    color = DARK_BLUE
                elif isinstance(cell_value_map, int) and cell_value_map > 0:
                    color = LIGHT_BLUE
                elif isinstance(cell_value, str):
                    if cell_value.startswith('S') or cell_value == 'S':
                        if len(cell_value) == 1:
                            color = LIGHT_GREEN
                        else:
                            color = GREEN
                    elif cell_value.startswith('G') or cell_value == 'G':
                        if len(cell_value) == 1:
                            color = LIGHT_PINK
                        else:
                            color = RED
                    elif cell_value.startswith('F') or cell_value == 'F':
                        color = LIGHT_YELLOW

                pygame.draw.rect(screen, color, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size), 1)

                # Draw text for special positions (S, G, and F)
                if isinstance(cell_value, str) and (cell_value.startswith('G') or cell_value.startswith('S') or cell_value.startswith('F')):
                    text_surface = font.render(cell_value, True, BLACK)
                    text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                    screen.blit(text_surface, text_rect)
                if cell_value == 'S' or cell_value == 'G':
                    text_surface = font.render(cell_value, True, BLACK)
                    text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                    screen.blit(text_surface, text_rect)
                # Draw text for toll booths and gas stations
                elif isinstance(cell_value_map, int) and cell_value_map > 0:
                    text_surface = font.render(str(cell_value_map), True, BLACK)
                    text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                    screen.blit(text_surface, text_rect)
                elif isinstance(city_map[row][col], tuple) and city_map[row][col] in gas_stations:
                    text_surface = font.render(f"F{gas_stations[city_map[row][col]]}", True, BLACK)
                    text_rect = text_surface.get_rect(center=(offset_x + col * cell_size + cell_size // 2, offset_y + row * cell_size + cell_size // 2))
                    screen.blit(text_surface, text_rect)
        pygame.display.update()
        # Display elapsed time
        if elapsed_time is not None:
            time_text = font.render(f"Elapsed Time: {elapsed_time} seconds", True, BLACK)
            screen.blit(time_text, (20, 20))

        # Display remaining fuel
        if fuel_remaining is not None:
            fuel_text = font.render(f"Fuel Remaining: {fuel_remaining} liters", True, BLACK)
            screen.blit(fuel_text, (20, 40))

    def draw_cur_states():
        for i in range(n_agents):
            # Define previous and current positions
            start_pos = (offset_x + cell_size // 2 + prev_state[i][1] * cell_size, 
            offset_y + cell_size // 2 + prev_state[i][0] * cell_size)
            end_pos = (offset_x + cell_size // 2 + cur_state[i][1] * cell_size, 
            offset_y + cell_size // 2 + cur_state[i][0] * cell_size)

            # Draw the agent as a circle at the current position
            if i == 0:
                circle_color = RED
            else:
                circle_color = GREEN
            pygame.draw.circle(
                screen,
                circle_color,
                end_pos,
                10,
            )

        pygame.display.update()

        
    def update_new_goal(i):
        start_goal[i][1][0] = random.randint(0, n - 1)
        start_goal[i][1][1] = random.randint(0, m - 1)
        while (
            grid[start_goal[i][1][0]][start_goal[i][1][1]][0] in ["G", "S", "F"]
            or int(grid[start_goal[i][1][0]][start_goal[i][1][1]]) != 0
            or any((state[0], state[1]) == (start_goal[i][1][0], start_goal[i][1][1]) for state in cur_state)
        ):
            start_goal[i][1][0] = random.randint(0, n - 1)
            start_goal[i][1][1] = random.randint(0, m - 1)

        grid[start_goal[i][1][0]][start_goal[i][1][1]] = f"G{i}"
        grid[start_goal[i][0][0]][start_goal[i][0][1]] = "0"
        grid[cur_state[i][0]][cur_state[i][1]] = f"S{i}"
        start_goal[i][0] = [
            cur_state[i][0],
            cur_state[i][1],
        ]
        cur_state[i] = (*start_goal[i][0], 0, t, -1, f)

screen.fill(WHITE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    
    if level == 1:
        draw_map_level1(screen, city_map, total_steps)
        # test gui
        
        path = find_path_level1( n, m, start_pos, goal_pos,city_map, algorithm='dfs')

        if path:
            if current_position == goal_pos:
                break

            next_position = path[curr_id]
            curr_id += 1 # Path adjustment

            time.sleep(0.75)  # Adjust delay for visualization

            # Add segment to draw path
            segments.append((current_position, next_position))
            
            current_position = next_position
            total_steps += 1

        # Draw path segments
        draw_path(screen, segments, RED, current_position)
        
    elif level == 2:
        draw_map_level2(screen, city_map, elapsed_time, total_steps)
        # test gui
        # path = uniform_cost_search(city_map, current_position, goal_pos)
        path = find_path_level2(city_map, current_position, goal_pos, t)
        
        if path:
            if current_position == goal_pos:
                break

            next_position = path[1]
            time.sleep(0.75)  # Adjust delay for visualization

            # Calculate time for the current cell
            cell_value = city_map[next_position[0]][next_position[1]]
            if isinstance(cell_value, int) and cell_value > 0:
                # Toll booth: add time for the toll booth
                elapsed_time += cell_value + 1
            else:
                # Normal cell or empty cell: add 1 minute for the move
                elapsed_time += 1

            # Add segment to draw path
            segments.append((current_position, next_position))
            
            current_position = next_position
            total_steps += 1

        # Draw path segments
        draw_path(screen, segments, RED, current_position)
        
    elif level == 3:
        draw_map_level3(screen, city_map,fuel_remaining, elapsed_time)
        # find path
        path = find_path_level3(n, m, committed_time, fuel_capacity, grid) 
        if path:
            if current_position == goal_pos:
                break

            next_position = path[curr_id]
            curr_id += 1 # Path adjustment

            time.sleep(0.75)  # Adjust delay for visualization

            # Calculate time for the current cell and handle refueling
            cell_value = city_map[next_position[0]][next_position[1]]

            elapsed_time += 1 # Path adjustment
                
            # Consume fuel
            if next_position == current_position:
                fuel_remaining -= 1
            
            # Check if out of fuel
            if fuel_remaining < 0:
                print("Ran out of fuel!")
                break

            # Add segment to draw path
            segments.append((current_position, next_position))
            
            current_position = next_position
            total_steps += 1

        # Draw path segments
        draw_path(screen, segments, RED, current_position)

    elif level == 4:
        # find curr states
        if event.type == pygame.USEREVENT + 1:
            if [cur_state[0][0], cur_state[0][1]] != start_goal[0][1] or i > 0:
                if start_goal[i][1] == [-1, -1]:
                    update_new_goal(i)
                node = level4.A_star(n, m, f, cur_state[i], (*start_goal[i][1], 0, 0, -1, 0), grid, cur_state, gantt, i, max(0, cur_state[i][3] - cur_state[0][3] - 1))
                path = level4.trace(node)[0]
                if not path:
                    if i == 0:
                        print("Not OK")
                        running = False
                        break
                    else:
                        prev_state = cur_state
                        for tp in range(0, cur_state[i][3]):
                            gantt[tp][i] = cur_state[i]
                        i = (i + 1) % n_agents
                        continue
                for state in path:
                    gantt[state[3]][i] = state
                path.pop()
                prev_state = cur_state
                cur_state[i] = path[-1]
                path.pop()
                if i > 0:
                    # it will randomly generate a valid destination on the map (i.e., not on obstacles, or other vehicles)
                    if (cur_state[i][0], cur_state[i][1]) == tuple(start_goal[i][1]):
                        start_goal[i][1] = [-1, -1]

                if i == n_agents - 1:
                    draw_map_level4()
                    draw_cur_states()
                    elapsed_time = t - cur_state[0][3]
                    fuel_remaining = cur_state[0][5]
                    total_steps += 1
                    time.sleep(0.75)
                i = (i + 1) % n_agents
            else:
                print("OK")
                running = False
                break
    pygame.display.flip()

# After the main loop ends
if current_position == goal_pos:
    if level in [2, 3, 4]:
        print(f"Reached the goal in {elapsed_time} minutes.")
    print(f"Cells Traversed (include Goal): {total_steps}")
else:
    print("Path not found.")

time.sleep(5)

pygame.quit()
sys.exit()
