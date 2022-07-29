#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import xml.etree.ElementTree as et
import pandas as pd
import math
from math import radians, cos, sin, asin, sqrt
import numpy as np
from pykalman import KalmanFilter



def read_gpx(filename):
#Read the XML
    parsed_xml = et.parse(filename) #got reference from https://stackoverflow.com/questions/63128936/is-there-any-way-to-extract-elements-from-xml-file-and-convert-it-into-pandas-da
    data_frame_col = ['lat','lon']
    data_frame = pd.DataFrame(columns = data_frame_col)

    for node in parsed_xml.iter('{http://www.topografix.com/GPX/1/0}trkpt'):
        lat = node.attrib.get('lat')
        lon = node.attrib.get('lon')
        data_frame = data_frame.append(pd.Series([lat,lon],index=data_frame_col),ignore_index = True)
    return data_frame
    
# Calculate distances

# got reference from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine_formula(temp):
    R = 6371 #form km
    lon1 = float(temp.lon)
    lat1 = float(temp.lat)
    lon2 = float(temp.new_lon)
    lat2 = float(temp.new_lat)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    d = R * c
    return d*1000 #distance in meters 

def distance(data):
    data['lat'] = data['lat'].astype(float)
    data['lon'] = data['lon'].astype(float)
    data['new_lat'] = data['lat'].shift(-1)
    data['new_lon'] = data['lon'].shift(-1)
    data['distance'] = data.apply(haversine_formula, axis =1)
    total_distance = data['distance']
    x = total_distance.sum(axis =0)
    x = round(x,6)
    return x

def smooth(data):
    kalman_data = data[['lat','lon']]
    converting_factor = 10**5;
    
    kalman_data = kalman_data.mul(converting_factor)
    
    initial_state = kalman_data.iloc[0]
    observation_covariance = np.diag([20, 20]) ** 2
    transition_covariance = np.diag([10, 10]) ** 2 
    transition = [[1,0], [0,1]]
    
    kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition
    )
    kalman_smoothed, state_cov = kf.smooth(kalman_data)
    data_frame = pd.DataFrame(kalman_smoothed, columns=['lat','lon'])
    data_frame = data_frame.div(converting_factor)
    return data_frame
    
#ouput code given by prof
def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def main():
    filename= sys.argv[1]
#     filename = 'walk1.gpx'
    points = read_gpx(filename)
    print('Unfiltered distance: %0.2f' % (distance(points)))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points)))
    
    output_gpx(smoothed_points, 'out.gpx')

if __name__ == '__main__':
    main()


