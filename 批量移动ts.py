import os
input_path=r'C:\Users\Jack\Downloads'
for root,dirs,files in os.walk(input_path):
    #print(root,dirs,files)
    for file in files:
        endname=os.path.splitext(file)[1]
        if endname=='.ts':
            fromdir=os.path.join(root,file)
            newdir=os.path.join(r'C:\Users\Jack\Downloads\HUB',file)
            os.rename(fromdir,newdir)
            print('%s movie success'%file)
