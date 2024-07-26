import pygame
import heapq
import time
import random


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
            or (
                rt - 1 - time_shift >= 0
                and any(
                    state and (s_idx < agent_idx or (gantt[rt - time_shift][s_idx][0], gantt[rt - time_shift][s_idx][1]) == (u, v)) and (state[0], state[1]) == (u, v)
                    for s_idx, state in enumerate(gantt[rt - 1 - time_shift])
                )
            )
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
                    children.append(Node((u, v, 0 + guv, rt - 1, -1, f - 1), dist + 1, node))
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
