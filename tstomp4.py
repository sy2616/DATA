import os
dd=r'C:\Users\Jack\Downloads\DownloadsHUB'
for i in os.listdir(dd):
    print(os.path.join(dd,i))
    d=os.path.splitext(i)[0]
    cmd='ffmpeg -i "{0}" -c copy "{1}.mp4"'.format(os.path.join(dd,i),os.path.join(dd,d))
    os.popen(cmd)
    break