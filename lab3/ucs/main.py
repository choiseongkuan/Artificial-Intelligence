from queue import PriorityQueue


class CompareAble:
    def __init__(self, index, cost, step):
        self.index = index
        self.cost = cost
        self.step = step

    def __lt__(self, other):
        return self.cost < other.cost


def get_maze():
    matrix = []
    with open('mazedata.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            tmp = []
            line = line.strip()
            for ele in line:
                tmp.append(ele)
            matrix.append(tmp)
    return matrix


def get_cost(now, goal):
    return abs(goal[0] - now[0]) + abs(goal[1] - now[1])


def bfs(maze, start, end):
    deep = 0
    direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    visited = set()
    path = {}
    q = PriorityQueue()
    q.put(CompareAble(start, get_cost(start, end), 0))
    visited.add(start)
    while not q.empty():
        deep += 1
        tmp = q.get()
        x, y = tmp.index
        step = tmp.step
        if (x, y) == end:
            print(deep)
            return path
        for dx, dy in direction:
            new_x, new_y = x+dx, y+dy
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '1' and (new_x, new_y) not in visited:
                q.put(CompareAble((new_x, new_y), get_cost((new_x, new_y), end)+step+1, step+1))
                visited.add((new_x, new_y))
                path[(new_x, new_y)] = (x, y)
    return None


def get_direction(x1, y1, x2, y2):
    if x1-x2 == 0 and y1-y2 == 1:
        return '←'
    if x1-x2 == 0 and y1-y2 == -1:
        return '→'
    if x1-x2 == 1 and y1-y2 == 0:
        return '↑'
    if x1-x2 == -1 and y1-y2 == 0:
        return '↓'


def print_path(maze_path, start, end, maze_map):
    path_len = 0
    path_list = [end]
    next_v = maze_path[end]
    path_len += 1
    prev_xy = end
    while True:
        if next_v != start:
            path_len += 1
            maze_map[next_v[0]][next_v[1]] = get_direction(next_v[0], next_v[1], prev_xy[0], prev_xy[1])
            path_list.append(next_v)
            prev_xy = next_v
            next_v = maze_path[next_v]
        else:
            break
    path_list.append(start)
    path_len += 1
    for index in reversed(path_list):
        print(index, end=", ")
    print("\n")
    for x in range(0, len(maze_map)):
        for y in range(0, len(maze_map[x])):
            print(maze_map[x][y], end=" ")
        print("\n")
    print(f"path length is {path_len}")

maze = get_maze()
visited = set()
for x in range(0, len(maze)):
    for y in range(0, len(maze[x])):
        if maze[x][y] == 'S':
            maze_S = (x, y)
        if maze[x][y] == 'E':
            maze_E = (x, y)
path = bfs(maze, maze_S, maze_E)
print_path(path, maze_S, maze_E, maze)



