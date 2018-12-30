# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

def weight(shape=[]):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)

def bias(dtype=tf.float32, shape=[]):
    initial = tf.zeros(shape, dtype=dtype)
    return tf.Variable(initial)

def loss(t, f):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(t*tf.log(f)))
    return cross_entropy

def accuracy(t, f):
    correct_predictions = tf.equal(tf.argmax(t, 1), tf.argmax(f, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32))
    return accuracy

Q = 4
P = 4
R = 3

def main():
    sess = tf.InteractiveSession()

    # model definition
    X = tf.placeholder(dtype=tf.float32, shape=[None, Q])
    t = tf.placeholder(dtype=tf.float32, shape=[None, R]) ## 教師データ

    W1 = weight(shape=[Q, P])
    b1 = bias(shape=[P])
    f1 = tf.matmul(X, W1) + b1
    sigm = tf.nn.sigmoid(f1)

    W2 = weight(shape=[P, R])
    b2 = bias(shape=[R])
    f2 = tf.matmul(sigm, W2) + b2
    f = tf.nn.softmax(f2) ## for classification

    loss_ = loss(t, f) ## loss関数
    acc = accuracy(t, f)

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01) ##確率勾配法を用いてロス関数を定義
    train_step = optimizer.minimize(loss_) ## loss関数の最小化

        # Data Preparation
    from sklearn import datasets
    iris = datasets.load_iris()
    train_x = iris.data
    train_t = iris.target
    train_t = np.eye(3)[train_t] ## Convert to One-Hot Expression

    with tf.Session() as sess:
        # Execution
        init = tf.global_variables_initializer()
        sess.run(init)


        num_epoch = 10000
        for epoch in range(num_epoch):
            sess.run(train_step, feed_dict={X: train_x, t:train_t})
            if epoch % 100 == 0:
                train_loss = sess.run(loss_, feed_dict={X: train_x, t: train_t})
                train_acc = sess.run(acc, feed_dict={X: train_x, t: train_t})
                print('epoch: {} loss: {} accuracy: {}'.format(epoch,
                    train_loss, train_acc))

if __name__ == '__main__':
    main()
