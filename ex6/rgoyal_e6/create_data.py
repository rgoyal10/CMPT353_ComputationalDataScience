#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import numpy as np
import pandas as pd
from implementations import all_implementations

data = []
for i in range (1,151):
    random_array = np.random.randint(10000, size = 3000)
    array = []
    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        total_time = en-st
        lst = [total_time]
        array = np.append(array,lst, axis=0)
    data.append(array)
data =  pd.DataFrame(data,columns = ['qs1','qs2','qs3','qs4','qs5','merge1','partition_sort'])

data.to_csv('data.csv', index=False)

