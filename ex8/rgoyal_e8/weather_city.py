#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler



filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]
# filename1 ='monthly-data-labelled.csv'
# filename2 = 'monthly-data-unlabelled.csv'
# filename3 = 'labels.csv'

labelled_data = pd.read_csv(filename1)
unlabelled_data = pd.read_csv(filename2)
# unlabelled_data
X = labelled_data.drop(['city','year'], axis =1) 
X = X.to_numpy() 
y = labelled_data['city'].values
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

model=  make_pipeline(StandardScaler(),
                     SVC(kernel = 'linear',C=0.1)
                     )
model.fit(X_train,y_train)


#predicting
X_unlabelled = unlabelled_data.drop(['city','year'], axis =1) 
X_unlabelled = X_unlabelled.to_numpy()
prediction = model.predict(X_unlabelled)
pd.Series(prediction).to_csv(filename3, index=False, header=False)
print("validation score = " + str(model.score(X_valid, y_valid)))

# df = pd.DataFrame({'truth': y_valid, 'prediction': model.predict(X_valid)})
# print(df[df['truth'] != df['prediction']])

# In[ ]:




