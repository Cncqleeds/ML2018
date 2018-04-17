# -*- coding: utf-8 -*-

import numpy as np
import copy
import sys

class State:
    def __init__(self,size=19, history=8,cur_player=1,dtype=np.int8):
        self.size = size
        self.history = history # 本方最近history步内的棋面和对方最近history步内的棋面,即history个回合
        self.cur_player = cur_player  # 当前棋手，0为执黑棋手，1 为执白棋手
        self.dtype = dtype
        # 其他状态的原始表示方法。-1表示黑子,0表示没子，1表示白子。
        self.raw_board = np.zeros((size,size),dtype)
        # 0 -- history*2+2 个channal。第history*2个channal表示执黑行棋，第history*2+1个channal表示执白行棋
        self.state = np.zeros((size,size,history*2+2),dtype)
        # 0 -- 2*history 个原始状态
        self.history_board = np.zeros((2*history,size,size),dtype)
        
    
    def move(self,action):
        """
        在raw_borad下，计算cur_player 执行action后的新状态next_raw_board
        事实上，这步比较核心，效率是很关键
        """
        next_raw_board = self.raw_board.copy() # 由于参数是引用，所以需要拷贝一份
        next_raw_board[action] = 1 if self.cur_player == 1 else -1
        return next_raw_board
    
    def next_player(self):
        """
        切换棋手
        """
        return 0 if self.cur_player == 1 else 1
    
    def gen_2d_state(self,raw_board):
        """
        """
        state_2d = np.zeros((self.size,self.size,2),self.dtype)
        black_state = np.zeros((self.size,self.size),self.dtype)
        white_state = np.zeros((self.size,self.size),self.dtype)
        black_state[raw_board == -1] = 1
        white_state[raw_board == 1] = 1

        state_2d[:,:,0] = black_state
        state_2d[:,:,1] = white_state

        return state_2d
    
#     def gen_state_from_history(self):
#         state = np.zeros((self.size,self.size,self.history*2+2),self.dtype)
#         state[:,:,self.history*2 + self.cur_player] = 1

#         for i in range(self.history):
#             state_2d = self.gen_2d_state(self.history_board[i,:,:])
#             state[:,:,i*2:i*2+2] = state_2d

#         return state  
    
    def update_history_board(self):
        self.history_board = np.roll(self.history_board,shift=1,axis=0)
        self.history_board[0,:,:] = self.raw_board
        
#         return self.history_board
    
    def upadate_state(self):
        state_minus_2 = self.state[:,:,:-2].copy()
        state_minus_2 = np.roll(state_minus_2,shift=1,axis=2)
        state_minus_2[:,:,0] = self.gen_2d_state(self.raw_board)[:,:,self.cur_player]

        self.state[:,:,self.history*2 + self.cur_player] = 1
        self.state[:,:,self.history*2 + 1 - self.cur_player] = 0
        self.state[:,:,:-2] = state_minus_2
        
#         return self.state
    
    def is_legal_action(self,action):
        if action[0] in range(self.size) and action[1] in range(self.size):
            return True
        elif action == (-1,-1):
            return True
        else:
            return False
        
    def update_after_action(self,action):
        if self.is_legal_action(action):
            self.cur_player = self.next_player()
            if action != (-1,-1):
                self.raw_board = self.move(action)
                self.update_history_board()
                self.upadate_state()
                
    def num2action(self,num):
        if 0<=num<=self.size*self.size-1:
            i = num // self.size
            j = num % self.size
            return (i,j)
        elif num == self.size * self.size:
            return (-1,-1)
        else:
            return (-2,-2)
        
    def action2num(self,action):
        if self.is_legal_action(action):
            return action[0]*self.size + action[1]
        else:
            return -1
    
    def rot45(self):
        """
        对棋面旋转n×45◦，n∈{0，1，···，7}
        """
        raw_board_list = []
        state_list = []
        history_board_list = []
        
        raw_board_list.append(self.raw_board)
        raw_board_list.append(np.rot90(self.raw_board,1))
        raw_board_list.append(np.rot90(self.raw_board,2))
        raw_board_list.append(np.rot90(self.raw_board,3))
        
        temp = np.transpose(self.raw_board)
        raw_board_list.append(temp)
        raw_board_list.append(np.rot90(temp,1))
        raw_board_list.append(np.rot90(temp,2))
        raw_board_list.append(np.rot90(temp,3))
        
        state_list.append(self.state)
        state_list.append(np.rot90(self.state,1,axes=(0,1)))
        state_list.append(np.rot90(self.state,2,axes=(0,1)))
        state_list.append(np.rot90(self.state,3,axes=(0,1)))
        
        temp = np.transpose(self.state,axes=(1,0,2))
        state_list.append(temp)
        state_list.append(np.rot90(temp,1,axes=(0,1)))
        state_list.append(np.rot90(temp,2,axes=(0,1)))
        state_list.append(np.rot90(temp,3,axes=(0,1)))
        
        history_board_list.append(self.history_board)
        history_board_list.append(np.rot90(self.history_board,1,axes=(1,2)))
        history_board_list.append(np.rot90(self.history_board,2,axes=(1,2)))
        history_board_list.append(np.rot90(self.history_board,3,axes=(1,2)))
        
        temp = np.transpose(self.history_board,axes=(0,2,1))
        history_board_list.append(temp)
        history_board_list.append(np.rot90(temp,1,axes=(1,2)))
        history_board_list.append(np.rot90(temp,2,axes=(1,2)))
        history_board_list.append(np.rot90(temp,3,axes=(1,2)))
        
        return raw_board_list, state_list, history_board_list    
        
        
        