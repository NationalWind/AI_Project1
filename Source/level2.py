from queue import PriorityQueue

# Uniform Cost Search implementation with minimum cells and time constraint
def find_path_level2(city_map, start, goal, max_time):
    frontier = PriorityQueue()
    frontier.put((0, 0, start))  # (cost, cells, (row, col))
    came_from = {start: None}
    cost_so_far = {start: (0, 0)}  # (cost, cells)

    while not frontier.empty():
        current_cost, current_cells, current = frontier.get()

        if current == goal:
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_node = (next_row, next_col)

            if 0 <= next_row < len(city_map) and 0 <= next_col < len(city_map[0]):
                if city_map[next_row][next_col] == -1:
                    continue

                move_cost = 1
                if isinstance(city_map[next_row][next_col], int) and city_map[next_row][next_col] > 0:
                    move_cost += city_map[next_row][next_col] 

                new_cost = current_cost + move_cost
                new_cells = current_cells + 1

                if new_cost <= max_time:
                    if next_node not in cost_so_far or (new_cost < cost_so_far[next_node][0] or (new_cost == cost_so_far[next_node][0] and new_cells < cost_so_far[next_node][1])):
                        cost_so_far[next_node] = (new_cost, new_cells)
                        priority = new_cost
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