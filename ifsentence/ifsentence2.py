# -*- coding: utf-8 -*-

import tensorflow as tf

boolean = tf.placeholder(dtype=tf.bool)
a = tf.placeholder(dtype=tf.float32)
b = tf.placeholder(dtype=tf.float32)

x = tf.where(boolean, a+b, a*b)

print(tf.Session().run(x, feed_dict={boolean: True, a: 1, b: 2}))
print(tf.Session().run(x, feed_dict={boolean: False, a: 1, b: 2}))
