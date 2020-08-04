import tensorflow as tf
from tensorflow.keras import datasets,layers,optimizers,Sequential,metrics,callbacks
from tensorflow import keras
import os,time

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
def preprocess(x,y):
    x=tf.cast(x,dtype=tf.float32)/255
    y=tf.cast(y,dtype=tf.int32)
    return x,y

batchsz=128
(x,y),(x_val,y_val)=datasets.cifar10.load_data()
y=tf.squeeze(y)
y_val=tf.squeeze(y_val)
y=tf.one_hot(y,depth=10)
y_val=tf.one_hot(y_val,depth=10)
print('datasets:',x.shape,y.shape,x.min(),x.max())
tain_db=tf.data.Dataset.from_tensor_slices((x,y))
tain_db=tain_db.map(preprocess).shuffle(10000).batch(batchsz)
test_db=tf.data.Dataset.from_tensor_slices((x_val,y_val))
test_db=test_db.map(preprocess).batch(batchsz)

class MyDense(layers.Layer):
    def __init__(self,inp_dim,oup_dim):
        super(MyDense,self).__init__()
        self.kernel=self.add_weight('w',[inp_dim,oup_dim])
        self.bias=self.add_weight('b',[oup_dim])

    def call(self,inputs,training=None):
        out=inputs@self.kernel+self.bias
        return out

class Mymodel(keras.Model):
    def __init__(self):
        super(Mymodel,self).__init__()
        self.fc1=MyDense(32*32*3,256)
        self.fc2=MyDense(256,128)
        self.fc3=MyDense(128,64)
        self.fc4=MyDense(64,32)
        self.fc5=MyDense(32,10)

    def call(self,inputs,training=None):
        x=tf.reshape(inputs,[-1,32*32*3])
        x=self.fc1(x)
        x=tf.nn.relu(x)
        x=self.fc2(x)
        x=tf.nn.relu(x)
        x=self.fc3(x)
        x=tf.nn.relu(x)
        x=self.fc4(x)
        x=tf.nn.relu(x)
        out=self.fc5(x)
        return out
start_time=time.time()
model=Mymodel()
call_back=callbacks.TensorBoard(log_dir='./model',write_graph=True)
model.compile(optimizer=optimizers.Adam(lr=1e-3),
              loss=tf.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
model.fit(tain_db,epochs=8,validation_data=test_db,validation_freq=1,callbacks=[call_back])
end_time=time.time()
print('cost time:',end_time-start_time)
model.evaluate(test_db)
model.save_weights('weig.ckpt')
del model
print('save model')
model=Mymodel()
model.compile(optimizer=optimizers.Adam(lr=1e-3),
              loss=tf.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
# model.fit(tain_db,epochs=5,validation_data=test_db,validation_freq=1)
model.load_weights('weig.ckpt')
print('load model')
model.evaluate(test_db)



