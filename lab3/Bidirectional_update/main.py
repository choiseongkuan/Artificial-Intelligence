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
    path = {}
    q_start = PriorityQueue()
    q_start.put(CompareAble(start, get_cost(start, end), 0))
    q_end = PriorityQueue()
    q_end.put(CompareAble(end, get_cost(end, start), 0))
    path[start] = ((-1, -1), "start")
    path[end] = ((-1, -1), "end")
    while not q_start.empty() and not q_end.empty():
        deep += 1
        tmp = q_start.get()
        x, y = tmp.index
        step = tmp.step
        for dx, dy in direction:
            new_x, new_y = x+dx, y+dy
            if (new_x, new_y) not in path:
                if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '1':
                    q_start.put(CompareAble((new_x, new_y), get_cost((new_x, new_y), end)+step+1, step+1))
                    path[(new_x, new_y)] = ((x, y), "start")
            else:
                if path[(new_x, new_y)][1] == "end":
                    path[(new_x, new_y)] = ((x, y), path[(new_x, new_y)][0], "end")
                    print(deep)
                    return path, (new_x, new_y)

        tmp = q_end.get()
        x, y = tmp.index
        step = tmp.step
        for dx, dy in direction:
            new_x, new_y = x+dx, y+dy
            if (new_x, new_y) not in path:
                if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '1':
                    q_end.put(CompareAble((new_x, new_y), get_cost((new_x, new_y), start)+step+1, step+1))
                    path[(new_x, new_y)] = ((x, y), "end")
            else:
                if path[(new_x, new_y)][1] == "start":
                    path[(new_x, new_y)] = (path[(new_x, new_y)][0], (x, y), "start")
                    print(deep)
                    return path, (new_x, new_y)
    return None


def get_direction_start(x1, y1, x2, y2):
    if x1 - x2 == 0 and y1 - y2 == 1:
        return '←'
    if x1 - x2 == 0 and y1 - y2 == -1:
        return '→'
    if x1 - x2 == 1 and y1 - y2 == 0:
        return '↑'
    if x1 - x2 == -1 and y1 - y2 == 0:
        return '↓'


def get_direction_end(x1, y1, x2, y2):
    if x1 - x2 == 0 and y1 - y2 == 1:
        return '→'
    if x1 - x2 == 0 and y1 - y2 == -1:
        return '←'
    if x1 - x2 == 1 and y1 - y2 == 0:
        return '↓'
    if x1 - x2 == -1 and y1 - y2 == 0:
        return '↑'


def print_path(maze_path, start, end, maze_map, last_v):
    path_len = 0
    path_list_start = [last_v]
    next_v = maze_path[last_v][0]
    path_len += 1
    prev_xy = last_v
    maze_map[prev_xy[0]][prev_xy[1]] = get_direction_start(next_v[0], next_v[1], prev_xy[0], prev_xy[1])
    while True:
        if next_v != start:
            path_len += 1
            maze_map[next_v[0]][next_v[1]] = get_direction_start(next_v[0], next_v[1], prev_xy[0], prev_xy[1])
            path_list_start.append(next_v)
            prev_xy = next_v
            next_v = maze_path[next_v][0]
        else:
            break
    path_list_start.append(start)
    path_len += 1
    next_v = maze_path[last_v][1]
    prev_xy = last_v
    path_list_end = []
    while True:
        if next_v != end:
            path_len += 1
            maze_map[next_v[0]][next_v[1]] = get_direction_end(next_v[0], next_v[1], prev_xy[0], prev_xy[1])
            path_list_end.append(next_v)
            prev_xy = next_v
            next_v = maze_path[next_v][0]
        else:
            break
    path_len += 1
    path_list_end.append(end)
    path_list_end = reversed(path_list_end)
    path_list = []
    path_list.extend(path_list_end)
    path_list.extend(path_list_start)
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
path, last = bfs(maze, maze_S, maze_E)
print_path(path, maze_S, maze_E, maze, last)



