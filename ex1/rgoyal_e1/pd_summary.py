#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

print('City with lowest total precipitation:');
print(totals.index[np.argmin(totals.sum(axis =1))])

print('Average precipitation in each month:');
print(totals.sum(axis =0)/ counts.sum(axis =0)) 

print('Average precipitation in each city:')
print(totals.sum(axis =1)/ counts.sum(axis =1)) 


# In[ ]:




