# -*- coding: utf-8 -*-
class Simulator:
    def __init__(self):
        self.size = size
        self.cur_state = np.zeros((1,size,size,1),dtype=np.float32)
        self.records = [self.cur_state.copy()]
        self.action_records = []
        self.cur_hands = 0
        self.n_actions = size**2
        
    def move(self,action):
        self.cur_hands += 1
        state = self.cur_state
        
        if action>self.n_actions or action<0:
            print("pass")
        elif action == self.n_actions:
            print("pass")
        else:
            i = action//self.size
            j = action % self.size
            state[0,i,j,0] += 1
        self.cur_state = state
#         print("move")
        self.records.append(state.copy())
        self.action_records.append(action)
        
    def get_state(self,state,action):
        if  not (action>self.n_actions or action<0):
            i = action//self.size
            j = action % self.size
            state[0,i,j,0] += 1
            
        return state
    
    def render(self):
        print("hands:",self.cur_hands)
        print("state: \n")
        print(self.cur_state.reshape((3,3)))
        
    def is_done(self):
        if abs(np.linalg.det(state)) >= 1:
            return True
        else:
            return False
        
    def who_win(self,state):
        state = state.reshape((size,size))
        res = np.linalg.det(state)
        if res == 1.:
            return 1.
        elif res > 1.:
            return -1.
        else:
            return 0.
        
    def state_rot(self):
        pass
    def board_to_state(self):
        pass
    def state_to_board(self):
        pass
    
    

