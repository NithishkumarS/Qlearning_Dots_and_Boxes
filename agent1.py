from dots_and_boxes import *
from random import randint

            

def get_first_completing_move(board):
    # returns completing move, if exists
    # otherwise returns False 
    for i in xrange(BOARD_SIZE-1):
        for j in xrange(BOARD_SIZE-1):
            sq_edges = get_edges((i,j),board)
            if sum(sq_edges) == 3: 
                ind = sq_edges.index(0)
                xc = [i*2,i*2+1,i*2+1,i*2+2]
                yc = [j,j,j+1,j]
                return (xc[ind],yc[ind])
    return(False)                
                

def get_random_move(board):
    
    feasible_moves = get_feasible_moves(board)
    ind = randint(0,len(feasible_moves)-1)
    return(feasible_moves[ind])
   


def behavior(board):
    move = get_first_completing_move(board)
    if move:
        return(move)
        
    feasible_moves = []
    feasible_moves_not3 = []
    
    
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == False:
                feasible_moves.append((i,j))
                # check for 2 edged  surroundung squares
                tmp = check_surrounding_squares(board,(i,j),2)
                if not tmp: feasible_moves_not3.append((i,j))
    
    if not feasible_moves:
        return(False)
    else:
        if feasible_moves_not3:
            return(feasible_moves_not3[randint(0,len(feasible_moves_not3)-1)])        
        else:
            return(feasible_moves[randint(0,len(feasible_moves)-1)])
