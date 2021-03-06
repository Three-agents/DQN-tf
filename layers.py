import tensorflow as tf
from tensorflow.contrib.layers.python.layers import initializers


# using https://github.com/devsisters/DQN-tensorflow/blob/master/dqn/ops.py

def conv2d(x,
           output_dim,
           kernel_size,
           stride,
           initializer=tf.contrib.layers.xavier_initializer(),
           activation_fn=tf.nn.relu,
           padding='VALID',
           name='conv2d'):
    with tf.variable_scope(name):
        stride = [1, stride[0], stride[1], 1]
        kernel_shape = [kernel_size[0], kernel_size[1], x.get_shape()[-1], output_dim]

        w = tf.get_variable('w', kernel_shape, tf.float32, initializer=initializer)
        conv = tf.nn.conv2d(x, w, stride, padding)

        b = tf.get_variable('biases', [output_dim], initializer=tf.constant_initializer(0.0))
        out = tf.nn.bias_add(conv, b)

    if activation_fn != None:
        out = activation_fn(out)

    return out, w, b


def linear(input_, output_dim, stddev=0.02, bias_start=0.0, activation_fn=None, name='linear'):
    shape = input_.get_shape().as_list()

    with tf.variable_scope(name):
        w = tf.get_variable('Matrix', [shape[1], output_dim], tf.float32,
                            tf.random_normal_initializer(stddev=stddev))
        b = tf.get_variable('bias', [output_dim],
                            initializer=tf.constant_initializer(bias_start))

        out = tf.nn.bias_add(tf.matmul(input_, w), b)

        if activation_fn != None:
            return activation_fn(out), w, b
        else:
            return out, w, b
