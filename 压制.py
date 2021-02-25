import os
path=r'"C:\Users\Jack\Downloads\HUB\Amateur Japanese Teen with Tight Pussy Gets Fucked - Pornhub.com.ts"'
out=r'D:\1.mp4'
cmd='ffmpeg -i %s -t 60 -c:v libx265 -crf 20 -c:a copy %s'%(path,out)
os.system(cmd)
