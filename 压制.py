import os
#path=r'"C:\Users\Jack\Downloads\HUB\Amateur Japanese Teen with Tight Pussy Gets Fucked - Pornhub.com.ts"'
#out=r'D:\1.mp4'
#cmd='ffmpeg -i %s -t 60 -c:v libx265 -crf 20 -c:a copy %s'%(path,out)
#os.system(cmd)
path=r'C:\Users\Jack\Downloads'
for root,dirs,files in os.walk(path):
    for file in files:
        print(os.path.abspath(file))
        if os.path.splitext(file)[1] =='.ts':
            oldfile=os.path.join(root,file)
            newfile=os.path.join(path,file)
            os.renames(oldfile,newfile)
            print('{} copy to new file'.format(file))
 
