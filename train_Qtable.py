from agent1 import *
from agent2 import *
from dots_and_boxes import *
import matplotlib.pyplot as plt
def traverse_updateQ(Q,board,l_rate=1,gamma = .9,random_move_prob=1):

    board_num = board2num(board)    
    feasible_moves = get_feasible_moves(board)
    m = len(feasible_moves)
    total_score = get_total_score(board)
    max_score = (BOARD_SIZE-1)**2
    
    s = 0
    p = 0
    for move in feasible_moves:
        edge_num = edge2num(move)
        q_tmp = Q[m-1].get(str(board_num+edge_num),0)
        s +=  q_tmp
        p += 1 if q_tmp else 0 
    Q_default = (max_score-total_score)/2 if p<2 else s/p 
    q_old = Q[m].get(str(board_num),Q_default)
    
    q_max = -np.inf
    for move in feasible_moves:
        edge_num = edge2num(move)
        q_tmp = Q[m-1].get(str(board_num+edge_num),Q_default) # gamma=1
        reward = check_surrounding_squares(board,move,3)
        if reward: 
            # it is our move again and we can get at least Q-value of score
            q_tmp += reward   # we add reward  
        else: 
            # it is the opponents move, so Qvalue is the score he can get
            q_tmp = (max_score - total_score - q_tmp)
        
        if q_tmp > q_max: 
            q_max = q_tmp
            best_move = move
            
    q_new = q_old + l_rate*(gamma*q_max - q_old) # q_max is the max_a{reward_a + q_next_state_a}   
    
    if random.randrange(int(random_move_prob)): 
        best_move = random.choice(feasible_moves)
	
    
    return(best_move,q_new)
    
    
def init_Q2():
    board = init_board()
    Q = [dict() for i in xrange(len(sum(board,[]))+1)]
    for i,row in enumerate(board):
        for j,val in enumerate(row):
            board[i][j] = True
    Q[0][str(board2num(board))] = 0
    return(Q)
    
    
def player_move(board,Qtable,k,agent):
    
    if agent == 0: 
        move = get_random_move(board)
    elif agent == 1:
        move = first_available_move(board)   
    elif agent == 2:
        move = behavior(board)
    elif agent == 3:
        move = agent2_move(board,Qtable,k)
    else:
        if random.randrange(3):
            move = agent2_move(board,Qtable,k)
        else: 
            move = get_random_move(board)
    return(move)
def train_Qlearning(num_games,Q = None,l_rate=1,gamma = .9,random_move_prob=2, print_score=False, agent=0):
    res= []
    if Q == None:
        # initialize Q
        Q = init_Q2()
    
    board = init_board()
    M = len(sum(board,[]))
    k = 10
    start_player = 1
    wins = [0,0]
    
    for game_num in range(num_games):
        board = init_board()
        current_player = start_player
        m = M
        score = [0,0]
        game_moves = []
        q_updates = []
        while m>0:
            
            board_num = board2num(board)
            if current_player == 1:
                move = player_move(board,Qtable,k,agent)
                tmp,update = traverse_updateQ(Q,board,l_rate,gamma,random_move_prob)
            else:
                move,update = traverse_updateQ(Q,board,l_rate,gamma,random_move_prob)
            
            Q[m][str(board_num)] = update
            
            game_moves.append(move)
            i,j = move
            
            if board[i][j] == True: 
                return(Q)
                
            gain = check_surrounding_squares(board,move,3)
            
            if (gain > 0):
                score[current_player] += gain   # update score
            else: 
                current_player = (1 + current_player)%2 # update current_player
            
            board[i][j] = True      # update board
            m -= 1
            

        if print_score: print(score)
        winner = score.index(max(score))
        if not score[0] == score[1]: wins[winner] += 1  
         
        start_player = (1 + start_player) % 2 
        res.append(score)
    print('wins', wins)
    return(Q,res)
        
    

    
Qtable = agent2_load(10) 
gamma = 0.9
#generarting intial q table
Q,wins = Q,wins = train_Qlearning(1,l_rate = 1,gamma = .9,random_move_prob = 3, agent = 1) 

#training the data
Q,wins = train_Qlearning(10000,Q, l_rate = 0.5,gamma = .82, random_move_prob = 2, agent = 2)
print('ff')

#testing the code, note learning rate set as zero 
# gamma doesnt have an ipact since learning rate is zero

Q1,wins = train_Qlearning(100,Q, l_rate = 0,gamma = .9, random_move_prob = 1, print_score = True, agent =1)
print('Wins, Loses '+  ': ' + str(wins))

a = [i[0] for i in wins]
b = [i[1] for i in wins]
n = range(100)
fig = plt.figure()
plt.plot(n,a,label = 'Q_agent')
plt.plot(n,b,label = 'Random player')
plt.legend()
plt.show()
