import visdom
import torch as t
# 新建一个连接客户端
#默认端口为8097，host是‘localhost'
vis = visdom.Visdom()

x = t.arange(1, 30, 0.01)
y = t.sin(x)
vis.line(X=x, Y=y, win='sinx', opts={'title': 'y=sin(x)'})