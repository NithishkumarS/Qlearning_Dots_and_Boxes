import numpy as np
import sys

# This try-catch is a workaround for Python3 when used with ROS; it is not needed for most platforms
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass
import cv2

def play_2x2_Grid():
    game = False
    result = 2 
    state = np.zeros(12)
    Box1 = 0
    Box2 = 0
    while not game:
        player1_move = int(input("Enter the position of the line player1: "))
        state = updateState(state, player1_move)
        plotGrid(state)
        game = isOver(state)
        if game:
            result = 1
            break
        if checkBox(state, player1_move):
            continue
        player2_move = int(input("Enter the position of the line player2: "))
        state = updateState(state, player2_move)
        plotGrid(state)
        game = isOver(state)
        while checkBox(state , player2_move):
            player2_move = int(input("Enter the position of the line player2: "))
            state = updateState(state, player2_move)
            plotGrid(state)
            game = isOver(state)
            
    if result == 1:
        print('Player 1 has won the game')
    elif result ==2 :
        print('Player 2 has won the game')
    
def checkBox(state, action):
    
    no_of_boxes = computeBoxCount(state)
    newState = updateState(state, action)
    no_of_boxes2 = computeBoxCount(newState)
    if no_of_boxes2 - no_of_boxes ==1:
        return True
    else:
        return False
    
def updateState(currentState, line_number):
    newState = np.copy(currentState)
    newState[int(line_number)] = 1
    print('Added an edge at ',line_number+1)
    return newState

def computeBoxCount(currentState):
    count = 0
    k = 0
    for i in range(4):
#         print('i:',i)
        if i != 0 and (i%2) == 0:
            k += 1
#             print('k:',k)
        if currentState[i] == 1 and currentState[(i+2)] == 1 and currentState[(i+5+k)] == 1 and currentState[(i+7+k)] == 1:
            count = count +1
#             print('count:', count)
    print('count',count)
    return count

def isOver(state):
    sum = np.sum(state)
    if sum == 12:
        return True
    else:
        return False
    
def plotGrid(state):
    img = np.zeros((200,200,3), np.uint8)
    points = np.array([[50,50],[100,50],[150,50],[50,100],[100,100],[150,100],[50,150],[100,150],[150,150]])
    for i in points:
        cv2.circle(img,(i[0],i[1]), 5, (0,0,255), -1)
    lines = {1:[[50,50],[100,50]], 2:[[100,50],[150,50]], 3:[[50,100],[100,100]], 4:[[100,100],[150,100]], 5:[[50,150],[100,150]], 6: [[100,150],[150,150]], 
             7:[[50,50],[50,100]], 8: [[50,100],[50,150]], 9: [[100,50],[100,100]], 10:[[100,100],[100,150]], 11:[[150,50],[150,100]], 12:[[150,100],[150,150]] }
    for i in range(len(state)):
        if (state[i]==1):
            pt1 = tuple(lines[i+1][0])
            pt2 = tuple(lines[i+1][1])
            cv2.line(img,pt1,pt2,(255,255,255))
        
    cv2.imshow('Board', img)
    cv2.waitKey(0)


if __name__ == "__main__":
    '''
    play_2x2_Grid()
    
    '''
#     img = np.zeros((200,200,3), np.uint8)
    state = np.ones(12)
    plotGrid(state)
#     cv2.waitKey(0)
    