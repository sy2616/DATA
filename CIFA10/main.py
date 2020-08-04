import torch
from torchvision import datasets,transforms
from torch.utils.data import DataLoader
from cifa10 import lene5
from torch import nn,optim
#from resnet import Resnet

def main():
    batchsz=128
    cifar_train=datasets.CIFAR10('cifar',True,transform=transforms.Compose([
        transforms.Resize((32,32)),
        transforms.ToTensor()
    ]),download=True)
    cifar_train=DataLoader(cifar_train,batch_size=batchsz,shuffle=True)
    cifar_test = datasets.CIFAR10('cifar', False, transform=transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor()
    ]), download = True)
    cifar_test =DataLoader(cifar_test, batch_size=batchsz, shuffle=True)

    x,label=iter(cifar_train).next()
    print('x',x.shape,'label',label.shape)
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model=lene5().to(device)
    print(model)
    criteon=nn.CrossEntropyLoss().to(device)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    for epoch in range(1000):
        model.train()
        for batchidx,(x,label) in enumerate(cifar_train):
            x,label=x.to(device),label.to(device)
            logits=model(x)
            loss=criteon(logits,label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(epoch,'loss:',loss.item())

        model.eval()
        with torch.no_grad():
            totol_corret=0
            totol_num=0
            for x,label in cifar_test:
                x,label=x.to(device),label.to(device)
                logits=model(x)
                pred=logits.argmax(dim=1)
                totol_corret+=torch.eq(pred,label).float().sum().item()
                totol_num+=x.size(0)

            acc=totol_corret/totol_num
            print(epoch,'score:',acc)
if __name__=='__main__':
    main()


