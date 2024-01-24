import numpy as np
import pygame
import board as b
import min_max as mi
import ctypes
import sys
import math
import time
from anytree import Node
deptho=2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
pygame.init()
screen1 = pygame.display.set_mode((600, 600))
screen2 = pygame.display.set_mode((850, 600))
turn = 0
def start():
    global turn
    board = b.create_board()
    b.print_board(board)
    game_over = False
    PLAYER = 0
    AI = 1
    screen = pygame.display.set_mode(b.size)
    b.draw_board(board)
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, b.width, b.SQUARESIZE))  # to clear circles
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(b.SQUARESIZE / 2)), b.RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, b.width, b.SQUARESIZE))
                # Ask for Player 1 Input
                if turn == PLAYER:

                    posx = event.pos[0]
                    col = int(math.floor(posx / b.SQUARESIZE))

                    if b.is_valid_location(board, col):
                        row = b.get_next_open_row(board, col)
                        b.drop_piece(board, row, col, b.PLAYER_PIECE)
                        turn += 1
                        turn = turn % 2

                    if b.win(board,b.PLAYER_PIECE):
                        print("you win")
                        game_over = True

                    if b.is_terminal_node(board):
                        print("draw")
                        game_over = True

                b.draw_board(board)

                if turn == AI and not game_over:
                    if b.is_terminal_node(board):
                        print("draw")
                        game_over = True

                    global deptho
                    root = Node(board)
                    start_time = time.time()
                    col, minimax_scorecore = mi.min_max_Function(board, deptho, AI, root)
                    end_time = time.time()
                    print(
                        "time taken = " + str(end_time - start_time))  # calculate time taked and display it in console

                    if b.is_valid_location(board, col):
                        # pygame.time.wait(500)
                        row = b.get_next_open_row(board, col)
                        b.drop_piece(board, row, col, b.AI_PIECE)
                        b.draw_board(board)
                        root.name = str(minimax_scorecore) + "\n" + str(np.flip(board, 0))
                        print("Nodes explored " + str(mi.count))
                        mi.count=0
                        mi.counter=0
                        mi.leafs=0
                        turn += 1
                        turn = turn % 2
                    if b.win(board,b.AI_PIECE):
                        print("AI win")
                        game_over = True

    time.sleep(5)
    exit()

def button(screen, position, text, color=(100, 100, 100)):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, color, (x, y, w, h))
    return screen.blit(text_render, (x, y))




def menu():
    """ This is the menu that waits you to click the s key to start """
    global turn
    global deptho
    colorAI = (200, 100, 100)
    colorPlayer = (100, 100, 200)
    b1 = button(screen1, (350, 500), "  Quit  ")
    b2 = button(screen1, (345, 400), "  Start  ")
    b3 = button(screen1, (500, 280), "    AI    ", colorAI)
    b4 = button(screen1, (200, 280), " Player ", colorPlayer)
    font = pygame.font.SysFont("Arial", 35)
    font1 = pygame.font.SysFont("Arial", 40)
    text = font1.render('       WELCOME TO OUR CONNECT 4 GAME', True, (255, 255, 255))
    text1 = font.render('       Please select the first player :', True, (255, 255, 255))

    textRect1 = text1.get_rect()
    textRect = text.get_rect()
    textRect1.center = (170, 200)
    textRect.center = (400, 50)
    turnCheck = 0
    algoCheck = 0
    depthCheck = 0
    clock = pygame.time.Clock()
    # it will display on screen
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    while True:
        screen1.blit(text, textRect)
        screen1.blit(text1, textRect1)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP

            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    exit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    if turnCheck == 0 and algoCheck == 0 and depthCheck == 0:
                        ctypes.windll.user32.MessageBoxW(0, "Please select who will play first", "ERROR!", 1)
                    else:
                        pygame.display.flip()
                        start()
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    turn = 1
                    turnCheck = 1
                    colorAI = (200, 00, 00)
                    colorPlayer = (100, 100, 200)
                    b3 = button(screen1, (500, 280), "    AI    ", colorAI)
                    b4 = button(screen1, (200, 280), " Player ", colorPlayer)
                elif b4.collidepoint(pygame.mouse.get_pos()):
                    turn = 0
                    turnCheck = 1
                    colorAI = (200, 100, 100)
                    colorPlayer = (00, 00, 200)
                    b3 = button(screen1, (500, 280), "    AI    ", colorAI)
                    b4 = button(screen1, (200, 280), " Player ", colorPlayer)


        clock.tick(60)
        pygame.display.update()
    pygame.quit()
menu()