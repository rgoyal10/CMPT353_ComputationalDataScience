#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']
print('Row with lowest total precipitation:')
print(np.argmin(totals.sum(axis =1)))
print('Average precipitation in each month:')
print(totals.sum(axis =0)/ counts.sum(axis =0)) 
print('Average precipitation in each city:')
print(totals.sum(axis =1)/ counts.sum(axis =1)) 
print('Quarterly precipitation totals:')
num_cities, num_months, = totals.shape
totals = np.reshape(totals,(4*num_cities, 3))
totals = totals.sum(axis=1)
totals =  np.reshape(totals,(num_cities,4))
print(totals)

