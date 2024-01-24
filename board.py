import numpy as np #the structure used for storing the board is an np array
import pygame
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_PIECE=1
AI_PIECE=2
#creates an empty array of zeros with the height= no of rows and width=no of columns
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT)) #initializaing an empty array
    return board

#el function el bt2ol lel pc ynazel el coin f anhy row
def drop_piece(board, row, col, piece):
    board[row][col] = piece

#function btt2aked en el column el ehna ekhtarnah da msh malian
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

#function btshouf anhy awel row fady fel column el ekhtarnah
def get_next_open_row(board, col):
    for r in range(ROW_COUNT): #starting from 0 to the row count we check for an empty row of the chosen column
        if board[r][col] == 0:
            return r
#function bt3ml print lel board bta3etna ma2louba 3shan el coins teb2a bttgama3 men taht l fo2 msh men fo2 l taht
def print_board(board):
    print(np.flip(board, 0))
#function bt-check ehna gam3na 4 coins wala lesa w law gama3na 4 bt-return True l function fel main
def win(board, piece):
    #ba-check el horizontal line win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] ==piece and board[r][c+3] == piece:
                return True
    # ba-check el vertical line win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] ==piece and board[r+3][c] == piece:
                return True
    # ba-check el right diagonal line win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if     board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] ==piece and board[r+3][c+3] == piece:
                return True;
    # ba-check el left diagonal line win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                 c + 3] == piece:
                return True;
    return False;
#RED is 1
#yellow is 2

#bt3ml list fiha el columns el available w msh maliana
def get_Children(board): #get the children of the current board (vary from 0 to 7 ) and check if the child is valid
    children=[]
    for col in range(COLUMN_COUNT):
        if(is_valid_location(board,col)):
            children.append(col)

    return children
#btshouf dy el board kolaha et2afalet wala lesa (6rows x 7columns =42 slots)
def is_terminal_node(board):
    return np.count_nonzero(board) == 42 #if the board has no empty places then the game is over (terminal node)

def scores(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 110 #win
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 60 #empty place and 3 in a row
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 10 #2 in a row and 2 empty places

    if window.count(opp_piece) == 4:
        score -= 100 # opponent win
    elif window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 50  # opponent connect 3
    elif window.count(opp_piece) == 2 and window.count(0) == 2:
        score -= 5   # opponent connect 2

    return score

def hurestic(board,piece):
    hueristic_array = np.array(
        [[0.25, 0.5, 1, 2, 1, 0.5, 0.25],
         [0.5, 1, 2, 3, 2, 1, 0.5],
         [1, 1.5, 2.5, 4, 2.5, 1.5, 1],
         [1, 1.5, 2.5, 4, 2.5, 1.5, 1],
         [0.5, 1, 2, 3, 2, 1, 0.5],
         [0.25, 0.5, 1, 2, 1, 0.5, 0.25]])

    copy_board = board.copy()

    score=0
    # To favor playing the middle places we multiply the current board with the heuristic array to get a score
    #note that playing in the middle should be favored because it provides more opportunity for a win
    if piece == AI_PIECE :
         copy_board[copy_board == PLAYER_PIECE] = 0
         copy_board[copy_board == AI_PIECE]=1
         score+=np.sum(np.multiply(copy_board,hueristic_array))
    else:
         copy_board[copy_board == AI_PIECE] = 0
         score+=np.sum(np.multiply(copy_board,hueristic_array))

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]   #assign the row to a window for score calculation later
            score += scores(window, piece)#send the list (window) for score evaluation

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += scores(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += scores(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += scores(window, piece)



    return score

#board GUI part
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#size kol khana menhom
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)
#radius el dayra el soda f kol khana (el -5 3shan yeb2a fy radius azra2 hawalen el daira el soda)
RADIUS = int(SQUARESIZE / 2 - 5 )
#bt create el window el bttla3lena fiha el le3ba
screen = pygame.display.set_mode(size)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            #btersem el squares el bn7ot fiha el coins
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE , r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            #btkhaly el square gowah el circle el soda el bidkhol fiha el coin
            pygame.draw.circle(screen, (0, 0, 0), (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
#hena bylawen kol circle 3ala hasab heya yellow wala red
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()