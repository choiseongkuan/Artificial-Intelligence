from queue import PriorityQueue
import time


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


def get_heuristic(board):  # Manhattan distance
    heuristic = 0
    for i in range(0, len(board)-1):
        x = i // 4
        y = i % 4
        target_pos = board.index(i+1)
        target_x = target_pos // 4
        target_y = target_pos % 4
        heuristic += abs(x-target_x) + abs(y-target_y)
    return heuristic


def get_puzzle():
    board = []
    blank_pos = 0
    for i in range(4):
        row = list(map(int, input().split()))
        board.extend(row)
    return tuple(board)


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


def astar(puzzle_board):
    node_num = 0
    closed = set()
    open_que = PriorityQueue()
    init_state = Node(puzzle_board, 0, get_heuristic(puzzle_board), None)
    open_que.put(init_state)
    closed.add(init_state)
    direction = (-4, 4, -1, 1)
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

    while not open_que.empty():
        current_state = open_que.get()
        node_num += 1
        if current_state.board == goal:
            closed.add(current_state)
            print(node_num)
            return current_state
        for dire in direction:
            next_state = current_state.move(dire)
            if next_state is not None and next_state not in closed:
                open_que.put(next_state)
                closed.add(next_state)
    return None


if __name__ == "__main__":
    puzzle = get_puzzle()
    time_start = time.time()
    ans = astar(puzzle)
    time_end = time.time()
    print_ans(ans)
    print(f"Used time {time_end - time_start} sec")
