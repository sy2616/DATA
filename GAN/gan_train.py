import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
import glob
from gan import Genrator,Discriminator
from dataset import make_anime_dataset

def celoss_ones(logits):
    loss=tf.nn.sigmoid_cross_entropy_with_logits(logits=logits,
                                                 labels=tf.ones_like(logits))
    return tf.reduce_mean(loss)


def celoss_zeros(logits):
    loss=tf.nn.sigmoid_cross_entropy_with_logits(logits=logits,
                                                 labels=tf.zeros_like(logits))
    return tf.reduce_mean(loss)

def d_loss_fn(generator,dis,batch_z,batch_x,is_training):
    fake_img=generator(batch_z,is_training)
    d_fake_logits=dis(fake_img,is_training)
    d_real_logits = dis(batch_x, is_training)

    d_loss_real=celoss_ones(d_real_logits)
    d_loss_fake=celoss_zeros(d_fake_logits)
    loss=d_loss_fake+d_loss_real
    return loss

def main():
    tf.random.set_seed(222)
    np.random.seed(222)
    z_dim=100
    epochs=3000000
    batch_size=512
    learning_rate=0.002
    is_training=True
    img_path=glob.glob(r'D:\BaiduNetdiskDownload\faces\faces\*.jpg')
    dataset,img_shape,_=make_anime_dataset(img_path,batch_size)
    print(dataset,img_shape)
    sample=next(iter(dataset))
    print(sample.shape)
    dataset=dataset.repeat()
    db_iter=iter(dataset)

    generator=Genrator()
    generator.build(input_shape=(None,z_dim))

    dis=Discriminator()
    dis.bulid(input_shape=(None,64,64,3))
    g_optimaizer=tf.optimizers.Adam(learning_rate=learning_rate,beta_1=0.50)
    d_optimaer=tf.optimizers.Adam(learning_rate=learning_rate,beta_2=0.5)
    for epoch in range(epochs):
        batch_z=tf.random.uniform([batch_size,z_dim],minval=-1,maxval=1)
        batch_x=next(db_iter)
        with tf.GradientTape() as tape:
            d_loss=d_loss_fn(generator,dis,batch_z,batch_x,is_training)
        grads=tape.gradient(d_loss,dis.trainable_varables)
        d_optimaer.apply_gradients(zip(grads,dis.trainable_varables))

        with tf.GradientTape() as tape:
            
if __name__ == '__main__':
    main()