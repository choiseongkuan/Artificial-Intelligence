from queue import PriorityQueue
import copy


class Node:
    def __init__(self, board, blank_pos, moves, heuristic, parent, action):
        self.board = board
        self.blank_pos = blank_pos
        self.moves = moves
        self.heuristic = heuristic
        self.parent = parent
        self.action = action

    def __hash__(self):
        return hash(tuple(self.board))

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.heuristic + self.moves < other.heuristic + other.moves

    def move(self, direction):
        illegal_action = {-4: [0, 1, 2, 3], 4: [12, 13, 14, 15], -1: [0, 4, 8, 12], 1: [3, 7, 11, 15]}  # 出界区域
        if self.blank_pos not in illegal_action[direction]:
            new_board = copy.deepcopy(self.board)
            new_blank_pos = self.blank_pos + direction
            new_board[self.blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[self.blank_pos]
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
        for j in range(0, len(row)):
            if row[j] == 0:
                blank_pos = i * 4 + j
        board.extend(row)
    return board, blank_pos


def print_ans(puzzle_node):
    print(f"Lower Bound {puzzle_node.moves} moves")
    path = []
    while puzzle_node.parent is not None:
        path.append(puzzle_node.action)
        puzzle_node = puzzle_node.parent
    for node in reversed(path):
        print(node, end=" ")


def search(current_state, limit, path, closed, moves):
    f = current_state.moves + current_state.heuristic
    if f > limit:
        return None, f
    if current_state.board == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]:
        return current_state, f
    min_f = float('inf')
    direction = [-4, 4, -1, 1]
    for dire in direction:
        next_state = current_state.move(dire)
        if next_state is not None and next_state not in closed:
            path.append(next_state)
            closed.add(next_state)
            found, new_limit = search(next_state, limit, path, closed, moves+1)
            if found is not None:
                return found, new_limit
            min_f = min(min_f, new_limit)
            path.pop()
            closed.remove(next_state)
    return None, min_f


def ida_star(puzzle_board, blank_pos):
    init_state = Node(puzzle_board, blank_pos, 0, get_heuristic(puzzle_board), None, -1)
    limit = get_heuristic(puzzle_board)
    path = []
    closed = set()
    found = None
    while found is None:
        found, limit = search(init_state, limit, path, closed, 0)
        if found is not None:
            return found
        else:
            print(f"当前迭代深度：{limit}")


if __name__ == "__main__":
    puzzle = get_puzzle()
    ans = ida_star(puzzle[0], puzzle[1])
    print_ans(ans)
