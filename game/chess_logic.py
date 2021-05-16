import logging, os

if not os.path.exists("./logs/"):
    os.makedirs("./logs/")

logging.basicConfig(level=logging.DEBUG, filename='./logs/chess_logic.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(asctime)s %(message)s')
logger = logging.getLogger(__name__)


def get_all_moves(board, piece_pos):
    piece = board[piece_pos[0]][piece_pos[1]]
    all_moves = []
    if piece in [1, 7]:
        # pawn
        if piece == 1:
            move = piece_pos[0], piece_pos[1] + 1
        else:
            move = piece_pos[0], piece_pos[1] - 1
        all_moves.append(move)

    elif piece in [2, 8]:
        # bishop
        for i in [1, -1]:
            for j in [1, -1]:
                move = piece_pos[0] + i, piece_pos[1] + j
                if not (is_within_board(move) and is_not_self_piece(board, piece, move)):
                    continue
                for k in range(1, 8):
                    move = piece_pos[0] + i * k, piece_pos[1] + j * k
                    all_moves.append(move)

    elif piece in [3, 9]:
        # knight
        for i in [1, 2, -1, -2]:
            for j in [1, 2, -1, -2]:
                if abs(i) != abs(j):
                    move = piece_pos[0] + i, piece_pos[1] + j
                    all_moves.append(move)

    elif piece in [4, 10]:
        # rook
        for i in [1, -1]:
            for k in range(1, 8):
                move = piece_pos[0] + i * k, piece_pos[1]
                move2 = piece_pos[0], piece_pos[1] - i * k
                all_moves.append(move)
                all_moves.append(move2)

    elif piece in [5, 11]:
        # Queen
        for i in [1, -1]:
            for j in [1, -1]:
                move = piece_pos[0] + i, piece_pos[1] + j
                if not (is_within_board(move) and is_not_self_piece(board, piece, move)):
                    continue
                for k in range(1, 8):
                    move = piece_pos[0] + i * k, piece_pos[1] + j * k
                    all_moves.append(move)
        for i in [1, -1]:
            for k in range(1, 8):
                move = piece_pos[0] + i * k, piece_pos[1]
                move2 = piece_pos[0], piece_pos[1] - i * k
                all_moves.append(move)
                all_moves.append(move2)
    elif piece in [6, 12]:
        # King
        for i in [1, 0, -1]:
            for j in [1, 0, -1]:
                all_moves.append((piece_pos[0] + i, piece_pos[1] + j))

    return all_moves


def get_possible_moves(board, all_moves, piece_pos, piece):
    possible_moves = []
    if piece in [1, 7, 3, 9, 6, 12]:
        for move in all_moves:
            logging.debug("[Debug] Check for " + str(piece_pos) + "->" + str(move))
            if is_within_board(move) \
                    and is_not_self_piece(board, piece, move):
                possible_moves.append(move)
    else:
        for move in all_moves:
            logging.debug("[Debug] Check for " + str(piece_pos) + "->" + str(move))
            if is_within_board(move) \
                    and is_not_self_piece(board, piece, move) \
                    and is_not_behind_another_piece(board, piece_pos, move):
                possible_moves.append(move)
    return possible_moves


def check_possible_moves(board, piece_pos):
    not_checkmate_moves = []
    piece = board[piece_pos[0]][piece_pos[1]]
    all_moves = get_all_moves(board, piece_pos)
    possible_moves = get_possible_moves(board, all_moves, piece_pos, piece)

    for move in possible_moves:
        if is_not_giving_checkmate(board, piece_pos, piece, move):
            not_checkmate_moves.append(move)
    return not_checkmate_moves


def is_within_board(move):
    is_within = not (move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7)  # debug
    logging.debug(str(move[0]) + "," + str(move[1]) + " is within board: " + str(is_within))

    return not (move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7)


def is_not_self_piece(board, piece, move):
    is_not_self = True  # debug
    if board[move[0]][move[1]] == 0:
        logging.debug(str(move[0]) + "," + str(move[1]) + " is not self: " + str(is_not_self))
        return is_not_self
    elif piece < 7:
        is_not_self = board[move[0]][move[1]] >= 7
    else:
        is_not_self = board[move[0]][move[1]] <= 6

    logging.debug(str(move[0]) + "," + str(move[1]) + " is not self: " + str(is_not_self))
    return is_not_self


def is_not_behind_another_piece(board, piece_pos, move):
    diff_x = piece_pos[0] - move[0]
    diff_y = piece_pos[1] - move[1]
    temp_x = piece_pos[0]
    temp_y = piece_pos[1]
    is_behind = True
    # debug
    while diff_x != 0 or diff_y != 0:

        if diff_x > 0:
            diff_x -= 1
            temp_x -= 1
        elif diff_x < 0:
            diff_x += 1
            temp_x += 1

        if diff_y > 0:
            diff_y -= 1
            temp_y -= 1
        elif diff_y < 0:
            diff_y += 1
            temp_y += 1

        if board[temp_x][temp_y] != 0 and move != (temp_x, temp_y):
            is_behind = False
            logging.debug(str(move[0]) + "," + str(move[1]) + " is not behihd another: " + str(is_behind))  # debug
            break
    logging.debug(str(move[0]) + "," + str(move[1]) + " is not behihd another: " + str(is_behind))  # debug
    return is_behind


def is_not_giving_checkmate(board, piece_pos, piece, move):
    pieces_to_check = []
    king_pos = []
    for x_index in range(0, 8):
        for y_index in range(0, 8):
            if piece < 7:
                if board[x_index][y_index] < 7:
                    if board[x_index][y_index] == 6:
                        king_pos = [x_index, y_index]
                    continue
            else:
                if board[x_index][y_index] > 6 or board[x_index][y_index] == 0:
                    if board[x_index][y_index] == 12:
                        king_pos = [x_index, y_index]
                    continue
            pieces_to_check.append([x_index, y_index])
    if piece in [6, 12]:
        king_pos = [move[0], move[1]]
    # simulate move
    temp_board = [row[:] for row in board]
    temp_board[piece_pos[0]][piece_pos[1]] = 0
    temp_board[move[0]][move[1]] = piece

    for enemy_piece_pos in pieces_to_check:
        enemy_piece = temp_board[enemy_piece_pos[0]][enemy_piece_pos[1]]
        enemy_moves = get_all_moves(temp_board, enemy_piece_pos)
        enemy_possible_moves = get_possible_moves(temp_board, enemy_moves, enemy_piece_pos, enemy_piece)
        if (king_pos[0], king_pos[1]) in enemy_possible_moves:
            logging.debug(str(move[0]) + "," + str(move[1]) + " is giving enemy checkmate")
            return False
    logging.debug(str(move[0]) + "," + str(move[1]) + " is not giving enemy checkmate")  # debug
    return True


def is_checkmate(board, is_white):
    ally_pieces = []
    for x_index in range(0, 8):
        for y_index in range(0, 8):
            if is_white:
                if 7 > board[x_index][y_index] > 0:
                    ally_pieces.append([x_index, y_index])
                else:
                    continue
            else:
                if board[x_index][y_index] > 6:
                    ally_pieces.append([x_index, y_index])

    for ally_piece_pos in ally_pieces:
        ally_possible_moves = check_possible_moves(board, ally_piece_pos)
        if ally_possible_moves:
            return False
    return True
