from agent1 import *
from dots_and_boxes import init_board
from itertools import combinations
import numpy as np
import json


WEIGHTS = np.array([2**i for i in xrange(2*BOARD_SIZE*(BOARD_SIZE-1))])
gamma = .9 # discount factor
RW = 10   # end score reward constant

def board2num(board):
    b = list(sum(board,[]))
    num = sum(WEIGHTS[i] for i in xrange(len(WEIGHTS))  if b[i])
    return num
    
def edge2num(edge):
    i,j = edge
    num = np.floor(i/2)*(2*BOARD_SIZE-1) + j
    if i % 2 == 1:
        num += BOARD_SIZE-1
    return(WEIGHTS[int(num)])
        
'''
def train_last_k(k):
    board = init_board()
    edges = []
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            board[i][j] = True
            edges.append((i,j))
   
    
    for m in xrange(k): 
    
        board_states = combinations(edges,m)        

        if m==0:    #end states
            board_num = str(board2num(board))
            max_score = (BOARD_SIZE-1)**2
            
            Qtable = [dict()]
            Q = [[ dict() for i in xrange(max_score+1)]]
            for score in xrange(max_score+1):
                Q[m][score][board_num] = RW*(score-(max_score/2))
                
        else:
            # initiate row in Q-value lookup table
            Q.append([ dict() for i in xrange(max_score - int(np.floor(m/4)))])
            Qtable.append(dict())
            for board_state in board_states:
                
                for edge in board_state:
                    i,j = edge
                    board[i][j] = False
                total_score = 0
                for i in xrange(BOARD_SIZE-1):
                    for j in xrange(BOARD_SIZE-1):
                        sq_edges = get_edges((i,j),board)
                        if sum(sq_edges) == 4:
                            total_score += 1
            
                feasible_moves = []
                
                for i, row in enumerate(board):
                    for j, val in enumerate(row):
                        if val == False:
                            gain = check_surrounding_squares(board,(i,j),3)
                            # move remembers edge inserted and score gain,  
                            feasible_moves.append(((i,j), gain))
                            
                # map feasible_moves on Q-values
                qmax = -np.inf
                board_num = board2num(board)
                for move in feasible_moves:
                    edge,gain = move
                    edge_num = edge2num(edge)
                    if gain:
                        qval = gamma*Q[m-1][total_score+gain][str(board_num + edge_num)]
                    else:
                        qval = -gamma*Q[m-1][0][str(board_num + edge_num)]
                    
                    if qmax < qval: 
                        qmax = qval
                        best_edge = edge
                
                # insert Q-values
                for score_state in xrange(total_score+1):
                    Q[m][score_state][str(board_num)] = qmax - RW*(total_score-score_state)
                # insert best move
                Qtable[m][str(board_num)] = best_edge
                    
                for edge in board_state:
                    i,j = edge
                    board[i][j] = True
                
    return(Q, Qtable)
'''
def agent2_load(k):
    
    f = open('Qedge_' + str(k)+ '_'+ str(BOARD_SIZE) + '.txt','r')
    Qtable = json.load(f)
    f.close()  
    
    return(Qtable)

def agent2_move(board,Qtable,k):
    # last k moves are best possible, the rest is played by behavior strategy

    m = 0
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == False: m += 1
    
    if m < k:
        board_num = board2num(board)
	Q_default = 0 
    	move = Qtable[m].get(str(board_num),Q_default)
        #move = Qtable[m][str(board_num)]
    else:
        move = behavior(board)
    
    return(move)
    
