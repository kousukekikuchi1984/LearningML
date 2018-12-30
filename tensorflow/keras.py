# -*- coding: utf-8 -*-

## Keras Sequential
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(32, input_shape=()500,))
model.add(tf.keras.layers.Dense(32))
model.compile(optimizer=optimizer, loss=loss)
model.fit(x, y, batch_size=32, epochs=10)

## Modelによるfuncitonal API
### 枝分かれするNWやロスが複数ある場合
inputs = tf.keras.Input(shape=(500,))
x = tf.keras.layers.Dense(32, activation=tf.nn.relu)(inputs)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=optimizer, loss=loss)
model.fit(x, y, batch_size=32, epochs=10)

## Eager
class MyModel(tf.keras.Model):

    def __init__(self):
        super(MyModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(32, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(32, activation=tf.nn.softmax)

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)


model = MyModel()
model.compile(optimizer=optimizer, loss=loss)
model.fit(x, y, batch_size=32, epochs=10)

## Eager with dropout
class MyDropoutModel(tf.keras.Model):

    def __init__(self):
        super(MyDropoutModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(32, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(32, activation=tf.nn.softmax)
        self.dropout = tf.keras.layers.Dropout(0.5)

    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        if training:
            x = self.dropout(x, training=training)
        return self.dense2(x)

model = MyDropoutModel()


