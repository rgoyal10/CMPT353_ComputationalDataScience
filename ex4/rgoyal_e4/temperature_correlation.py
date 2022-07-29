#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import gzip
from math import pi

# referred to https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def haversine_formula(city, stations):
    R = 6371 #form km
    p = pi/180
    lat1 = city.loc['latitude']
    lon1 = city.loc['longitude']
    lon2 = stations['longitude'].values
    lat2 = stations['latitude'].values
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    c = 2*np.arcsin(np.sqrt(a))
    d = R * c
    return d #distance in kilometers 

def distance(stations,city):
    list_distance = (haversine_formula(city, stations))
    return list_distance
   

def best_tmax(city, stations):
    temp = distance(stations, city)
    distance_series = pd.Series(temp)
    indexes = distance_series.idxmin()
    required_station = stations.loc[indexes]
    t_max = required_station.avg_tmax
    return t_max

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

# filename1 = 'stations.json.gz'
# filename2 = 'city_data.csv'
# filename3 = 'output.svg'

stations = pd.read_json(filename1 ,lines=True)
city_data = pd.read_csv(filename2)
stations.avg_tmax = stations['avg_tmax']/10;
city_data = city_data.drop(city_data[pd.isnull(city_data.population)].index)
city_data = city_data.drop(city_data[pd.isnull(city_data.area)].index)
city_data.area = city_data['area'] / 1000000 
city_data = city_data.drop(city_data[city_data.area > 10000].index)
city_data['population_density'] = city_data['population']/city_data['area']
city_data['Avg_Tmax'] = city_data.apply(best_tmax, stations = stations, axis=1)

# plot
plt.plot(city_data['Avg_Tmax'].values,city_data['population_density'].values,'b.')
plt.ylabel('Population Density (people/km\u00b2)')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.title('Temperature vs Population Density')
# plt.show()
plt.savefig(filename3) 

