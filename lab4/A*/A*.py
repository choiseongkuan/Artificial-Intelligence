from queue import PriorityQueue
import time
import copy
node_num = 0


class Node:
    def __init__(self, board, blank_pos, moves, heuristic, parent, action):
        self.board = board  # puzzle
        self.blank_pos = blank_pos  # 空格位置
        self.moves = moves  # 移动次数
        self.heuristic = heuristic  # 启发值
        self.parent = parent  # 父状态
        self.action = action  # 记录此状态时由上状态的哪个数字移动而来

    def __hash__(self):
        return hash(tuple(self.board))

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):  # 对f进行升序排序，当f相等时对hx进行升序排序
        if self.heuristic + self.moves == other.heuristic + other.moves:
            return self.heuristic < other.heuristic
        return self.heuristic + self.moves < other.heuristic + other.moves

    def move(self, direction):  # 生成移动后的状态
        illegal_action = {-4: [0, 1, 2, 3], 4: [12, 13, 14, 15], -1: [0, 4, 8, 12], 1: [3, 7, 11, 15]}  # 出界区域
        if self.blank_pos not in illegal_action[direction]:  # 判断本次移动是否会出界
            new_board = copy.deepcopy(self.board)
            new_blank_pos = self.blank_pos + direction
            new_board[self.blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[self.blank_pos]  # 将要移动的数字与空格交换位置
            new_moves = self.moves + 1
            new_heuristic = get_heuristic(new_board)
            new_action = self.board[new_blank_pos]
            return Node(new_board, new_blank_pos, new_moves, new_heuristic, self, new_action)
        else:
            return None


# def get_heuristic(board):  # Hamming distance
#     heuristic = 0
#     for i in range(0, len(board) - 1):
#         if i + 1 != board[i]:
#             heuristic += 1
#     if board[15] != 0:
#         heuristic += 1
#     return heuristic

# def get_heuristic(board):  # Manhattan distance
#     heuristic = 0
#     for i in range(0, len(board)-1):
#         x = i // 4
#         y = i % 4
#         target_pos = board.index(i+1)
#         target_x = target_pos // 4
#         target_y = target_pos % 4
#         heuristic += abs(x-target_x) + abs(y-target_y)
#     return heuristic


# def get_heuristic(board):  # Manhattan distance
#     heuristic = 0
#     for i in range(0, len(board)-1):
#         x = i // 4
#         y = i % 4
#         target_pos = board.index(i+1)
#         target_x = target_pos // 4
#         target_y = target_pos % 4
#         heuristic += abs(x-target_x) + abs(y-target_y)
#     return heuristic


def get_manhattan(board):
    heuristic = 0
    for i in range(0, len(board)-1):
        x = i // 4
        y = i % 4
        target_pos = board.index(i+1)
        target_x = target_pos // 4
        target_y = target_pos % 4
        heuristic += abs(x-target_x) + abs(y-target_y)
    return heuristic


def get_heuristic(board):  # Linear_conflict
    cost = 0
    for row in range(4):
        for i in range(3):
            if board[row*4+i] == row*4+i+2 and board[row*4+i+1] == row*4+i+1:
                # print(f"{board[row * 4 + i]} and {board[row * 4 + i+1]} in row {row}")
                cost += 2
    for col in range(4):
        for i in range(3):
            if board[col+i*4] == col+(i+1)*4+1 and board[col+(i+1)*4] == col+i*4+1:
                # print(f"{board[col + i * 4]} and {board[col + (i+1) * 4]} in col {col}")
                cost += 2
    return cost + get_manhattan(board)


def get_puzzle():
    board = []
    blank_pos = 0
    for i in range(4):
        row = list(map(int, input().split()))
        for j in range(0, len(row)):
            if row[j] == 0:
                blank_pos = i * 4 + j
        board.extend(row)
    return board, blank_pos


def print_ans(puzzle_node):  # 打印结果
    print(f"Lower Bound {puzzle_node.moves} moves")  # 打印最终移动次数
    path = []
    while puzzle_node.parent is not None:  # 往上回溯所记录的移动操作
        path.append(puzzle_node.action)
        puzzle_node = puzzle_node.parent
    for node in reversed(path):  # 打印移动操作
        print(node, end=" ")
    print("\n")


def update_path(state, open_list):  # 更新open list中moves更短的结点
    for state_so_far in open_list:
        if state_so_far.board == state.board and state_so_far.moves > state.moves:  # 发现新状态的moves小于open list中该状态的moves则更新
            state_so_far.moves = state.moves
            state_so_far.parent = state.parent
            return True
    return False


def astar(puzzle_board, blank_pos):
    global node_num  # 访问状态计数
    closed = set()
    open_que = PriorityQueue()
    open_list = []
    init_state = Node(puzzle_board, blank_pos, 0, get_heuristic(puzzle_board), None, -1)  # 初始状态
    open_que.put(init_state)  # 初始化优先队列
    open_list.append(init_state)  # 初始化open list
    closed.add(init_state)  # 初始化 closed list
    direction = [-4, 4, -1, 1]
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    while not open_que.empty():
        current_state = open_que.get()  # 获取f值最小的状态
        node_num += 1
        open_list.remove(current_state)  # 从open list 移除该状态
        if current_state.board == goal:  # 找到目标状态
            return current_state
        for dire in direction:  # 遍历四个可能的移动操作
            next_state = current_state.move(dire)
            if next_state is not None and next_state not in closed:  # 判断新状态合法且并不在closed list
                if update_path(next_state, open_list):  # 当新状态已存在open list则更新
                    continue
                # 不在open list时
                open_que.put(next_state)  # 入队
                open_list.append(next_state)  # 加入open list
    return None


if __name__ == "__main__":
    puzzle = get_puzzle()
    time_start = time.time()
    ans = astar(puzzle[0], puzzle[1])
    time_end = time.time()
    print(f"expanded {node_num} nodes")
    print_ans(ans)
    print(f"Used time {time_end - time_start} sec")