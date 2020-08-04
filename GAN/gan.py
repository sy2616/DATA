import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Genrator(keras.Model):
    def __init__(self):
        super(Genrator,self).__init__()
        self.fc1=layers.Dense(3*3*512)
        self.con1=layers.Conv2DTranspose(256,3,3,'valid')
        self.bn1=layers.BatchNormalization()
        self.con2=layers.Conv2DTranspose(128,5,2,'valid')
        self.bn2=layers.BatchNormalization()
        self.con3=layers.Conv2DTranspose(3,4,3,'valid')

    def call(self,inputs,training=None):
        x=self.fc1(inputs)
        x=tf.reshape(x,[-1,3,3,512])
        x=tf.nn.leaky_relu(x)
        x=tf.nn.leaky_relu(self.bn1(self.con1(x),training=training))
        x=tf.nn.leaky_relu(self.bn2(self.con2(x),training=training))
        x=self.con3(x)
        x=tf.tanh(x)
        return x



class Discriminator(keras.Model):
    def __init__(self):
        super(Discriminator,self).__init__()
        self.con1=layers.Conv2D(64,5,3,'valid')
        self.con2=layers.Conv2D(128,5,3,'valid')
        self.bn2=layers.BatchNormalization()
        self.con3=layers.Conv2D(256,5,3,'valid')
        self.bn3=layers.BatchNormalization()
        self.flat=layers.Flatten()
        self.fc=layers.Dense(1)

    def call(self,inputs,training=None):
        x=tf.nn.leaky_relu(self.con1(inputs))
        x=tf.nn.leaky_relu(self.bn2(self.con2(x),training=training))
        x=tf.nn.leaky_relu(self.bn3(self.con3(x),training=training))
        x=self.flat(x)
        logits=self.fc(x)
        return logits

def main():
    d=Discriminator()
    g=Genrator()
    x=tf.random.normal([2,64,64,3])
    z=tf.random.normal([2,100])
    prob=d(x)
    print(prob)
    x_hat=g(z)
    print(x_hat.shape)

if __name__ == '__main__':
    main()