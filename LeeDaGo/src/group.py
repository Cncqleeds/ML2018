# -*- coding: utf-8 -*-

class Group: # 棋子整体串
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.stones = set() # 棋子集合
        self.airs = set() # 气点集合
        self.liberty = 0 # 气数
        self.opponents = set() #棋子整体周围的对方棋子整体
        
    def __str__(self):
        res = "{"
        
        for s in self.stones:
            res += str(s)
            res += " "
            
        res += "} Lives:"
        res += str(self.liberty)
        
        res += " Airs:" + str(self.airs)
        return res
        
    def add_stone(self,stone):
        self.stones.add(stone)
        
    def del_stone(self,stone):
        if stone in self.stones:
            self.reset()
            
    def add_op(self,op):
        self.opponents.add(op)
        
    def del_op(self,op):
        if op in self.opponents:
            self.opponents.remove(op)
        
    def add_air(self,air):
        self.airs.add(air)
        self.liberty = len(self.airs)
        
    def del_air(self,air):
        if air in self.airs:
            self.airs.remove(air)
            self.liberty = len(self.airs)
            
    def merge(self,group):
        self.stones = self.stones.union(group.stones)
        self.airs = self.airs.union(group.airs)
        self.liberty = len(self.airs)
        
        return self