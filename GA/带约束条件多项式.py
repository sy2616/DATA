import numpy as np
import geatpy as ea
import time
class MyProblem(ea.Problem):
    def __init__(self):
        name='MyProblem'
        M=1
        maxormins=[-1]
        Dim=3
        varTypes=[0]*Dim
        lb=[0,0,0]
        ub=[1,1,2]
        lbin=[1,1,0]
        ubin=[1,1,0]
        ea.Problem.__init__(self,name,M,maxormins,Dim,varTypes,lb,ub,lbin,ubin)
    def aimFunc(self,pop):
        Vars=pop.Phen
        x1=Vars[:,[0]]
        x2=Vars[:,[1]]
        x3=Vars[:,[2]]
        pop.ObjV=4*x1+2*x2+x3
        pop.CV=np.hstack([2*x1+x2-1,x1+2*x3-2,np.abs(x1+x2+x3-1)])

problem=MyProblem()
Encoding='RI'
NIND=50
Field=ea.crtfld(Encoding,problem.varTypes,problem.ranges,problem.borders)
population=ea.Population(Encoding,Field,NIND)
myAlogorithm=ea.soea_DE_best_1_L_templet(problem,population)
myAlogorithm.MAXGEN=1000
myAlogorithm.mutOper.F=0.5
myAlogorithm.recOper.XOVR=0.5
myAlogorithm.drawing=1
[population,obj_trace,var_trace]=myAlogorithm.run()
best_gen=np.argmax(obj_trace[:,1])
best_ObjV=obj_trace[best_gen,1]
print('最优的目标函数值:%s'%(best_ObjV))
print('最优的决策变量:')
for i in range(var_trace.shape[1]):
    print(var_trace[best_gen,i])
print('有效进化代数:%s'%(obj_trace.shape[0]))
print('最优的一代是第%s代'%(best_gen+1))
print('评价次数:%s'%(myAlogorithm.evalsNum))
print('时间已过%s秒'%(myAlogorithm.passTime))