# -*- coding:utf-8 -*-

import tensorflow as tf
import tensorflow.contrib.eager as tfe

tfe.enable_eager_execution()

const1 = tf.constant(2)
const2 = tf.constant(3)
add_op = tf.add(const1, const2)

print(add_op)
type(add_op)
print(add_op + 3)
add_op2 = add_op + 3
print(add_op2.numpy())

