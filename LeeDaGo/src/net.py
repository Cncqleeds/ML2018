# -*- coding: utf-8 -*-
from config import *

import os
import datetime

import numpy as np
import tensorflow as tf

class Net:
    def __init__(self):
        self.state_ph = tf.placeholder(tf.float32,shape=(None,size,size,state_channal))
        self.z_ph = tf.placeholder(tf.float32,shape=(None,1))
        self.pi_ph = tf.placeholder(tf.float32,shape=(None,n_actions))
        
#        self.training = tf.placeholder(tf.bool) # 区分训练和测试
        self.training = True
        
        self.p_op, self.v_op = self.inference()
        
        self.l_op = self.loss_op()
        
        self.optimizer = self.minimize()
        
        self.saver = self.get_saver()
        
        self.sess = tf.Session()
        
        self.sess.run(tf.global_variables_initializer())
        
    def set_training(self,training=True):
        self.training = training

    def get_training(self):
        return self.training
    
    def get_saver(self):
        """
        将net中的所有训练参数保存
        """
        var_list = tf.trainable_variables()
        g_list = tf.global_variables()
        bn_moving_vars = [g for g in g_list if 'moving_mean' in g.name]
        bn_moving_vars += [g for g in g_list if 'moving_variance' in g.name]
        var_list += bn_moving_vars
        saver = tf.train.Saver(var_list=var_list, max_to_keep=5)
        return saver
        
    def input_module(self,inputs,filters,training):
        outputs = tf.layers.conv2d(inputs,filters=filters,kernel_size=3,padding='same')
        outputs = tf.layers.batch_normalization(outputs,training=training)
        outputs = tf.nn.relu(outputs)
        return outputs

    def residual_module(self,inputs,filters,training):
        outputs = tf.layers.conv2d(inputs,filters=filters,kernel_size=3,padding='same')
        outputs = tf.layers.batch_normalization(outputs,training=training)
        outputs = tf.nn.relu(outputs)

        outputs = tf.layers.conv2d(outputs,filters=filters,kernel_size=3,padding='same')
        outputs = tf.layers.batch_normalization(outputs,training=training)

        outputs += inputs
        outputs = tf.nn.relu(outputs)  
        return outputs
    
    def output_module(self,inputs,fc_units_v,training):
        outputs_v = tf.layers.conv2d(inputs,filters=1,kernel_size=1,padding='same')
        outputs_v = tf.layers.batch_normalization(outputs_v,training=training)
        outputs_v = tf.nn.relu(outputs_v)

        outputs_v = tf.layers.flatten(outputs_v)

        outputs_v = tf.layers.dense(outputs_v,fc_units_v,activation=tf.nn.relu)

        outputs_v = tf.layers.dense(outputs_v,1,activation=tf.nn.tanh)
        
        outputs_p = tf.layers.conv2d(inputs,filters=2,kernel_size=1,padding='same')
        outputs_p = tf.layers.batch_normalization(outputs_p,training=training)
        outputs_p = tf.nn.relu(outputs_p)
        
        outputs_p = tf.layers.flatten(outputs_p)
        
        outputs_p = tf.layers.dense(outputs_p,n_actions,activation=tf.nn.softmax)
        return outputs_p, outputs_v

    def inference(self,fc_units_v=fc_units_v,num_res_module=n_modules):
        inputs = self.input_module(self.state_ph,filters,self.training) # 输入模块
        
        mid_values = inputs
        for i_module in range(n_modules): # 残差模块
            mid_values = self.residual_module(mid_values,filters,self.training)
            
        outputs_p, outputs_v = self.output_module(mid_values,fc_units_v,self.training)
        return outputs_p, outputs_v
        
    def get_var_value(self,var,feed_dict):
        return self.sess.run(var,feed_dict)
    
    def loss_op(self):
        regularizer = tf.contrib.layers.l2_regularizer(scale=lambda_c)
        l2_var = tf.contrib.layers.apply_regularization(\
                    regularizer,tf.trainable_variables())
        
        l_op = l2_var + \
            tf.reduce_mean(\
                tf.reduce_sum(\
                    tf.pow(self.z_ph - self.v_op,2)\
                              - tf.matmul(self.pi_ph,tf.transpose(tf.log(self.p_op))),reduction_indices=[1]))
        return l_op
    
    def minimize(self):
        if self.training:
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                return tf.train.AdamOptimizer().minimize(self.l_op)
        else:
            return tf.train.AdamOptimizer().minimize(self.l_op)
    
    def update(self,feed_dict):
        for it in range(n_iters):
            self.sess.run(self.optimizer,feed_dict)
        
    def save_params(self):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        self.saver.save(self.sess,save_path=model_path)
        print(str(datetime.datetime.now())+": latest model and params saved to path:",model_path)
        
    def restore_params(self):
        if os.path.exists(dir_path):
            self.saver.restore(self.sess,save_path=model_path)
            print(str(datetime.datetime.now())+": last model and params restored from path",model_path)
        else:
            print("Not found %s file"%model_path)
        
            
            
            
if __name__ == "__main__":
    net = Net()
    print(net.get_training())
#    net.restore_params()
    states = np.random.randn(5,size,size,state_channal).astype(np.float32)
    zs = np.ones((5,1),np.float32)
    pis = np.tile(np.array([0.11]*n_actions).astype(np.float32),(5,1))
    
    feed_dict = {net.state_ph:states,net.z_ph:zs,net.pi_ph:pis}

    print("before training Loss:",net.get_var_value(net.l_op,feed_dict))
    
    net.set_training(False)
#    net.update(feed_dict)
    
    print("after training Loss:",net.get_var_value(net.l_op,feed_dict))
    net.save_params()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        