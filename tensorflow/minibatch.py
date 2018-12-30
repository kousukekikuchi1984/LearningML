# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf


def weight(shape = []):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias(dtype = tf.float32, shape = []):
    initial = tf.zeros(shape, dtype = dtype)
    return tf.Variable(initial)

def loss(t, f):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(t * tf.log(f)))
    return cross_entropy

def accuracy(t, f):
    correct_prediction = tf.equal(tf.argmax(t, 1), tf.argmax(f, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    return accuracy

Q = 4
P = 4
R = 3

sess = tf.InteractiveSession()

X = tf.placeholder(dtype = tf.float32, shape = [None, Q])
t = tf.placeholder(dtype = tf.float32, shape = [None, R])

W1 = weight(shape = [Q, P])
b1 = bias(shape = [P])
f1 = tf.matmul(X, W1) + b1
sigm = tf.nn.sigmoid(f1)

W2 = weight(shape = [P, R])
b1 = bias(shape = [R])
f2 = tf.matmul(sigm, W2) + b1
f = tf.nn.softmax(f2)

loss = loss(t, f)
acc = accuracy(t, f)

optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.001)
train_step = optimizer.minimize(loss)

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    # Set up figure.
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, frameon=False)
    plt.ion()
    plt.show()
    plt.grid()

    from sklearn import datasets
    iris = datasets.load_iris()
    shuffle = np.random.permutation(150)
    train_x = iris.data[shuffle[:100]]
    train_t = iris.target[shuffle[:100]]
    train_t = np.eye(3)[train_t]
    test_x = iris.data[shuffle[100:]]
    test_t = iris.target[shuffle[100:]]
    test_t = np.eye(3)[test_t]

    num_epoch = 10000
    num_data = train_x.shape[0]
    batch_size = 1
    loss_list_tr = []
    loss_list_tes = []
    epoch_list = []
    for epoch in range(num_epoch):

        if batch_size < num_data:
            batch_size += 1
        sff_idx = np.random.permutation(num_data)

        for idx in range(0, num_data, batch_size):
            batch_x = train_x[sff_idx[idx: idx + batch_size
                if idx + batch_size < num_data else num_data]]
            batch_t = train_t[sff_idx[idx: idx + batch_size
                if idx + batch_size < num_data else num_data]]
            sess.run(train_step, feed_dict = {X: batch_x, t: batch_t})

        if epoch % 100 == 0:
            train_loss = sess.run(loss, feed_dict = {X: train_x, t: train_t})
            train_acc = sess.run(acc, feed_dict = {X: train_x, t: train_t})
            test_loss = sess.run(loss, feed_dict = {X: test_x, t: test_t})
            test_acc = sess.run(acc, feed_dict = {X: test_x, t: test_t})
            print('epoch:{} \n \
                   tr_loss:{}\n \
                   tr_acc:{} \n \
                   tes_loss:{} \n \
                   tes_acc:{}'.format(epoch,
                                      train_loss,
                                      train_acc,
                                      test_loss,
                                      test_acc))

            # print data and functions
            loss_list_tr.append(train_loss)
            loss_list_tes.append(test_loss)
            epoch_list.append(epoch)
            plt.cla()
            p1, = ax.plot(epoch_list, loss_list_tr)
            p2, = ax.plot(epoch_list, loss_list_tes)
            plt.grid()
            plt.legend([p1, p2], ["train loss","validation loss"])
            plt.draw()
            plt.pause(1.0 / 60.0)
