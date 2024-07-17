import pygame
import sys
import time
import re
from queue import PriorityQueue

# Function to get level from filename
def get_level_from_filename(filename):
    match = re.search(r'_level(\d+)', filename)
    if match:
        level = int(match.group(1))
        return level
    else:
        return None

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

# Function to read input file for Level 3
def read_input_file_level3(file_path):
    with open(file_path, 'r') as f:
        n, m, committed_time, fuel_capacity = map(int, f.readline().strip().split())
        city_map = []
        gas_stations = []
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
                    refuel_time = int(char[1:])
                    row.append(refuel_time)
                    gas_stations.append((i, j, refuel_time))
                elif char.isdigit():
                    toll_time = int(char)
                    row.append(toll_time)
                    toll_booths[(i, j)] = toll_time
            city_map.append(row)
        return n, m, committed_time, fuel_capacity, city_map, gas_stations, toll_booths

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
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Delivery Route Visualization")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)

# Define level and input file
input_file = 'input1_level2.txt'  # Change the input file name here
level = get_level_from_filename(input_file)

# Read input file based on level
if level == 1:
    n, m, city_map = read_input_file_level1(input_file)
elif level == 2:
    n, m, t, city_map, toll_booths = read_input_file_level2(input_file)
elif level == 3:
    n, m, committed_time, fuel_capacity, city_map, gas_stations, toll_booths = read_input_file_level3(input_file)
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

# Draw the map function
def draw_map(screen, city_map, current_position=None, elapsed_time=None):
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            color = WHITE
            if city_map[row][col] == -1:
                color = DARK_BLUE
            elif city_map[row][col] == 'S':
                color = LIGHT_GREEN  
            elif city_map[row][col] == 'G':
                color = (255, 182, 193)  #light pink
            elif isinstance(city_map[row][col], int) and city_map[row][col] > 0:
                color = LIGHT_BLUE  
            elif isinstance(city_map[row][col], str) and city_map[row][col].startswith('F'):
                color = YELLOW  

            pygame.draw.rect(screen, color, (offset_x + col*cell_size, offset_y + row*cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (offset_x + col*cell_size, offset_y + row*cell_size, cell_size, cell_size), 1)

            # Draw text for special positions (S and G)
            if city_map[row][col] == 'S' or city_map[row][col] == 'G':
                text_surface = font.render(city_map[row][col], True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col*cell_size + cell_size // 2, offset_y + row*cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)

            # Draw text for toll booths and gas stations
            elif isinstance(city_map[row][col], int) and city_map[row][col] > 0:
                text_surface = font.render(str(city_map[row][col]), True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col*cell_size + cell_size // 2, offset_y + row*cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)
            elif isinstance(city_map[row][col], str) and city_map[row][col].startswith('F'):
                text_surface = font.render(city_map[row][col], True, BLACK)
                text_rect = text_surface.get_rect(center=(offset_x + col*cell_size + cell_size // 2, offset_y + row*cell_size + cell_size // 2))
                screen.blit(text_surface, text_rect)
    # Display elapsed time
    if elapsed_time is not None:
        time_text = font.render(f"Elapsed Time: {elapsed_time} seconds", True, BLACK)
        screen.blit(time_text, (20, 20))

    # Highlight current position
    if current_position:
        pygame.draw.rect(screen, YELLOW, (offset_x + current_position[1] * cell_size, offset_y + current_position[0] * cell_size, cell_size, cell_size), 3)


# Draw the path function
def draw_path(screen, segments, color):
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    draw_map(screen, city_map, current_position, elapsed_time)

    if level == 1:
        path = uniform_cost_search(city_map, start_pos, goal_pos)
    elif level == 2:
        # Implement pathfinding for Level 2
        path = uniform_cost_search(city_map, current_position, goal_pos)
    elif level == 3:
        # Implement pathfinding for Level 3 with fuel and gas stations
        pass  # Placeholder for Level 3 pathfinding

    if path:
        if current_position == goal_pos:
            break

        next_position = path[1]
        time.sleep(1)  # Adjust delay for visualization

        # Calculate elapsed time and move to next position
        if isinstance(city_map[current_position[0]][current_position[1]], int):
            elapsed_time += 1 + city_map[current_position[0]][current_position[1]]
        else:
            elapsed_time += 1

        # Add segment to draw path
        segments.append((current_position, next_position))
        
        current_position = next_position

    # Draw path segments
    draw_path(screen, segments, RED)

    pygame.display.flip()

# After the main loop ends
if current_position == goal_pos:
    print(f"Reached the goal in {elapsed_time} seconds.")
else:
    print("Path not found.")

time.sleep(10)

pygame.quit()
sys.exit()
