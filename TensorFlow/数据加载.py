import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def himmelblau(x):
    return (x[0]**2+x[1]-11)**2+(x[0]+x[1]**2-7)**2

x=np.arange(-6,6,0.1)
y=np.arange(-6,6,0.1)
print('x,y range:',x.shape,y.shape)
x,y=np.meshgrid(x,y)
print('x,y maps:',x.shape,y.shape)
z=himmelblau([x,y])
fig=plt.figure('himmelblau')
ax=fig.gca(projection='3d')
ax.plot_surface(x,y,z)
ax.view_init(60,-30)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

x=tf.constant([4.,0.])
for step in range(200):
    with tf.GradientTape() as tape:
        tape.watch([x])
        y=himmelblau(x)
    grads=tape.gradient(y,[x])[0]
    x-=0.01*grads

    if step%20==0:
        print('step {}:x={},f(x)={}'.format(step,x.numpy(),y.numpy()))