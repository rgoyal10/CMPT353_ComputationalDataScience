#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

# filename1 = 'pagecounts-20190509-120000.txt'
# filename2 = 'pagecounts-20190509-130000.txt'

views_dist = pd.read_csv(filename1, sep=' ', header = None, index_col=1, names=['lang','page','views1','bytes'])
hourly_views_dist = pd.read_csv(filename2, sep=' ', header = None, index_col=1, names=['lang','page','views2','bytes'])

#plot1

views_dist_sorted = views_dist.sort_values(by='views1', ascending = False)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(views_dist_sorted['views1'].values)
plt.title('Distributuion of Views')
plt.xlabel('Number of views')
plt.ylabel('pages')


#plot2
merged = pd.concat([views_dist['views1'],hourly_views_dist['views2']],axis =1)
plt.subplot(1, 2, 2)
plt.xscale('log')
plt.yscale('log')
plt.plot(merged['views1'].values,merged['views2'].values,'b.')
plt.title('Hourly views')
plt.xlabel('views1')
plt.ylabel('views2')

plt.savefig('wikipedia.png')



