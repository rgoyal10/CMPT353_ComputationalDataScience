#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
import datetime as dt
from pykalman import KalmanFilter

def convert_date(temp):
    dt_object =  dt.datetime.strptime(temp,'%Y-%m-%d %H:%M:%S.%f')
    return dt_object

filename = sys.argv[1]
# filename = 'sysinfo.csv'
cpu_data = pd.read_csv(filename)

cpu_data.timestamp = cpu_data['timestamp'].apply(convert_date)

plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)


#LOESS Smoothing
loess_smoothed = lowess(cpu_data['temperature'],cpu_data['timestamp'], frac =0.006)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')

#Kalman Smoothing
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]

initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([2, 2, 0.7, 45]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.2, 0.1, 0.1, 0.1]) ** 2 # TODO: shouldn't be zero
transition = [[0.97,0.5,0.2,-0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]] # TODO: shouldn't (all) be zero

kf = KalmanFilter(
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition
)
kalman_smoothed, state_cov = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['Actual','LOESS','KALMAN'])
plt.ylabel('Temperature')
plt.xlabel('Timestamp')


# plt.show() # maybe easier for testing
plt.savefig('cpu.svg') # for final submission

