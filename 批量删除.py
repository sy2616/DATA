import os
dd=r'E:'
# n=0
for root,dirs,files in os.walk(dd):
    # print(root)
    # print(dirs)
    # print(files)
    for file in files:
        if file == '有趣的小视频.mp4':
            os.remove(os.path.join(root,file))
            n+=1
            print('remove successes')
        if os.path.splitext(file)[1]=='.bc!':
            os.remove(os.path.join(root,file))    #删除特定格式文件
            print('remove bc!')
    for dir in dirs:
        nn=os.path.join(root,dir)
        try:
            os.rmdir(nn)     #删除空文件夹
            print('remove %s'%nn)
        except:
            pass

# print('%s are removed'%n)