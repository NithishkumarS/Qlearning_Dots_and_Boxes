import numpy as np
from game import plotGrid, updateState, computeBoxCount, isOver
import random
import csv


class Qlearning:
    grid_size = 2
    state = np.zeros(grid_size*grid_size*4 - 4)
    observationSpace_size = np.power(2,12)
    actionSpace_size = 12
    Qtable = {}
    alpha = 0.5
    gamma  = 0.9
    reward = [0,1,5]
    epsilon = 1.0
    decay_rate = .01
    isOverFlag = False
    countA = 0
    countB = 0
    netA = 0
    netB = 0
    def __init__(self, q):
        self.decay_rate = .02
        self.Qtable = q
        self.grid_size = 2
    # ((2n +1 )(2n+1) - 1 )/2

    def valid_moves(self, currentState):
        return  list(np.where(np.array(currentState) == 0)[0])

    def best_future_actionReward(self,currentState, action):
        newState = updateState(currentState, action)
        max = np.argmax(self.Qtable[tuple(newState)])
        return max
    
    def boxDiff(self, action, currentState):
        no_of_boxes = computeBoxCount(currentState)
        newState = updateState(currentState, action)
        updatedBoxCount = computeBoxCount(newState)
        return updatedBoxCount - no_of_boxes
            
    def Qfunction(self, action, currentState):
        diff = self.boxDiff(action, currentState)
        self.countA += diff
        return self.Qtable[tuple(currentState)][action] + self.alpha*(self.computeReward(currentState,action,diff) + self.gamma*self.best_future_actionReward(currentState, action) - self.Qtable[tuple(currentState)][action]) 
    
    def computeReward(self, currentState, action,diff):
        reward = 0
#         print('current State:', currentState)
#         print('action:', action)
        if np.sum(currentState) == 11:# and currentState[action - 1 ] == 0:
            reward = 5
        else: 
            if diff >= 1:
                reward = diff
#         print('reward', reward)
        if reward == 5:
            self.isOverFlag = True
        return reward
    
    def decision(self):
        if self.countA > self.countB:
            self.netA += 1
            print('net a:', self.netA)
            print('A wins')
            self.countB = 0
            self.countA = 0
            
        else:
            self.netB += 1
            print('net b:', self.netB)
            print('B wins')
            self.countB = 0
            self.countA = 0
        
    def epsilonGreedy(self, currentState):
        
        action = 0
        esp = self.epsilon
        for batch in range(100):
            if .01 <= esp <= 1.0:
                esp = self.decay_rate*esp
        
            for i in range(100):
                print('i:',i)
               
                game = False
                while not game:        
                    feasbile_moves1 = self.valid_moves(currentState)
    #                 print('iter:', i)
                    if not tuple(currentState) in self.Qtable:
                        self.Qtable[tuple(currentState)] = np.zeros(12)
                    if np.random.uniform() < esp:
                        action = feasbile_moves1[random.sample(range(len(feasbile_moves1)),1)[0]]
                    else:
                        action = np.argmax(self.Qtable[tuple(currentState)])
    #                     print('current State:', currentState)
                    newState = updateState(currentState, action)
                    self.Qtable.setdefault(tuple(newState), np.zeros(12))
    #                 if not tuple(newState) in self.Qtable:
    #                     self.Qtable[tuple(newState)] = np.zeros(12)
                    self.Qtable[tuple(currentState)][action] = self.Qfunction(action, currentState)
                    currentState = newState
    #                 print('A:', currentState)
    #                 print('a count:',self.countA)
                    if isOver(currentState,self.grid_size):
                        currentState = np.zeros(12)
                        game = True
                        self.countA = 0
        print('Training Done')
        w = csv.writer(open("output.csv", "w"))
        for key, val in self.Qtable.items():
            w.writerow([key, val])            
                    
#     def epsilonDecay(self):

    def testPlay(self, currentState):
        print('Testing with random agent')
        for i in range(100):
            game = False
            next = random.sample(range(2),1)[0]
            while not game:        
                if next == 1:
                    next = 0
                    feasbile_moves2 = self.valid_moves(currentState)
                    action2= feasbile_moves2[random.sample(range(len(feasbile_moves2)),1)[0]]
                    self.countB += self.boxDiff(action2, currentState)
                    currentState = updateState(currentState, action2)
#                     print('b count:',self.countB)
#                     print('B:', currentState)
                
                feasbile_moves1 = self.valid_moves(currentState)
                actionSpace = self.Qtable.setdefault(tuple(currentState) , np.zeros(12)) 
                action1 = -1
                max = 0.0
                for i in feasbile_moves1:
                    if actionSpace[i] > max :
                        max = actionSpace[i]
                        action1 = i
                self.countA += self.boxDiff(action1, currentState)
                currentState = updateState(currentState, action1)
                
                if isOver(currentState, self.grid_size):
                    currentState = np.zeros(12)
                    game = True
                    self.decision()
                    break
                
                feasbile_moves2 = self.valid_moves(currentState)
                action2= feasbile_moves2[random.sample(range(len(feasbile_moves2)),1)[0]]
                self.countB += self.boxDiff(action2, currentState)
                currentState = updateState(currentState, action2)
#                 print('b count:',self.countB)
#                 print('B:', currentState)
                if isOver(currentState, self.grid_size):
                    currentState = np.zeros(12)
                    game = True
                    self.decision()
        w = csv.writer(open("output.csv", "w"))
        for key, val in self.Qtable.items():
            w.writerow([key, val])            
                            

if __name__ == "__main__":    
    obj = Qlearning({})
    currentState = np.zeros(12)
    obj.epsilonGreedy(currentState)
    obj.testPlay(currentState)
    print(obj.netA)
    print(obj.netB)
    