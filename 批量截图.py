import os
path=r'D:\[ThZu.Cc]020421_01-10mu-1080p\[ThZu.Cc]020421_01-10mu-1080p.mp4'
out='D:\[ThZu.Cc]020421_01-10mu-1080p\img%03d.jpg'
cmd='ffmpeg -i {0} -vf fps=1/600 {1}'.format(path,out)
os.popen(cmd)