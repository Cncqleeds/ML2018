# -*- coding: utf-8 -*-
from config  import *
import net
import simulator


class TreeNode:
    def __init__(self,parent,prior_p,layer):
        self._parent = parent
        self._children = dict()
        self._n_visits = 0 # 节点遍历次数
        
        self._Q = 0 # 动作平均值
        self._W = 0 # 动作累计值
        self._u = prior_p # 动作置信值, 根节点不存在置信值
        self._p = prior_p # 动作先验概率
        self.layer = layer
        
        
    def render(self):
        print(self.layer,",Q:%.3f, W:%.3f, U:%.3f, N:%3d, Prob:%.3f"%(self._Q,self._W,self._u,self._n_visits,self._p))
        for action, node in self._children.items():
            node.render()
#             if node._children:
#                 node.render()
        
        
    def select(self):
        return max(self._children.items(), key=lambda act_node: act_node[1].get_value())
    
    def get_value(self):
        return self._Q + self._u
    
    def expand(self, action_priors):
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self,prob,self.layer+1)
                
    def evaluation(self,leaf_value,c_puct):
        self._n_visits += 1
        self._W += leaf_value
        self._Q = self._W / self._n_visits
        if not self.is_root():
            self._u = c_puct * self._p * np.sqrt(self._parent._n_visits) / (1+self._n_visits)

    def is_root(self):
        return self._parent is None
    
    def is_leaf(self):
        return self._children == dict()
    
    def backup(self,leaf_value,c_puct):
        
        
        if self._parent:
            self._parent.backup(leaf_value,c_puct)
            
        self.evaluation(leaf_value,c_puct)
        
        
class MCTS:
    def __init__(self,net,simulator):
        self.net = net
        self.simulator = simulator
        
        self._root = TreeNode(None,1.0,1)
        self.root = self._root
        self.c_puct = c_puct
        self.max_search_depth = max_search_depth
        self.n_search = n_search
        self.cur_depth = 0
        self.cur_node = self._root
        
        self.root_state = self.simulator.cur_state
        self.cur_state = self.root_state.copy()
        
        self.pis = []
        
        
    def search(self):
        while self.cur_depth < self.max_search_depth:
            if not self.cur_node.is_leaf():
#                 print(self.cur_state)
                
                action, self.cur_node = self.cur_node.select()
                
                self.cur_state = self.simulator.get_state(self.cur_state.copy(),action)
                
                self.cur_depth += 1
            else:
                action_priors = enumerate(self.net.get_var_value(self.net.p_op,{self.net.state_ph:self.cur_state}).reshape(-1).tolist())
                self.cur_node.expand(action_priors)
                
                leaf_value = self.net.get_var_value (self.net.v_op,{self.net.state_ph:self.cur_state})[0,0]
#                 print("leaf_value",leaf_value)
                self.cur_node.backup(leaf_value,self.c_puct)
    
                
    def policy(self,tau):
        for it in range(self.n_search):
#             print("第%d次搜索"%(it+1))
            self.search()
            self.cur_node = self._root
            self.cur_state = self.root_state
            self.cur_depth = 0
            
        pi = [x._n_visits for _,x in self._root._children.items()]
   
        # 需考虑退火 温度系数，
        pi = (np.power(pi,1/tau)/np.sum(np.power(pi,1/tau))).tolist()
        self.pis.append(pi)
        return pi
    
    def choice(self,tau):
        pi = self.policy(tau)
#         print(pi)
        action = np.random.choice(range(len(pi)),p=pi)
        self.action = action
        self.next_prepare()
        return action
    
    def next_prepare(self):
        self._root = self._root._children[self.action]
        self._root._parent = None
        self.simulator.move(self.action)
        self.root_state = self.simulator.cur_state.copy()
        self.cur_state = self.root_state.copy()
        
        self.cur_depth = 0
        self.cur_node = self._root

        return self
        
        
if __name__ == "__main__":
   tree = TreeNode(None,1.0,1)
   tree.render() 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    