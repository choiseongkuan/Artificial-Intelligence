import time
node_num = 0


class Node:
    def __init__(self, board, moves, heuristic, parent):
        self.board = board
        self.moves = moves
        self.heuristic = heuristic
        self.parent = parent

    def __hash__(self):
        return hash(self.board)

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        if self.heuristic + self.moves == other.heuristic + other.moves:
            return self.heuristic < other.heuristic
        return self.heuristic + self.moves < other.heuristic + other.moves

    def move(self, direction):
        illegal_action = {-4: (0, 1, 2, 3), 4: (12, 13, 14, 15), -1: (0, 4, 8, 12), 1: (3, 7, 11, 15)}  # 出界区域
        blank_pos = self.board.index(0)
        if blank_pos not in illegal_action[direction]:
            new_board = list(self.board)
            new_blank_pos = blank_pos + direction
            new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
            new_moves = self.moves + 1
            new_heuristic = get_heuristic(new_board)
            new_board = tuple(new_board)
            return Node(new_board, new_moves, new_heuristic, self)
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
    for i in range(4):
        row = list(map(int, input().split()))
        board.extend(row)
    return board


def print_ans(puzzle_node):
    print(f"Lower Bound {puzzle_node.moves} moves")
    path = []
    parent_node = puzzle_node.parent
    while puzzle_node.parent is not None:
        action = parent_node.board[puzzle_node.board.index(0)]
        path.append(action)
        puzzle_node = parent_node
        parent_node = parent_node.parent
    for node in reversed(path):
        print(node, end=" ")
    print("\n")


def generate_node(current_state, closed):
    direction = (-4, 4, -1, 1)
    next_states = []
    for dire in direction:
        next_state = current_state.move(dire)
        if next_state is not None and next_state not in closed:
            next_states.append(next_state)
    next_states = sorted(next_states)
    return next_states


def search(current_state, limit, closed, moves):
    global node_num  # 访问状态计数
    node_num += 1
    f = current_state.moves + current_state.heuristic  # 计算f值
    if f > limit:  # f值超过阈值则返回
        return None, f
    if current_state.board == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0):
        return current_state, f
    min_f = float('inf')  # 所有超出阈值的子状态中的最小阈值
    next_states = generate_node(current_state, closed)  # 子状态列表
    for next_state in next_states:  # 遍历子状态
        closed.add(next_state)  # 加入closed进行环检测
        found, new_limit = search(next_state, limit, closed, moves+1)  # 判断是否找到目标并获取新的阈值
        if found is not None:  # 找到目标状态
            return found, new_limit
        min_f = min(min_f, new_limit)  # 更新min_f为最小阈值
        closed.remove(next_state)  # 回溯
    return None, min_f


def ida_star(puzzle_board):
    init_state = Node(puzzle_board, 0, get_heuristic(puzzle_board), None)
    limit = get_heuristic(puzzle_board)
    closed = set()
    found = None
    while found is None:
        found, limit = search(init_state, limit, closed, 0)
        if found is not None:
            return found
        else:
            print(f"当前迭代深度：{limit}")


if __name__ == "__main__":
    puzzle = get_puzzle()
    time_start = time.time()
    ans = ida_star(puzzle)
    time_end = time.time()
    print(f"expanded {node_num} nodes")
    print_ans(ans)
    print(f"Used time {time_end - time_start} sec")