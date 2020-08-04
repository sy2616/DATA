import torch
from torch import nn
from torch.nn import functional as F

class ResBl(nn.Module):
    def __init__(self,ch_in,ch_out,stride=1):
        super(ResBl,self).__init__()
        self.conv1=nn.Conv2d(ch_in,ch_out,kernel_size=3,stride=stride,padding=1)
        self.bn1=nn.BatchNorm2d(ch_out)
        self.conv2=nn.Conv2d(ch_out,ch_out,kernel_size=3,stride=1,padding=1)
        self.bn2=nn.BatchNorm2d(ch_out)
        self.extra=nn.Sequential()
        if ch_out!=ch_in:
            self.extra=nn.Sequential(
                nn.Conv2d(ch_in,ch_out,kernel_size=1,stride=stride),
                nn.BatchNorm2d(ch_out)
            )

    def forward(self, x):
        out=F.relu(self.bn1(self.conv1(x)))
        out=self.bn2(self.conv2(out))
        out=self.extra(x)+out
        return out

class Resnet(nn.Module):
    def __init__(self):
        super(Resnet,self).__init__()
        self.con1=nn.Sequential(
            nn.Conv2d(3,64,kernel_size=3,stride=3,padding=0),
            nn.BatchNorm2d(64)
        )
        self.blc1=ResBl(64,128,stride=2)
        self.blc2=ResBl(128,256,stride=2)
        self.blc3=ResBl(256,512,stride=2)
        self.blc4=ResBl(512,512,stride=2)
        self.outlayer=nn.Linear(512*1*1,10)

    def forward(self,x):
        x=F.relu(self.con1(x))
        x=self.blc1(x)
        x=self.blc2(x)
        x=self.blc3(x)
        x=self.blc4(x)
        #print(x.shape)
        x=F.adaptive_avg_pool2d(x,[1,1])
        #print(x.shape)
        x=x.view(x.size(0),-1)
        x=self.outlayer(x)
        return x

# def main():
#     blk=ResBl(64,128,stride=4)
#     tmp = torch.randn(2, 64, 32, 32)
#     out=blk(tmp)
#     print('block:',out.shape)
#
#     x=torch.randn(2,3,32,32)
#     model=Resnet()
#     out=model(x)
#     print('resnet:',out.shape)
#
#
# if __name__ == '__main__':
#     main()
