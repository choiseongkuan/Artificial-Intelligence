import copy
from ChessBoard import *


class Evaluate(object):
    # 棋子棋力得分
    single_chess_point = {
        'c': 989,   # 车
        'm': 439,   # 马
        'p': 442,   # 炮
        's': 226,   # 士
        'x': 210,   # 象
        'z': 55,    # 卒
        'j': 65536  # 将
    }
    # 红兵（卒）位置得分
    red_bin_pos_point = [
        [1, 3, 9, 10, 12, 10, 9, 3, 1],
        [18, 36, 56, 95, 118, 95, 56, 36, 18],
        [15, 28, 42, 73, 80, 73, 42, 28, 15],
        [13, 22, 30, 42, 52, 42, 30, 22, 13],
        [8, 17, 18, 21, 26, 21, 18, 17, 8],
        [3, 0, 7, 0, 8, 0, 7, 0, 3],
        [-1, 0, -3, 0, 3, 0, -3, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 红车位置得分
    red_che_pos_point = [
        [185, 195, 190, 210, 220, 210, 190, 195, 185],
        [185, 203, 198, 230, 245, 230, 198, 203, 185],
        [180, 198, 190, 215, 225, 215, 190, 198, 180],
        [180, 200, 195, 220, 230, 220, 195, 200, 180],
        [180, 190, 180, 205, 225, 205, 180, 190, 180],
        [155, 185, 172, 215, 215, 215, 172, 185, 155],
        [110, 148, 135, 185, 190, 185, 135, 148, 110],
        [100, 115, 105, 140, 135, 140, 105, 115, 110],
        [115, 95, 100, 155, 115, 155, 100, 95, 115],
        [20, 120, 105, 140, 115, 150, 105, 120, 20]
    ]
    # 红马位置得分
    red_ma_pos_point = [
        [80, 105, 135, 120, 80, 120, 135, 105, 80],
        [80, 115, 200, 135, 105, 135, 200, 115, 80],
        [120, 125, 135, 150, 145, 150, 135, 125, 120],
        [105, 175, 145, 175, 150, 175, 145, 175, 105],
        [90, 135, 125, 145, 135, 145, 125, 135, 90],
        [80, 120, 135, 125, 120, 125, 135, 120, 80],
        [45, 90, 105, 190, 110, 90, 105, 90, 45],
        [80, 45, 105, 105, 80, 105, 105, 45, 80],
        [20, 45, 80, 80, -10, 80, 80, 45, 20],
        [20, -20, 20, 20, 20, 20, 20, -20, 20]
    ]
    # 红炮位置得分
    red_pao_pos_point = [
        [190, 180, 190, 70, 10, 70, 190, 180, 190],
        [70, 120, 100, 90, 150, 90, 100, 120, 70],
        [70, 90, 80, 90, 200, 90, 80, 90, 70],
        [60, 80, 60, 50, 210, 50, 60, 80, 60],
        [90, 50, 90, 70, 220, 70, 90, 50, 90],
        [120, 70, 100, 60, 230, 60, 100, 70, 120],
        [10, 30, 10, 30, 120, 30, 10, 30, 10],
        [30, -20, 30, 20, 200, 20, 30, -20, 30],
        [30, 10, 30, 30, -10, 30, 30, 10, 30],
        [20, 20, 20, 20, -10, 20, 20, 20, 20]
    ]
    # 红将位置得分
    red_jiang_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9750, 9800, 9750, 0, 0, 0],
        [0, 0, 0, 9900, 9900, 9900, 0, 0, 0],
        [0, 0, 0, 10000, 10000, 10000, 0, 0, 0],
    ]
    # 红相或士位置得分
    red_xiang_shi_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 60, 0, 0, 0, 60, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [80, 0, 0, 80, 90, 80, 0, 0, 80],
        [0, 0, 0, 0, 0, 120, 0, 0, 0],
        [0, 0, 70, 100, 0, 100, 70, 0, 0],
    ]

    red_pos_point = {
        'z': red_bin_pos_point,
        'm': red_ma_pos_point,
        'c': red_che_pos_point,
        'j': red_jiang_pos_point,
        'p': red_pao_pos_point,
        'x': red_xiang_shi_pos_point,
        's': red_xiang_shi_pos_point
    }

    def __init__(self, team):
        self.team = team

    def get_single_chess_point(self, chess: Chess):
        if chess.team == self.team:
            return self.single_chess_point[chess.name]
        else:
            return -1 * self.single_chess_point[chess.name]

    def get_chess_pos_point(self, chess: Chess):
        red_pos_point_table = self.red_pos_point[chess.name]
        if chess.team == 'r':
            pos_point = red_pos_point_table[chess.row][chess.col]
        else:
            pos_point = red_pos_point_table[9 - chess.row][chess.col]
        if chess.team != self.team:
            pos_point *= -1
        return pos_point

    def evaluate(self, chessboard: ChessBoard):
        point = 0
        for chess in chessboard.get_chess():
            point += self.get_single_chess_point(chess)
            point += self.get_chess_pos_point(chess)
        return point


class ChessMap(object):
    def __init__(self, chessboard: ChessBoard):
        self.chess_map = copy.deepcopy(chessboard.chessboard_map)


class ChessAI(object):
    def __init__(self, computer_team):
        self.team = computer_team
        self.max_depth = 5
        self.old_pos = [0, 0]
        self.new_pos = [0, 0]
        self.evaluate_class = Evaluate(self.team)

    def get_next_step(self, chessboard: ChessBoard):
        chess_num = len(chessboard.get_chess())
        if chess_num > 14:
            self.max_depth = 5
        elif chess_num > 7:
            self.max_depth = 6
        elif chess_num > 5:
            self.max_depth = 7
        elif chess_num > 3:
            self.max_depth = 8
        else:
            self.max_depth = 9
        # print(f"deep{self.max_depth} and {chess_num}")
        score, move = self.alpha_beta(1, -9999999, 9999999, chessboard)  # 获取最优选择
        return move[0][0], move[0][1], move[1][0], move[1][1]  # 返回要移动的内容
        # raise NotImplementedError("Cannot determin next step!! Implement function ChessAI::get_next_step !!")

    @staticmethod
    def get_nxt_player(player):
        if player == 'r':
            return 'b'
        else:
            return 'r'

    @staticmethod
    def get_tmp_chessboard(chessboard, player_chess, new_row, new_col) -> ChessBoard:
        tmp_chessboard = copy.deepcopy(chessboard)
        tmp_chess = tmp_chessboard.chessboard_map[player_chess.row][player_chess.col]
        tmp_chess.row, tmp_chess.col = new_row, new_col
        tmp_chessboard.chessboard_map[new_row][new_col] = tmp_chess
        tmp_chessboard.chessboard_map[player_chess.row][player_chess.col] = None
        return tmp_chessboard

    def alpha_beta(self, depth, a, b, chessboard: ChessBoard):
        if depth == self.max_depth:  # 到达最大深度时返回估计值
            return self.evaluate_class.evaluate(chessboard), None
        if depth % 2 == 1:  # Max层
            chess_in_current_team = [chess for chess in chessboard.get_chess() if chess.team == "b"]  # 获取AI方所有的可用的棋子
            moves = {}
            for chess in chess_in_current_team:
                moves[chess] = list(chessboard.get_put_down_position(chess))  # 获取每个棋子可能的走步
            best_move = [(0, 0), (0, 0)]  # 初始化最优走步
            max_source = -9999999  # 初始化最优选择
            for chess, new_pos_list in moves.items():  # 遍历每一颗棋子
                for new_pos in new_pos_list:  # 遍历棋子的每一个走步
                    pos_chess_back = chessboard.chessboard_map[new_pos[0]][new_pos[1]]  # 记录即将被替换的位置的内容
                    old_pos = (chess.row, chess.col)  # 记录棋子的旧位置
                    # 更新棋盘走步
                    chessboard.chessboard_map[new_pos[0]][new_pos[1]] = chessboard.chessboard_map[old_pos[0]][old_pos[1]]  # 在棋盘新位置放下棋子
                    chessboard.chessboard_map[new_pos[0]][new_pos[1]].update_position(new_pos[0], new_pos[1])  # 更新棋子信息
                    chessboard.chessboard_map[old_pos[0]][old_pos[1]] = None  # 棋盘中棋子的旧位置为空（被移走）
                    score, _ = self.alpha_beta(depth+1, a, b, chessboard)  # 递归下一步
                    # 复原棋盘
                    chessboard.chessboard_map[old_pos[0]][old_pos[1]] = chessboard.chessboard_map[new_pos[0]][new_pos[1]]  # 在棋盘旧位置放回棋子
                    chessboard.chessboard_map[old_pos[0]][old_pos[1]].update_position(old_pos[0], old_pos[1])  # 更新棋子信息
                    chessboard.chessboard_map[new_pos[0]][new_pos[1]] = pos_chess_back  # 棋盘中新位置的内容复原
                    if score > max_source:  # 发现更优的选择
                        max_source = score  # 更新评价值
                        best_move[0] = (chess.row, chess.col)  # 更新最优走步（棋子的位置）
                        best_move[1] = new_pos  # 更新最优走步（棋子移动到哪）
                    a = max(max_source, a)  # 更新alpha值
                    if a >= b:  # alpha>=beta则剪枝
                        return a, best_move
            return a, best_move  # 遍历完所有情况，返回上一级
        else:  # Min层
            chess_in_current_team = [chess for chess in chessboard.get_chess() if chess.team == "r"]  # 获取对手方所有的可用的棋子
            moves = {}
            for chess in chess_in_current_team:
                moves[chess] = list(chessboard.get_put_down_position(chess))  # 获取每个棋子可能的走步
            min_source = 9999999  # 初始化最优选择
            for chess, new_pos_list in moves.items():  # 遍历每一颗棋子
                for new_pos in new_pos_list:  # 遍历棋子的每一个走步
                    pos_chess_back = chessboard.chessboard_map[new_pos[0]][new_pos[1]]   # 记录即将被替换的位置的内容
                    old_pos = (chess.row, chess.col)  # 记录棋子的旧位置
                    # 更新棋盘走步
                    chessboard.chessboard_map[new_pos[0]][new_pos[1]] = chessboard.chessboard_map[old_pos[0]][old_pos[1]]  # 在棋盘新位置放下棋子
                    chessboard.chessboard_map[new_pos[0]][new_pos[1]].update_position(new_pos[0], new_pos[1])  # 更新棋子信息
                    chessboard.chessboard_map[old_pos[0]][old_pos[1]] = None  # 棋盘中棋子的旧位置为空（被移走）
                    score, _ = self.alpha_beta(depth+1, a, b, chessboard)  # 递归下一步
                    # 复原棋盘
                    chessboard.chessboard_map[old_pos[0]][old_pos[1]] = chessboard.chessboard_map[new_pos[0]][new_pos[1]]  # 在棋盘旧位置放回棋子
                    chessboard.chessboard_map[old_pos[0]][old_pos[1]].update_position(old_pos[0], old_pos[1])  # 更新棋子信息
                    chessboard.chessboard_map[new_pos[0]][new_pos[1]] = pos_chess_back  # 棋盘中新位置的内容复原
                    if score < min_source:  # 发现更优的选择
                        min_source = score  # 更新评价值
                    b = min(min_source, score)  # 更新beta值
                    if a >= b:  # alpha>=beta则剪枝
                        return b, None
            return b, None   # 遍历完所有情况，返回上一级
        # raise NotImplementedError("Method not implemented!!!")
