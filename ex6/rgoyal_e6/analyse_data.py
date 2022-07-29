#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib




data = pd.read_csv('data.csv')

# print(stats.normaltest(data['partition_sort']).pvalue)
# plt.plot(data['partition_sort'],'b.')
# plt.show()
anova = stats.f_oneway(data['qs1'],data['qs2'],data['qs3'],data['qs4'],data['qs5'],data['merge1'],data['partition_sort'])
print(anova)
print(anova.pvalue)

x_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(
    x_melt['value'], x_melt['variable'],
    alpha=0.05)

print(posthoc)

print('ranking of sorting implemenation by speed - partition_sort>qs1>qs3>qs2>qs4>qs5>merge1')








# In[ ]:




