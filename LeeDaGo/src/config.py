# -*- coding: utf-8 -*-

size = 9 #19
history = 2 #8
state_channal = history*2 + 2 # 2 * history +1
filters = 16 #256
fc_units_v = 256
n_modules = 3 # 19
lambda_c = 0.0001
n_actions = size*size + 1
c_puct = 5 
epsilon = 0.25
eta = 0.03
init_tau = 1.0
n_search = 1600
max_search_depth = 50
max_play_steps = 500
v_resign = -0.95
n_iters = 1000

dir_path = "../data/model_save"
model_path = dir_path + "/model_net_demo.ckpt"