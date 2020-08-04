import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.model_selection import train_test_split

a=pd.read_excel(r'C:\Users\Jack\Downloads\日销量数据.xlsx')
#print(a)
b=a.loc[a['SKU']==2024836]
#print(b)
d=b['日期']
c=b['销量']
plt.plot(d,c)
plt.show()
# c.mean()
# c.std()
def cdf(n):
    return norm(n.mean(),n.std()).cdf((n.min()-n.mean())/n.std())\
           +norm(n.mean(),n.std()).cdf((n.max()-n.mean())/n.std())

print(cdf(c))
