import numpy as np #the structure used for storing the board is an np array
import board as b
import math
from random import shuffle
from anytree import Node
AI = 1
PLAYER = 0
counter=0
leafs = 0
count=0
def min_max_Function(board,depth,maximizingPlayer,root):

    global counter #counter to differentiate between nodes and each others
    global leafs
    global count
    #boolean variable byshouf el board etmalet wala lesa
    is_terminal = b.is_terminal_node(board)
    if depth == 0 or is_terminal: #if the depth is zero or we have reached a full board then we must return the score of the board
                                #this is a leaf node
        return (None, b.hurestic(board, b.AI_PIECE)-b.hurestic(board,b.PLAYER_PIECE))#calculate the score wrt the AI (maximizing player)
                                                                            #and player score (minimizing player)
    #btgib el list el fiha kol el columns el msh maliana w t3mlaha shuffle
    shuffled_neigboors = b.get_Children(board)
    shuffle(shuffled_neigboors)
    #el variable el fih el column el hayel3abo el AI fel next move
    column=shuffled_neigboors[0]
    #el AI howa el maxmizing ya3ny bydawar 3ala a3la rakam positive
    if maximizingPlayer == AI:
        #bn7ot variable el score =-infinity 3ashan initial value
        best=-math.inf
        #ba3mel check 3ala kol el available moves fel board
        for col in shuffled_neigboors:
            #kol column bashouf anhy awel row fady fih
            row=b.get_next_open_row(board,col)
            #bakhod copy men el board 3ashan agarab fiha mngher ma abawaz el main board
            board_copy=board.copy()
            #bagarab ahot el piece fel copy bta3et el board w ashouf anhy move hatb2a ahsan
            b.drop_piece(board_copy,row,col,b.AI_PIECE)
            #ba-save el node dy ka child lel root
            child = Node(board_copy, parent=root)

            new_score = min_max_Function(board_copy, depth - 1, PLAYER, child)[1]
            if depth == 1:#if it's a leaf node we print the board and it's score for tracing the minmax algorithm in the graph
                child.name=str(new_score) + "\n" + str(np.flip(board_copy, 0)) + "\n" + str(counter)
                leafs+=1
            else: #else it's a minimizing or a maximizing node then we should just add the score
                counter = counter + 1
                child.name =str(counter) + "\n" + str(new_score)

            #ba check el score da a3la men el best wala la( 3shan ana maximizing fa badwar 3ala a3la value)
            if new_score > best:
                best = new_score
                column = col

            count+=1
    else:
        best=math.inf
        for col in shuffled_neigboors:
            row=b.get_next_open_row(board,col)
            board_copy=board.copy()
            b.drop_piece(board_copy,row,col,b.PLAYER_PIECE)
            child = Node(board_copy, parent=root)
            new_score = min_max_Function(board_copy, depth - 1, AI, child)[1]
            if depth == 1:
                leafs += 1
                child.name=str(new_score) + "\n" + str(np.flip(board_copy, 0)) + "\n" + str(counter)
            else:
                counter = counter + 1
                child.name =str(counter) + "\n" + str(new_score)

            if new_score < best:
                best = new_score
                column = col
            count+=1

    return column,best