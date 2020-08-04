import tensorflow as tf
from tensorflow.keras import layers,Sequential
from tensorflow import keras
# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# tf.random.set_seed(22222)
#
# def preprocess(x,y):
#     x=tf.cast(x,dtype=tf.float32)/255
#     y=tf.cast(y,dtype=tf.int32)
#     return x,y
# (x,y),(x_test,y_test)=datasets.cifar100.load_data()
# bachsz=64
# train_db=tf.data.Dataset.from_tensor_slices((x,y))
# train_db=train_db.map(preprocess).shuffle(10000).batch(bachsz)
# test_db=tf.data.Dataset.from_tensor_slices((x_test,y_test))
# test_db=test_db.map(preprocess).batch(bachsz)
#
# sample=next(iter(train_db))
# print('sample:',sample[0].shape,sample[1].shape)

class BasicBlock(layers.Layer):
    def __init__(self,filter_num,stride=1):
        super(BasicBlock,self).__init__()
        self.cov1=layers.Conv2D(filter_num,(3,3),strides=stride,padding='same')
        self.bn1=layers.BatchNormalization()
        self.relu=layers.Activation('relu')

        self.cov2=layers.Conv2D(filter_num,(3,3),strides=1,padding='same')
        self.bn2=layers.BatchNormalization()

        if stride!=1:
            self.downsample=Sequential()
            self.downsample.add(layers.Conv2D(filter_num,(1,1),strides=stride))
        else:
            self.downsample=lambda x:x


    def call(self,inputs,training=None):
        out=self.cov1(inputs)
        out=self.bn1(out)
        out=self.relu(out)
        out=self.cov2(out)
        out=self.bn2(out)

        identity=self.downsample(inputs)
        output=layers.add([out,identity])
        output=tf.nn.relu(output)

        return output

class ResNet(keras.Model):
    def __init__(self,layer_dims,num_classes=100):
        super(ResNet,self).__init__()
        self.stem=Sequential([layers.Conv2D(64,(3,3),strides=(1,1)),
                              layers.BatchNormalization(),
                              layers.Activation('relu'),
                              layers.MaxPool2D(pool_size=(2,2),strides=(1,1),padding='same')
                              ])
        self.layer1=self.build_resblock(64,layer_dims[0])
        self.layer2=self.build_resblock(128,layer_dims[1],stride=2)
        self.layer3=self.build_resblock(256,layer_dims[2],stride=2)
        self.layer4=self.build_resblock(512,layer_dims[3],stride=2)

        self.avgpool=layers.GlobalAveragePooling2D()
        self.fc=layers.Dense(num_classes)
    def call(self,inputs,training=None):
        x=self.stem(inputs)
        x=self.layer1(x)
        x=self.layer2(x)
        x=self.layer3(x)
        x=self.layer4(x)

        x=self.avgpool(x)
        x=self.fc(x)
        return x

    def build_resblock(self,filter_num,blocks,stride=1):
        res_block=Sequential()
        res_block.add(BasicBlock(filter_num,stride))

        for _ in range(1,blocks):
            res_block.add(BasicBlock(filter_num,stride=1))

        return res_block
def resnet18():
    return ResNet([2,2,2,2])

def resnet34():
    return ResNet([3,4,6,3])
#
# def main():
#     model=resnet18()
#     # model.build(input_shape=(None,32,32,3))
#     optimizer=optimizers.Adam(lr=1e-3)
#
#     for epoch in range(50):
#         for step,(x,y) in enumerate(train_db):
#             with tf.GradientTape() as tape:
#                 logits=model(x)
#                 y_onehot=tf.one_hot(y,depth=100)
#                 loss=tf.losses.categorical_crossentropy(y_onehot,logits,from_logits=True)
#                 loss=tf.reduce_mean(loss)
#             grads=tape.gradient(loss,)
#             optimizer.apply_gradients(zip(grads,model.trained_variables))
#
#             if step%100==0:
#                 print(epoch,step,'loss:',loss)
#
# if __name__ == '__main__':
#     main()
#
