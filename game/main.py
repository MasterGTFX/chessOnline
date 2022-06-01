import pygame, sys, os
from pygame.locals import *
from board import Board, black

pygame.init()

size = width, height = 600, 650
board_size = 600, 600
field_board_size = 5

screen = pygame.display.set_mode(size)

board = Board(screen, board_size, field_board_size)
screen.fill(black)
board.draw_board_background()
board.draw_pieces()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                board.handle_mouse_click(event.pos)

    pygame.display.flip()
