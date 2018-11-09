import tensorflow as tf
import tensorflow.contrib.eager as tfe
import numpy as np


class Net(tf.keras.Model):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(10, 5)
        self.conv2 = tf.keras.layers.Conv2D(20, 5)
        self.fc1 = tf.keras.layers.Dense(50)
        self.fc1 = tf.keras.layers.Dense(10)

    def call(self, x):
        x = tf.nn.relu(
                tf.nn.max_pool(
                    self.conv1(x),
                    [1, 2, 2,1],
                    [1, 1, 1, 1,],
                    'VALID'))
        x = self.conv2(x)
        x = tf.nn.relu(
                tf.nn.max_pool(
                    self.conv1(x),
                    [1, 2, 2,1],
                    [1, 1, 1, 1,],
                    'VALID'))
        x = tf.layers.flatten(x)
        x = tf.nn.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def main():
    model = Net()
    X = np.random.randn(100, 28, 28, 1)
    X = tf.convert_to_tensor(X, tf.float32)

##     model.eval()
    model.compile(tf.train.AdamOptimizer())
    print(model.summary())

    Y1 = model(X)
    model.eval()
    print(model.training)

    Y2 = model(X)
    model.eval()
    print(model.training)

    Y3 = model(X)

    print(Y1.numpy() == Y2.numpy())
    print(Y1.numpy() == Y3.numpy())



if __name__ == '__main__':
    main()
