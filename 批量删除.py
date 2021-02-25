import os
dd=r'D:'
for root,dirs,files in os.walk(dd):
    print(root)
    print(dirs)
    print(files)