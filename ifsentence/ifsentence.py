# -*- coding: utf-8 -*-

import tensorflow as tf

boolian = tf.placeholder(dtype=tf.bool)
a = tf.placeholder(dtype=tf.float32)
b = tf.placeholder(dtype=tf.float32)

x = tf.cond(boolian, lambda: a+b, lambda: a*b)

print( tf.Session().run(x, feed_dict={boolian: True, a: 1, b: 2})  )
