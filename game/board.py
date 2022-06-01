import pygame, os
from .chess_logic import check_possible_moves, is_checkmate

black = 0, 0, 0
white = 255, 255, 255
floralwhite = 255, 250, 240
grey = 192, 192, 192
ivory = 255, 255, 15
limegreen = 50, 205, 50


class Board:
    is_field_selected = False
    is_started = False
    field_selected = 0, 0
    possible_moves = []
    checkmate = False

    def __init__(self, screen, board_size, field_board_size):
        self.screen = screen
        self.board_size = board_size
        self.field_board_size = field_board_size
        self.board_width = board_size[0]
        self.board_height = board_size[1]
        self.field_size = self.board_width / 8, self.board_height / 8
        self.field_without_board_size = [(self.board_width - field_board_size * 8) / 8,
                                         (self.board_height - field_board_size * 8) / 8]
        self.black_queen = pygame.image.load(os.path.join("game", "resources", "black_queen.png"))
        self.white_queen = pygame.image.load(os.path.join("game", "resources", "white_queen.png"))
        self.black_pawn = pygame.image.load(os.path.join("game", "resources", "black_pawn.png"))
        self.white_pawn = pygame.image.load(os.path.join("game", "resources", "white_pawn.png"))
        self.white_king = pygame.image.load(os.path.join("game", "resources", "white_king.png"))
        self.black_king = pygame.image.load(os.path.join("game", "resources", "black_king.png"))
        self.white_rook = pygame.image.load(os.path.join("game", "resources", "white_rook.png"))
        self.black_rook = pygame.image.load(os.path.join("game", "resources", "black_rook.png"))
        self.white_bishop = pygame.image.load(os.path.join("game", "resources", "white_bishop.png"))
        self.black_bishop = pygame.image.load(os.path.join("game", "resources", "black_bishop.png"))
        self.white_knight = pygame.image.load(os.path.join("game", "resources", "white_knight.png"))
        self.black_knight = pygame.image.load(os.path.join("game", "resources", "black_knight.png"))

        self.board = self.default_board()

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

    def draw_field(self, pos, color):
        pygame.draw.rect(self.screen, color,
                         pygame.Rect((self.field_board_size * pos[0]) + (pos[0] * self.field_without_board_size[0]),
                                     (self.field_board_size * pos[1]) + (pos[1] * self.field_without_board_size[1]),
                                     self.field_without_board_size[0], self.field_without_board_size[1]))

    def draw_pieces(self):
        """
        Empty -> 0

        Black Pawn -> 1
        Black Bishop -> 2
        Black Knight -> 3
        Black Rook -> 4
        Black Queen -> 5
        Black King -> 6

        White Pawn -> 7
        White Bishop -> 8
        White Knight -> 9
        White Rook -> 10
        White Queen -> 11
        White King -> 12
        """
        for i in range(8):
            for j in range(8):
                piece_pos = ((self.field_board_size * i) + (i * self.field_without_board_size[0])
                             + self.field_without_board_size[0] / 2 - 30,
                             (self.field_board_size * j) + (j * self.field_without_board_size[1])
                             + self.field_without_board_size[1] / 2 - 30)
                if self.board[i][j] == 0:
                    continue
                elif self.board[i][j] == 1:
                    self.screen.blit(self.black_pawn, piece_pos)
                elif self.board[i][j] == 2:
                    self.screen.blit(self.black_bishop, piece_pos)
                elif self.board[i][j] == 3:
                    self.screen.blit(self.black_knight, piece_pos)
                elif self.board[i][j] == 4:
                    self.screen.blit(self.black_rook, piece_pos)
                elif self.board[i][j] == 5:
                    self.screen.blit(self.black_queen, piece_pos)
                elif self.board[i][j] == 6:
                    self.screen.blit(self.black_king, piece_pos)
                elif self.board[i][j] == 7:
                    self.screen.blit(self.white_pawn, piece_pos)
                elif self.board[i][j] == 8:
                    self.screen.blit(self.white_bishop, piece_pos)
                elif self.board[i][j] == 9:
                    self.screen.blit(self.white_knight, piece_pos)
                elif self.board[i][j] == 10:
                    self.screen.blit(self.white_rook, piece_pos)
                elif self.board[i][j] == 11:
                    self.screen.blit(self.white_queen, piece_pos)
                elif self.board[i][j] == 12:
                    self.screen.blit(self.white_king, piece_pos)

    def draw_board_background(self):
        self.screen.fill(black)
        for i in range(8):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    field_color = floralwhite
                else:
                    field_color = grey
                self.draw_field((i, j), field_color)

    def handle_mouse_click(self, pos):
        field = int(pos[0] / self.field_size[0]), int(pos[1] / self.field_size[1])
        if not self.is_field_selected:
            self.field_selected = field
            self.draw_board_background()
            self.draw_field(self.field_selected, ivory)
            for field in check_possible_moves(self.board, self.field_selected):
                self.possible_moves.append(field)
                self.draw_field(field, limegreen)
            self.draw_pieces()
        else:
            if field in self.possible_moves:
                checkmate = is_checkmate(self.board, self.board[field[0]][field[1]] > 6)
                if checkmate:
                    print("CHECKMATE!")
            self.draw_board_background()
            self.draw_pieces()
            self.possible_moves = []
        self.is_field_selected = not self.is_field_selected
        if not self.is_field_selected:
            return self.field_selected, field
        return False

    def set_board(self, board):
        self.board = board
