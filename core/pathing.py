import math
from core import priodict


def astar(start, goal, data):
    closedset = set()
    openset = set()
    openset.add(start)

    came_from = {}

    g_score = {}
    g_score[start] = 0

    f_score = priodict.priorityDictionary()
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal)

    while len(openset) != 0:
        current = f_score.smallest()
        del f_score[current]

        if current == goal:
            return reconstruct_path(came_from, goal)

        openset.remove(current)
        closedset.add(current)
        for neighbor in neighbor_nodes(current, data):
            tentative_g_score = g_score[current] + dist_between(current, neighbor)
            if neighbor in closedset and tentative_g_score >= g_score[neighbor]:
                continue

            if neighbor not in openset or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                if neighbor not in openset:
                    openset.add(neighbor)
    return None


def heuristic_cost_estimate(start, goal):
    return dist_between(start, goal)


def dist_between(pos1, pos2):
    return math.sqrt(math.pow(pos2[0] - pos1[0], 2) + math.pow(pos2[1] - pos1[1], 2))


def neighbor_nodes(current, data):
    neighbor_list = []

    height, width = len(data), len(data[0])

    for y in range(current[1] - 1, current[1] + 2):
        for x in range(current[0] - 1, current[0] + 2):
            if not (x == current[0] and y == current[1]):
                if x >= 0 and y >= 0 and x < width and y < height:
                    if data[y][x]:
                        neighbor_list.append((x, y))

    return neighbor_list


def reconstruct_path(came_from, current_node):
    if current_node in came_from:
        p = reconstruct_path(came_from, came_from[current_node])
        p.append(current_node)
        return p
    else:
        return [current_node, ]