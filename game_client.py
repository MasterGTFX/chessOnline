import pygame, pygame_menu, threading
from game.board import black
from network_client import Client

pygame.init()

size = width, height = 600, 800
board_size = 600, 600
field_board_size = 5
start_game = False

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess Client')
screen.fill(black)


def start_game(name, server_ip, server_port):
    game_client = Client(name, server_ip, int(server_port))
    menu.get_widget("is_connecting").set_title("Connecting...")
    menu.close()
    if game_client.connected:
        menu.get_widget("is_connecting").set_title("Connected")
        menu.close()
    else:
        menu.get_widget("is_connecting").set_title("Coudn't connect to a game server..")


def join_the_game():
    name = menu.get_widget('name').get_value()
    server_ip = menu.get_widget('server_ip').get_value()
    server_port = menu.get_widget('server_port').get_value()
    menu.get_widget("is_connecting").set_title("Connecting...")
    start_game(name, server_ip, server_port)


# menu
menu = pygame_menu.Menu('Chess Game', 600, 800,
                        theme=pygame_menu.themes.THEME_DARK)
# menu.set_onclose(game_loop)
menu.add.text_input('Name: ', default='John Doe', textinput_id="name")
menu.add.text_input('Server IP: ', default='192.168.243.100', textinput_id="server_ip")
menu.add.text_input('Port: ', default='65432', textinput_id="server_port")
menu.add.button('Join', join_the_game)
menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT)
menu.add.label("", label_id="is_connecting")
menu.mainloop(screen)
