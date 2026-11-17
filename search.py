def neighbors(env, row, col):
    direction = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    result = []
    for dr, dc in direction:
        new_row = row + dr
        new_col = col + dc
        if not env.is_wall(new_row, new_col):
            result.append((new_row, new_col))
    return result

def bfs_distance(env, start, target):
    queue = [(start, 0)]
    visited = [(start)]
    while len(queue) > 0:
        (row, col), dis = queue.pop(0)
        if (row, col) == target:
            return dis
        neighbor = neighbors(env, row, col)
        for (nrow, ncol) in neighbor:
            if (nrow, ncol) not in visited:
                visited.append((nrow, ncol))
                queue.append(((nrow, ncol), dis + 1))
    return None

def find_path(env, start, target):
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }
    queue = [(start, [])]
    visited = [start]
    while (len(queue)) > 0 :
        (row, col), path = queue.pop(0)
        if (row, col) == target:
            return path
        for action, (dr, dc) in moves.items():
            nrow = row + dr
            ncol = col + dc
            if not env.is_wall(nrow, ncol) and (nrow, ncol) not in visited:
                visited.append((nrow, ncol))
                queue.append(((nrow, ncol), path + [action]))
    return None