#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import sys
from difflib import get_close_matches

#returns the list of all wrong movie names
def close_match(word ,pattern):
    temp = get_close_matches(word, pattern, n = len(pattern))
    return temp

#returns the list of ratings 
def find_rating(movie_index):
    return other_data['rating'][movie_index] 

#returns the average rating
def find_movie(false_list, df):
    length = len(false_list)
    index = df[df.title.isin(false_list)].index #referred to https://www.geeksforgeeks.org/python-pandas-dataframe-isin/#:~:text=Pandas%20isin()%20method%20is,value%20in%20a%20particular%20column.&text=Parameters%3A,the%20caller%20Series%2FData%20Frame.
    total = 0;
    rating_list = list(map(find_rating,index.values))
    average_rating =0
    if length != 0:
        total = sum(rating_list)
        average_rating = total/length;
    return average_rating
    
filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

data_frame = pd.read_csv(filename1, delimiter='\n' ,names = ['title']) #referred to https://stackoverflow.com/questions/46081317/reading-csv-with-pandas-and-ignoring-commas
other_data = pd.read_csv(filename2)
data_frame['false_list'] = data_frame['title'].apply(close_match, pattern = other_data.title)
data_frame['rating'] = data_frame['false_list'].apply(find_movie, df = other_data)
data_frame.rating = data_frame['rating'].round(2)
data_frame.sort_values('title'); #referred to https://stackoverflow.com/questions/43401903/python-order-dataframe-alphabetically/43401954
data_frame = data_frame.drop(data_frame[(data_frame.rating)== 0].index)
header = ['title','rating'] #referred to https://stackoverflow.com/questions/22019763/pandas-writing-dataframe-columns-to-csv
data_frame.to_csv(filename3, columns = header, index = False)


# In[ ]:




