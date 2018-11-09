# -*- coding: utf-8 -*-

import tensorflow as tf

w = tf.Variable(tf.zeros([3, 2]))

with tf.Session() as sess:
    sess.run( tf.global_variables_initializer() )
    print("w = %s" % sess.run(w))

    sess.run( tf.assign(w, tf.ones([3, 2])) )
    wn = sess.run(w)
    print("w = %s" % wn)
