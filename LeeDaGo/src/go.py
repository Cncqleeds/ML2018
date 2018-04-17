# -*- coding: utf-8 -*-

class Go:
    def __init__(self,size = 19):
        self.size = size
        self.ws = set() # 白子
        self.bs = set() # 黑子
        self.wg = set() # 白串
        self.bg = set() # 黑串
        
        self.es = {(i,j) for i in range(size) for j in range(size)} # 无子
        self.raw_board = np.zeros((size,size),np.int8)
        
        self.last_action = None # 上一步 动作
        self.cur_action = None # 当前的动作
        
        self.hands = 0
        self.player = 'B'
        self.records = dict() # 棋谱
        self.ko = None # 劫
        
        self.w_no = set() # 白棋禁入点
        self.b_no = set() # 黑棋禁入点
        
        self.value = .52382 # player获胜的初始概率
        
        self.take_info = dict() # 发生提子的相关信息
        self.take_history = list() # 提子的历史记录信息
        
    def update_es(self):
        self.es = {(i,j) for i in range(self.size) for j in range(self.size)} # 无子
        self.es = self.es - self.ws - self.bs
        
    def render(self): # OK
        print(">> Hand:%3d "%self.hands,"Win Prob: %.2f%%"%(self.value*100))
                
        for i in range(self.size):
            for j in range(self.size):
                c = '.'
                if (i,j) in self.ws:
                    c = 'O'
                elif (i,j) in self.bs:
                    c = 'X'
                print(c,end=' ')
        
            print("%-2d"%(self.size-i))
            
        for k in range(self.size):
            print(chr(k+65),end = ' ')
        print("")    

    def who_win(self):
        """
        如果一方投降（落子到（-2，-2）表示投降）,则另一方获胜
        如果一方落子到非法点（已落有白子、黑子，或对应的禁入点），则另一方获胜
        如果双方均PASS（落子到（-1，-1）表示PASS），则计算各方的地盘大小
        例如：黑方的地盘大小为：b_market = len(bs) + len(w_no) + len(es) / 2
        
        依据围棋一条规则：就是黑棋要让白3又1/4子
        
        如果 b_market - w_market > 3.25 则 黑胜，否则白胜。
        """
        
        if self.cur_action == (-2,-2):
            print(self.player," lose")
            return 1 if self.player == 'B' else -1
        elif not self._is_legal(self.cur_action):
#             print(self.cur_action)
#             print("非法")
            print(self.player," lose")
            return 1 if self.player == 'B' else -1
        elif self.cur_action == (-1,-1) and self.last_action == (-1,-1):
            b_market = len(self.bs) + len(self.w_no) + len(self.es) / 2
            w_market = len(self.ws) + len(self.b_no) + len(self.es) / 2
            
            print(b_marke, w_marke)
            return 1 if (b_market - w_market) > 3.25  else -1
        else:
            return -2
    
#         return 1 # 表示黑棋获胜
#         return 0 # 表示无胜负
#         return -1 # 表示白棋获胜
#         return -2  # 表示暂时不能断定胜负
    
    def _is_legal(self,pos): # OK
        if pos is None:
            return True
        x = pos[0]
        y = pos[1]
        
        # Pass or Resign
        if pos == (-1,-1) or pos == (-2,-2):
            return True
        
        if x<0 or y<0 or x>=self.size or y>=self.size:
            return False
            
        if pos in self.ws:
            return False
        if pos in self.bs:
            return False
        if pos == self.ko:
            return False
            
        ####
        ## 判断是否在禁入点上
        if self.player == 'B':
            if pos in self.b_no:
                return False
            else:
                return True
                
        else:
            if pos in self.w_no:
                return False
            else:
                return True
        ####   
        return True     
        
    def _is_take(self,pos): # OK 判断是否需要提子
        # 需要逻辑判断
        # 例如，当前棋手黑'B',则判断self.wg 中是否有某个串g的airs属性中只含有1个点且该点为pos
        # 如果是，则需要提子，返回True，如果不是，返回False
        
        if self.player == 'B':
            for g in self.wg:
                if g.liberty == 1:
                    if pos in g.airs:
                        return True
        else:
            for g in self.bg:
                if g.liberty == 1:
                    if pos in g.airs:
                        return True
                        
        return False
        
    def _take(self,pos): #  提子
        # 需要更改ws 或 bs中的信息  
        # 需要记录提走了哪些子
        self.take_info['hands'] = self.hands
        self.take_info['player'] = self.player
        self.take_info['pos'] = pos
        self.take_info['stones'] = list()
        if self.player == 'B':
            for g in self.wg:
                if g.liberty == 1:
                    if pos in g.airs:
                        for stone in g.stones:
                            self.ws.remove(stone.pos)
                            self.take_info['stones'].append(stone.pos)
                            
                            
        else:
            for g in self.bg:
                if g.liberty == 1:
                    if pos in g.airs:
                        for stone in g.stones:
                            self.bs.remove(stone.pos)
                            self.take_info['stones'].append(stone.pos)
                            
        self.take_history.append(self.take_info) # 把本次提子信息加入提子历史记录中
        
    def display(self):
        print("当前的白串:")
        for g in self.wg:
            print(g,'\n')
            
        print("当前的黑串:")
        for g in self.bg:
            print(g,'\n')
                 
        print("当前的白棋")
        print(self.ws,'\n')
        
        print("当前的黑棋")
        print(self.bs,'\n')
        
        print("当前的死子")
        print(self.take_history,'\n')
        
        print("当前的劫")
        print(self.ko,'\n')
        
        print("当前的白禁入点")
        print(self.w_no,'\n')
        
        print("当前的黑禁入点")
        print(self.b_no,'\n')
        
        print("当前的棋谱")
        print(self.records)
        
        print("当前的棋手:",self.player)
        
        print("当前的黑子数：",len(self.bs),"白子数",len(self.ws),"黑禁入点数：",len(self.b_no),\
              "白禁入点数：",len(self.w_no),"总数：",len(self.bs)+len(self.ws)+len(self.b_no)+len(self.w_no))

    
    """
    update方法是围棋的核心方法，根据当前局面更新相关信息(wg,bg,ko,w_no,b_no)
    
    递归扫描每个点，并对扫描过的点做标记，直到递归结束，生成一个group
    如果该点已经做过标记，则跳过，如果没有标记，则再递归生成一个group。这样就完成了 wg 和 bg的更新
    
    
    对于劫ko的计算
    如果take_info 中有内容，则发生了提子，根据take_info计算ko点
    提了对方一子，如果对方在死子的位置落子,也能提走本方的落子，且本方落子的所在的组的长度为1，则该点为ko点
    
    
    对于禁入点的计算
    比如 计算 黑禁入点 b_no
    扫描每个非落子点，如果该点的四周都有子，则考虑四周各串的liberty == 1的情况
    如果该group为黑串，且四周的白串的liberty都>1,则该点为黑禁入点
    
    同样的思路 考虑该非落子点是否为白禁入点 w_no
    
    """
    def update(self):
        self.wg = set()
        self.bg = set()
        self.ko = None
        self.b_no = set()
        self.w_no = set()
        
        # 生成标记
        labels = dict()
        for i in range(self.size):
            for j in range(self.size):
                    labels[(i,j)] = 0  # 初始化为未扫描标记0
                    
        """
        递归扫描每个点，并对扫描过的点做标记，直到递归结束，生成一个group
        如果该点已经做过标记，则跳过，如果没有标记，则再递归生成一个group。这样就完成了 wg 和 bg的更新
        """                   
        for i in range(self.size):
            for j in range(self.size):
                point = (i,j) #扫描这个点
                if labels[point] == 0: # 没有扫描
                    labels[point] = 1 # 标识为已扫描
                    stone = None
                    color = None
                    if point in self.ws:
                        stone = Stone(point[0], point[1],'W')
                        color = 'W'
                    elif point in self.bs:
                        stone = Stone(point[0], point[1],'B')
                        color = 'B'
                    if stone:
                        group = Group()
                        group.add_stone(stone)
                        
                        w_group_set,b_group_set,airs_set = self.get_sets(point)
                        
                        for air in airs_set: # 加入气点
                            group.add_air(air)
                        
                        if color == 'B':
                            for g in b_group_set:
                                
                                group.merge(g)
#                                print("TBT",group)
                                self.bg.remove(g)
                                
                                for s in g.stones:
                                    labels[s.pos] = 1
                                self.bg.add(group)

                            self.bg.add(group)

                                
                        elif color == 'W':
                            for g in w_group_set:
#                                print("TWT",g)
                                group.merge(g)
                                self.wg.remove(g)
                            
                                for s in g.stones:
                                    labels[s.pos] = 1

                                self.wg.add(group)
        
                            self.wg.add(group)
                         
                        
        """                    
        对于劫ko的计算
        如果take_info 中有内容，则发生了提子，根据take_info计算ko点
        提了对方一子，如果对方在死子的位置落子,也能提走本方的落子，且本方落子的所在的组的长度为1，则该点为ko点
        """
        if self.take_info:
            if len(self.take_info['stones']) == 1:
#                print("提了一个")
                for stone in self.take_info['stones']:
                    take_point = stone
                pos = self.take_info['pos']
                group,_ = self.query_group(pos)
#                print(group)
                if len(group.stones) == 1:
                    if group.liberty == 1:
                        self.ko = take_point
                        
                        
        """
        对于禁入点的计算
        比如 计算 黑禁入点 b_no
        扫描每个非落子点，如果该点的四周都有子，则考虑四周各串的liberty == 1的情况
        如果该group为黑串，且四周的白串的liberty都>1,且四周的黑串的liberty都=1,则该点为黑禁入点
        """
        for i in range(self.size):
            for j in range(self.size):
                point = (i,j)
                if point not in self.ws and point not in self.bs:
                    cur_player = self.player
                    if self.player == 'W':
                        self.player = 'B'
                        
                    take_flag = self._is_take(point)
                    if take_flag:
                        # 如何可以提子，则此点肯定不是黑禁入点
                        pass
                    else:
                        # 如果不能提子，且该点周围的黑串的气都为1，则该点为黑禁入点
                        w_group_set,b_group_set,airs_set = self.get_sets(point)
                        b_flag = True
                        for bg in b_group_set:
                            if bg.liberty > 1:
                                b_flag = False
                                
                        if b_flag and not airs_set:
                            self.b_no.add(point)
                           
                ###############
                           
                    if self.player == 'B':
                        self.player = 'W'
                    take_flag = self._is_take(point)
                    if take_flag:
                        # 如何可以提子，则此点肯定不是白禁入点
                        pass
                    else:
                        # 如果不能提子，且该点周围的白串的气都为1，则该点为白禁入点
                        w_group_set,b_group_set,airs_set = self.get_sets(point)
                        w_flag = True
                        for wg in w_group_set:
                            if wg.liberty >1:
                                w_flag = False
    
                        if w_flag and  not airs_set:
                           self.w_no.add(point)   
                           
                         
                    self.player = cur_player
        
    def update_raw_board(self):
        self.raw_board = np.zeros((self.size,self.size),np.int8)
        for s in self.bs:
            self.raw_board[s] = -1
        for s in self.ws:
            self.raw_board[s] = 1
            
        
            
           
     
    """
    围棋的核心方法，根据当前局面更新相关信息(wg,bg,ko,w_no,b_no)
    """
    
     
    def get_neighbors(self,pos): # 得到pos周围的坐标
        x = pos[0]
        y = pos[1]
        if x<0 or y<0 or x>=self.size or y>=self.size:
            return list()
        xs = [x-1,x+1]
        ys = [y-1,y+1]
        
        if x-1 <0:
            xs.remove(x-1)
        if x+1>self.size-1:
            xs.remove(x+1)
            
        if y-1 <0:
            ys.remove(y-1)
        if y+1>self.size-1:
            ys.remove(y+1)
            
        results = []

        for r in xs:
            results.append((r,y))
        for c in ys:
            results.append((x,c))
             
        return results
        
    def query_pos(self,pos): # 查询某个位置属于黑棋 白棋，空地
        if pos in self.ws:
            return 1 # 白子
        elif pos in self.bs:
            return 0 # 黑子
        else:
            return -1 #空地
            
    def query_group(self, pos): #  查询某个位置属于哪个group
        for g in self.bg:
            for s in g.stones:
                if pos[0] == s.x and pos[1] == s.y:
                    return g,'B'
        for g in self.wg:
            for s in g.stones:
                if pos[0] == s.x and pos[1] == s.y:
                    return g,'W'
                    
        return None,'E'
    
        
    def get_sets(self,pos): # 得到该pos四周的组
        neighbors = self.get_neighbors(pos)
        w_group_set = set()
        b_group_set = set()
        airs_set = set()
        if neighbors:
            for neighbor in neighbors:
                if self.query_pos(neighbor) == -1:
                    airs_set.add(neighbor)
                else:
                    g,c = self.query_group(neighbor)
                    if c == 'B':
                        b_group_set.add(g)
                    elif c == 'W':
                        w_group_set.add(g)
                    
        return w_group_set,b_group_set,airs_set
    
    """
    落子方法
    """    
    def move(self,pos):
        
        
        
        #0 手数加1
        self.hands += 1 
        #1 判断是否合法
        if not self._is_legal(pos):
            cur_pos = 'PASS'
#            print('PASS',pos)
        else:
            cur_pos = str(pos)

            #2 判断是否提子
            if self._is_take(pos):
                self._take(pos)
#                print("TAKE",pos)
                # 是，提走棋子
            else:
                self.take_info = dict()
            
            
            # 3.1 添加当前棋子到黑子集合或白子集合
            if self.player == 'B':
                self.bs.add(pos)
            else:
                self.ws.add(pos)
                
            # 3.2 根据当前局面 更新相关信息, ***** 核心 *****
        self.update()
        self.update_raw_board()
        self.update_es()
            
        #4 更新记录棋谱
        self.records[self.hands] = cur_pos
        #5 切换棋手
        self.player = 'W' if self.player == 'B' else 'B'

   