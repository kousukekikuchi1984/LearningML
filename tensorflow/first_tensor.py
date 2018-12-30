# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

def weight(shape=[]):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)

def bias(dtype=tf.float32, shape=[]):
    inital = tf.zeros(shape, dtype=dtype)
    return tf.Variable(inital)

def sigmoid(x):
    return (1 / (1 + tf.exp(-x)))

Q = 5
P = 2
R = 1

sess = tf.InteractiveSession()

X = tf.placeholder(dtype=tf.float32, shape=[None, Q])

W1 = weight(shape=[Q, P])
b1 = bias(shape=[P])
f1 = tf.matmul(X, W1) + b1
# sigm = sigmoid(f1)
sigm = tf.sigmoid(f1)

W2 = weight(shape=[P, R])
b2 = bias(shape=[R])
f2 = tf.matmul(sigm, W2) + b1


init_op = tf.global_variables_initializer()
sess.run(init_op)

y = sess.run(f2, {X: np.array([1, 2, 2, 5, 2]).astype(np.float32).reshape(1, 5)})


