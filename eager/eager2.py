# -*- coding: utf-8 -*-

import tensorflow as tf
import tensorflow.contrib.eager as tfe

tfe.enable_eager_execution()

w = tfe.Variable(tf.zeros([3, 2]))

tf.global_variables_initializer()

print("w = %s" % w)

tf.assign(w, tf.ones([3, 2]))
print("w = %s" % w)
