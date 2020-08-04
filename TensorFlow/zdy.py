import tensorflow as tf
from tensorflow.keras import datasets,layers,optimizers,Sequential,metrics
from tensorflow import keras

def preprocess(x,y):
    x=tf.cast(x,dtype=tf.float32)/255
    x=tf.reshape(x,[28*28])
    y=tf.cast(y,dtype=tf.int32)
    y=tf.one_hot(y,depth=10)
    return x,y

batchsz=128
tf.random.set_seed(22)
(x,y),(x_val,y_val)=datasets.mnist.load_data()
print('datasets:',x.shape,y.shape,x.min(),x.max())

db=tf.data.Dataset.from_tensor_slices((x,y))
db=db.map(preprocess).shuffle(60000).batch(batchsz)
ds_val=tf.data.Dataset.from_tensor_slices((x_val,y_val))
ds_val=ds_val.map(preprocess).batch(batchsz)

sample=next(iter(db))
print(sample[0].shape,sample[1].shape)

network=Sequential([layers.Dense(256,activation='relu'),
                    layers.Dense(128,activation='relu'),
                    layers.Dense(64,activation='relu'),
                    layers.Dense(32,activation='relu'),
                    layers.Dense(10)])
network.build(input_shape=(None,28*28))
network.summary()

class MyDense(layers.Layer):
    def __init__(self,inp_dim,oup_dim):
        super(MyDense,self).__init__()
        self.kernel=self.add_variable('w',[inp_dim,oup_dim])
        self.bias=self.add_variable('b',[oup_dim])

    def call(self,inpts,training=None):
        out=inpts@self.kernel+self.bias
        return out

class MyModel(keras.Model):
    def __init__(self):
        super(MyModel,self).__init__()
        self.fc1=MyDense(28*28,256)
        self.fc2=MyDense(256,128)
        self.fc3=MyDense(128,64)
        self.fc4=MyDense(64,32)
        self.fc5=MyDense(32,10)

    def call(self,inputs,training=None):
        x=self.fc1(inputs)
        x=tf.nn.relu(x)
        x=self.fc2(x)
        x=tf.nn.relu(x)
        x=self.fc3(x)
        x=tf.nn.relu(x)
        x=self.fc4(x)
        x=tf.nn.relu(x)
        x=self.fc5(x)
        return x
network=MyModel()

network.compile(optimizer=optimizers.Adam(lr=1e-3),
                loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                metrics=['accuracy']
                )
network.fit(db,epochs=4,validation_data=ds_val,validation_freq=2)
network.evaluate(ds_val)
# network.save('model.h5')
# print('saved')
# del network
# print('load')
# network=tf.keras.models.load_model('model.h5')
# x_val,y_val=preprocess((x_val,y_val))
#
# network.evaluate(x_val,y_val)
network.save_weights('weight.ckpt')
del network
network=Sequential([layers.Dense(256,activation='relu'),
                    layers.Dense(128,activation='relu'),
                    layers.Dense(64,activation='relu'),
                    layers.Dense(32,activation='relu'),
                    layers.Dense(10)])
network.compile(optimizer=optimizers.Adam(lr=1e-3),
                loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                metrics=['accuracy']
                )
network.load_weights('weight.ckpt')
print('load weight')
network.evaluate(ds_val)

# sample=next(iter(ds_val))
# x=sample[0]
# y=sample[1]
# pred=network.predict(x)

# y = tf.argmax(y, axis=1)
# pred = tf.argmax(pred, axis=1)
#
# print(pred)
# print(y)

