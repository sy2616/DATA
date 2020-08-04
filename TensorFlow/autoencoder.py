import os
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

tf.random.set_seed(11)
np.random.seed(11)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
assert tf.__version__.startswith('2.')

def save_images(imgs,name):
    new_im=Image.new('L',(280,280))
    index=0
    for i in range(0,280,28):
        for j in range(0,280,28):
            im=imgs[index]
            im=Image.fromarray(im,mode='L')
            new_im.paste(im,(i,j))
            index+=1
    new_im.save(name)

h_dim=20
batch_sz=512
lr=1e-3

(x_train,y_train),(x_test,y_test)=keras.datasets.fashion_mnist.load_data()
x_train,x_test=x_train.astype(np.float32)/255.,x_test.astype(np.float32)/255.
train_db=tf.data.Dataset.from_tensor_slices(x_train)
train_db=train_db.shuffle(batch_sz*5).batch(batch_sz)
test_db=tf.data.Dataset.from_tensor_slices(x_test)
test_db=test_db.batch(batch_sz)
print(x_train.shape,y_train.shape)
print(x_test.shape,y_test.shape)


class AE(keras.Model):
    def __init__(self):
        super(AE,self).__init__()
        #encoder
        self.encoder=keras.Sequential([
            keras.layers.Dense(256,activation=tf.nn.relu),
            keras.layers.Dense(128,activation=tf.nn.relu),
            keras.layers.Dense(h_dim)
        ])

        self.decoder=keras.Sequential([
            keras.layers.Dense(128,activation=tf.nn.relu),
            keras.layers.Dense(256,activation=tf.nn.relu),
            keras.layers.Dense(784)
        ])

    def call(self,inputs,training=None):
        h=self.encoder(inputs)
        h_hat=self.decoder(h)
        return h_hat

model=AE()
model.build(input_shape=(None,784))
model.summary()
optimazer=tf.optimizers.Adam(lr=lr)
for epoch in range(100):
    for step,x in enumerate(train_db):
        x=tf.reshape(x,[-1,784])
        with tf.GradientTape() as tape:
            x_rec_logits=model(x)
            rec_loss=tf.losses.binary_crossentropy(x,x_rec_logits,from_logits=True)
            rec_loss=tf.reduce_mean(rec_loss)
        grads=tape.gradient(rec_loss,model.trainable_variables)
        optimazer.apply_gradients(zip(grads,model.trainable_variables))

        if step%100==0:
            print(epoch,step,'loss:',float(rec_loss))

        x=next(iter(test_db))
        # x=tf.reshape(x,[-1,784])
        logits=model(tf.reshape(x,[-1,784]))
        x_hat=tf.sigmoid(logits)
        x_hat=tf.reshape(x_hat,[-1,28,28])
        x_concat=tf.concat([x,x_hat],axis=0)
        x_concat=x_concat.numpy()*255.
        x_concat=x_concat.astype(np.uint8)
        save_images(x_concat,'ae_images/rec_epoch_%d.png'%epoch)

