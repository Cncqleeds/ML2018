# -*- coding: utf-8 -*-

class Stone: # 棋子
    def __init__(self,x,y,c):
        self.x = x
        self.y = y
        self.c = c # 标识黑白子{'B','W'}
        self.pos = (x,y)
    def __call__(self,x,y,c):
        self.x = x
        self.y = y
        self.c = c 
        self.pos = (x,y)
        return self       
    def __str__(self):
        return str(self.c) + "_" + str(self.x) + "_" + str(self.y)