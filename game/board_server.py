import pygame, os
from .chess_logic import check_possible_moves, is_checkmate

black = 0, 0, 0
white = 255, 255, 255
floralwhite = 255, 250, 240
grey = 192, 192, 192
ivory = 255, 255, 15
limegreen = 50, 205, 50


class Board:
    def __init__(self):
        self.board = self.default_board()
        self.possible_moves = []
        self.field_selected = 0, 0

    def default_board(self):
        """
        10 9 8 11 12 8 9 10
        7 7 7 7 7 7 7 7
        ..
        1 1 1 1 1 1 1 1
        4 3 2 5 6 2 3 4
        """
        board = [[0 for i in range(8)] for i in range(8)]
        for a in range(8):
            board[a][1] = 1
            board[a][6] = 7

        board[0][0] = 4
        board[7][0] = 4
        board[1][0] = 3
        board[6][0] = 3
        board[2][0] = 2
        board[5][0] = 2
        board[3][0] = 5
        board[4][0] = 6

        board[0][7] = 10
        board[7][7] = 10
        board[1][7] = 9
        board[6][7] = 9
        board[2][7] = 8
        board[5][7] = 8
        board[3][7] = 11
        board[4][7] = 12

        return board

    def move_piece(self, previous_field, field, is_white):
        self.field_selected = previous_field

        # check if own piece
        if is_white and self.board[previous_field[0]][previous_field[1]] < 7:
            return False
        if not is_white and self.board[previous_field[0]][previous_field[1]] >= 7:
            return False

        # check if move possible
        possible_moves = []
        for possible_field in check_possible_moves(self.board, self.field_selected):
            possible_moves.append(possible_field)
        if field == self.field_selected or field not in possible_moves:
            return False
        # all correct -> make move
        else:
            past_piece = self.board[self.field_selected[0]][self.field_selected[1]]
            self.board[field[0]][field[1]] = past_piece
            self.board[self.field_selected[0]][self.field_selected[1]] = 0
            return True

    def check_checkmate(self, is_white):
        return is_checkmate(self.board, is_white)
