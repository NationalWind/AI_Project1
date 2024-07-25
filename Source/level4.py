import pygame
import heapq
import time
import random

# Initialize the game
pygame.init()

# Set up the screen
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Node:
    def __init__(self, state, path_cost, parent):
        self.state = state
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other):
        return self.state[3] > other.state[3]


def fn(node, goal_state):
    return node.path_cost + abs(goal_state[0] - node.state[0]) + abs(goal_state[1] - node.state[1]), node


def A_star(n, m, f, start_state, goal_state, grid, cur_state, gantt, agent_idx, time_shift):
    node = Node(start_state, 0, None)
    frontier = []
    heapq.heappush(frontier, fn(node, goal_state))
    reached = {node.state: node}
    while frontier:
        node = heapq.heappop(frontier)[1]
        if node.state[3] < 0 or node.state[5] < 0:
            continue
        if (node.state[0], node.state[1]) == (goal_state[0], goal_state[1]):
            return node
        for child in expand(node, n, m, f, grid, cur_state, gantt, agent_idx, time_shift):
            s = child.state
            if reached.get(s) is None or child.path_cost < reached[s].path_cost:
                reached[s] = child
                heapq.heappush(frontier, fn(child, goal_state))


# state = (i, j, rwt, rt, rwt_f, rf)
# path_cost = (dist)
# grid[i][j] = {-1, >= 0 (rwt), F1, Sx, Gx}
def expand(node, n, m, f, grid, cur_state, gantt, agent_idx, time_shift):
    children = []
    moves = [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0]]
    i, j, rwt, rt, rwt_f, rf = node.state
    # if cur_state[agent_idx][0] == 5 and cur_state[agent_idx][1] == 3:
    #     breakpoint()
    dist = node.path_cost

    for move in moves:
        # duplicate when stopped
        u = i + move[0]
        v = j + move[1]

        if (
            u < 0
            or u >= n
            or v < 0
            or v >= m
            or grid[u][v] == "-1"
            # or (any(state and s_idx != agent_idx and (state[0], state[1]) == (u, v) for s_idx, state in enumerate(gantt[rt])))
            or (rt - 1 - time_shift >= 0 and any(state and (s_idx < agent_idx or 0) and (state[0], state[1]) == (u, v) for s_idx, state in enumerate(gantt[rt - 1 - time_shift])))
            or (
                rt - 1 - time_shift >= 0
                and any(
                    next and cur and s_idx < agent_idx and (next[0], next[1]) == (i, j) and (cur[0], cur[1]) == (u, v)
                    for s_idx, (next, cur) in enumerate(zip(gantt[rt - 1 - time_shift], gantt[rt - time_shift]))
                )
            )
        ):
            continue

        if grid[u][v][0] in ["F", "S", "G"]:
            guv = 0
        else:
            guv = int(grid[u][v])

        if grid[i][j][0] == "F":
            wt_f = int(grid[i][j][1:])

            if rf == 0:
                if move == [0, 0]:
                    if wt_f - 1 == 0:
                        children.append(Node((i, j, 0, rt - 1, 0, f), dist, node))
                    else:
                        children.append(Node((i, j, 0, rt - 1, wt_f - 1, 0), dist, node))
            else:  # state = (i, j, rwt, rt, rwt_f, rf)
                if rwt_f == 0:
                    if move == [0, 0]:
                        children.append(Node((i, j, 0, rt - 1, -1, f), dist, node))
                    children.append(Node((u, v, 0, rt - 1, -1, f - 1), dist + 1, node))
                elif rwt_f == -1:
                    if move == [0, 0]:
                        if wt_f - 1 == 0:
                            children.append(Node((i, j, 0, rt - 1, 0, f), dist, node))
                        else:
                            children.append(Node((i, j, 0, rt - 1, wt_f - 1, rf), dist, node))
                    children.append(Node((u, v, rwt + guv, rt - 1, -1, rf - 1), dist + 1, node))  # move, diste + 1, fuel -1
                else:
                    if move == [0, 0]:
                        if rwt_f > 1:
                            children.append(Node((i, j, 0, rt - 1, rwt_f - 1, rf), dist, node))
                        else:
                            children.append(Node((i, j, 0, rt - 1, 0, f), dist, node))

            continue

        if grid[i][j][0] in ["S", "G"]:
            gij = 0
        else:
            gij = int(grid[i][j])

        if gij > 0:
            if rwt > 0:
                if move == [0, 0]:
                    children.append(Node((i, j, rwt - 1, rt - 1, 0, rf), dist, node))
            else:
                if move == [0, 0]:
                    children.append(Node((i, j, 0, rt - 1, -1, rf), dist, node))
                children.append(Node((u, v, 0 + guv, rt - 1, -1, rf - 1), dist + 1, node))
        else:  # grid[i][j] == '0'
            if move == [0, 0]:
                children.append(Node((i, j, 0, rt - 1, -1, rf), dist, node))
            children.append(Node((u, v, 0 + guv, rt - 1, -1, rf - 1), dist + 1, node))

    return children


def trace(node):
    # if node is not None:
    #     print(node.state, node.path_cost)

    depth = 0
    path = []
    while node is not None:
        depth += 1
        path.append(node.state)
        node = node.parent
    return (
        path,
        depth - 1,
    )


def main():
    with open("input1_level1.txt") as inp:
        n, m, t, f = map(int, (inp.readline().split()))

        grid = [[] for _ in range(n)]
        for i in range(n):
            grid[i] = inp.readline().split()

        start_goal = [[[-1, -1], [-1, -1]] for _ in range(10)]  # coord

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

        n_agents = len(start_goal)
        # i, j, rwt, rt, rwt_f, rf
        cur_state = [(*start_goal[i][0], 0, t, -1, f) for i in range(n_agents)]
        gantt = [[[] for _ in range(n_agents)] for _ in range(t + 1)]

        def draw_grid_with_text_in_the_middle():
            for i in range(n):
                for j in range(m):
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        (
                            j * SCREEN_WIDTH // m + 3,
                            i * SCREEN_HEIGHT // n + 3,
                            SCREEN_WIDTH // m - 6,
                            SCREEN_HEIGHT // n - 6,
                        ),
                    )

                    font = pygame.font.Font(None, 36)
                    text = font.render(grid[i][j], True, (0, 0, 0))
                    screen.blit(text, (j * SCREEN_WIDTH // m + 10, i * SCREEN_HEIGHT // n + 10))

            pygame.display.update()

        def draw_cur_states():
            for i in range(n_agents):
                pygame.draw.circle(
                    screen,
                    (i * 20, i * 10 + 100, 20),
                    (
                        cur_state[i][1] * SCREEN_WIDTH // m + SCREEN_WIDTH // m // 2,
                        cur_state[i][0] * SCREEN_HEIGHT // n + SCREEN_HEIGHT // n // 2,
                    ),
                    10,
                )

                font = pygame.font.Font(None, 36)
                text = font.render(
                    # f"({cur_state[i][2]}, {cur_state[i][3]}, {cur_state[i][4]}, {cur_state[i][5]})",
                    f"A{i}, {cur_state[0][3]}, {cur_state[i][5]}",
                    True,
                    (0, 0, 0),
                )
                screen.blit(
                    text,
                    (
                        cur_state[i][1] * SCREEN_WIDTH // m + 10,
                        cur_state[i][0] * SCREEN_HEIGHT // n + 10,
                    ),
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

        draw_grid_with_text_in_the_middle()
        draw_cur_states()
        pygame.time.set_timer(pygame.USEREVENT + 1, 200)
        running = True
        i = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    if [cur_state[0][0], cur_state[0][1]] != start_goal[0][1] or i > 0:
                        if start_goal[i][1] == [-1, -1]:
                            update_new_goal(i)
                        node = A_star(n, m, f, cur_state[i], (*start_goal[i][1], 0, 0, -1, 0), grid, cur_state, gantt, i, max(0, cur_state[i][3] - cur_state[0][3] - 1))
                        path = trace(node)[0]
                        if not path:
                            if i == 0:
                                print("Not OK")
                                running = False
                                break
                            else:
                                for tp in range(0, cur_state[i][3]):
                                    gantt[tp][i] = cur_state[i]
                                i = (i + 1) % n_agents
                                continue
                        for state in path:
                            gantt[state[3]][i] = state
                        path.pop()
                        cur_state[i] = path[-1]
                        path.pop()
                        if i > 0:
                            # it will randomly generate a valid destination on the map (i.e., not on obstacles, or other vehicles)
                            if (cur_state[i][0], cur_state[i][1]) == tuple(start_goal[i][1]):
                                start_goal[i][1] = [-1, -1]

                        if i == n_agents - 1:
                            draw_grid_with_text_in_the_middle()
                            draw_cur_states()
                        i = (i + 1) % n_agents
                    else:
                        print("OK")
                        running = False
                        break
                if event.type == pygame.QUIT:
                    running = False


# main()
# pygame.quit()