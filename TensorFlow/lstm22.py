import tensorflow as tf
from tensorflow.keras import datasets, Sequential, layers, optimizers, metrics
import os
import numpy as np
from tensorflow import keras

tf.random.set_seed(11)
np.random.seed(111)

total_words = 10000
max_len = 80
batchsz = 128
embedding_len = 100
(x_train, y_train), (x_test, y_test) = datasets.imdb.load_data(num_words=total_words)
x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, maxlen=max_len)
x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test, maxlen=max_len)
db_train = tf.data.Dataset.from_tensor_slices((x_train, y_train))
db_train = db_train.shuffle(1000).batch(batchsz, drop_remainder=True)
db_test = tf.data.Dataset.from_tensor_slices((x_test, y_test))
db_test = db_test.batch(batchsz, drop_remainder=True)
print('x_train:', x_train.shape, tf.reduce_min(y_train), tf.reduce_max(y_train))
print('x_test:', x_test.shape)


class Myrnn(keras.Model):
    def __init__(self, units):
        super(Myrnn, self).__init__()
        self.state0 = [tf.zeros([batchsz, units]), tf.zeros([batchsz, units])]
        self.state1 = [tf.zeros([batchsz, units]), tf.zeros([batchsz, units])]
        self.embedding = layers.Embedding(total_words, embedding_len,
                                          input_length=max_len)
        # self.rnn_cell0 = layers.LSTMCell(units, dropout=0.2)
        # self.rnn_cell1 = layers.LSTMCell(units, dropout=0.2)
        self.rnn=Sequential([
            layers.LSTM(units,dropout=0.2,return_sequences=True,unroll=True),
            layers.LSTM(units,dropout=0.2,unroll=True)
        ]
        )
        self.fc = layers.Dense(1)

    def call(self, inputs, training=None):
        x = inputs
        x = self.embedding(x)
        # state0 = self.state0
        # state1 = self.state1
        # for word in tf.unstack(x, axis=1):
        #     # out0, state0 = self.rnn_cell0(word, state0, training)
        #     # out1, state1 = self.rnn_cell1(out0, state1, training)
        # out1,state1=self.rnn(word,state0,training)
        x=self.rnn(x)
        x = self.fc(x)
        prob = tf.sigmoid(x)
        return prob


def main():
    units = 64
    epochs = 4
    model = Myrnn(units)
    # model.build(input_shape=[None,units])
    # model.summary()
    model.compile(optimizer=optimizers.Adam(lr=1e-3),
                  loss=tf.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])
    model.fit(db_train, epochs=epochs, validation_data=db_test, validation_freq=1)
    model.summary()

    model.evaluate(db_test)


if __name__ == '__main__':
    main()


