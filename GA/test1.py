import geatpy as ea
import numpy as np
import time
def aim(Phen):
    x1=Phen[:,[0]]
    x2=Phen[:,[1]]
    return np.sin(x1+x2)+(x1-x2)**2-1.5*x1+2.5*x2+1
x1=[-1.5,4]
x2=[-3,4]
b1=[1,1]
b2=[1,1]
ranges=np.vstack([x1,x2]).T
borders=np.vstack([b1,b2]).T
varTypess=np.array([0,0])
Encoding='BG'
codes=[1,1]
precisions=[6,6]
scales=[0,0]
FieldD=ea.crtfld(Encoding,varTypess,ranges,borders,precisions,codes,scales)

NIND=20
MAXGEN=100
maxorins=np.array([1])
selectStyle='sus'
recStyle='xovdp'
mutStyle='mutbin'
Lind=int(np.sum(FieldD[0,:]))
pc=0.9
pm=1/Lind
obj_trace=np.zeros((MAXGEN,2))
var_trace=np.zeros((MAXGEN,Lind))
start_time=time.time()
Chrom=ea.crtpc(Encoding,NIND,FieldD)
variable=ea.bs2real(Chrom,FieldD)
ObjV=aim(variable)
best_ind=np.argmin(ObjV)

for gen in range(MAXGEN):
    FitnV=ea.ranking(maxorins*ObjV)
    SelCh=Chrom[ea.selecting(selectStyle,FitnV,NIND-1),:]
    SelCh=ea.recombin(recStyle,SelCh,pc)
    SelCh=ea.mutate(mutStyle,Encoding,SelCh,pm)
    Chrom=np.vstack([Chrom[best_ind,:],SelCh])
    Phen=ea.bs2real(Chrom,FieldD)
    ObjV=aim(Phen)
    best_ind=np.argmin(ObjV)
    obj_trace[gen,0]=np.sum(ObjV)/ObjV.shape[0]
    obj_trace[gen,1]=ObjV[best_ind]
    var_trace[gen,:]=Chrom[best_ind,:]

end_time=time.time()
ea.trcplot(obj_trace,[['种族个体平均目标函数值','种族最优个体目标函数值']])
best_gen=np.argmin(obj_trace[:,[1]])
print('最优解的目标值:',obj_trace[best_gen,1])
variable=ea.bs2real(var_trace[[best_gen],:],FieldD)
print('最优解的决策变量值为:')
for i in range(variable.shape[1]):
    print('x'+str(i)+'=',variable[0,i])
print('用时:',end_time-start_time,'秒')