import tensorflow as tf
from tensorflow.keras import datasets,layers,optimizers,Sequential,metrics
import os
import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
def preprocess(x,y):
    x=tf.cast(x,dtype=tf.float32)/255
    y=tf.cast(y,dtype=tf.int32)
    return x,y

def plot_to_image(figure):
    pass

(x,y),(x_test,y_test)=datasets.mnist.load_data()
print(x.shape,y.shape)
batchsz=128

db=tf.data.Dataset.from_tensor_slices((x,y))
db=db.map(preprocess).shuffle(60000).batch(batchsz).repeat(10)
db_test=tf.data.Dataset.from_tensor_slices((x_test,y_test))
db_test=db_test.map(preprocess).batch(batchsz)

db_iter=iter(db)
sample=next(db_iter)
print('batch:',sample[0].shape,sample[1].shape)

model=Sequential([
    layers.Dense(256,activation=tf.nn.relu),
    layers.Dense(128,activation=tf.nn.relu),
    layers.Dense(64,activation=tf.nn.relu),
    layers.Dense(32,activation=tf.nn.relu),
    layers.Dense(10)
])
model.build(input_shape=[None,28*28])
model.summary()
optimizer=optimizers.Adam(lr=1e-3)
acc_meter=metrics.Accuracy()
loss_meter=metrics.Mean()

current_time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
log_dir='logs/'+current_time
summary_writer=tf.summary.create_file_writer(log_dir)

sample_img=next(iter(db))[0]
sample_img=sample_img[0]
sample_img=tf.reshape(sample_img,[1,28,28,1])

with summary_writer.as_default():
    tf.summary.image('training sample:',sample_img,step=0)


def main():

    for step,(x,y) in enumerate(db):
        x=tf.reshape(x,[-1,28*28])
        with tf.GradientTape() as tape:
            logist=model(x)
            y_onehot=tf.one_hot(y,depth=10)
            loss_MSE=tf.reduce_mean(tf.losses.MSE(y_onehot,logist))
            loss_ce=tf.losses.categorical_crossentropy(y_onehot,logist,from_logits=True)
            loss_ce=tf.reduce_mean(loss_ce)
            a=loss_meter.update_state(loss_ce)
        grads=tape.gradient(loss_ce,model.trainable_variables)
        optimizer.apply_gradients(zip(grads,model.trainable_variables))

        if step%100==0:
            print(step,'loss_ce:',loss_meter.result().numpy(),'loss_MSE:',float(loss_MSE))
            # loss_meter.reset_states()
            # with summary_writer.as_default():
            #     tf.summary.scalar('train-loss',float(a),step=step)
        if step%500==0:

            total_corret=0
            total_num=0
            acc_meter.reset_states()
            for step,(x,y) in enumerate(db_test):
                x=tf.reshape(x,[-1,28*28])
                logists=model(x)
                prob=tf.nn.softmax(logists,axis=1)
                pred=tf.argmax(prob,axis=1)
                pred=tf.cast(pred,dtype=tf.int32)
                corret=tf.equal(pred,y)
                corret=tf.reduce_sum(tf.cast(corret,dtype=tf.int32))
                total_corret+=int(corret)
                total_num+=x.shape[0]
                acc = total_corret / total_num
                acc_meter.update_state(y,pred)
            print(step,'acc:',acc,acc_meter.result().numpy())
        # acc=total_corret/total_num
        # print('epoch:',epoch,'acc:',acc)
        # with summary_writer.as_default():
        #     tf.summary.scalar('acc',float(acc),step=epoch)

if __name__ == '__main__':
    main()