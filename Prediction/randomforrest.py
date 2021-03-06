# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 07:18:36 2019

"""

import pandas as pd
import numpy as np
import seaborn as sns
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import cv2
from sklearn.cluster import KMeans
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn.preprocessing import LabelEncoder
import sklearn.metrics as metrics
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import math
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 

crime_data=pd.read_csv("Chicago_Crimes_2012_to_2017.csv")
crime_data.Date=pd.to_datetime(crime_data.Date,format='%m/%d/%Y %I:%M:%S %p')
crime_data.index=pd.DatetimeIndex(crime_data.Date)
crime_data['time_hour']=crime_data['Date'].apply(lambda x:x.hour)
crime_data['month']=crime_data['Date'].apply(lambda x:x.month)
#crime_data['year']=crime_data['Date'].apply(lambda x:x.year)
crime_data = crime_data[crime_data['Primary Type']=='HOMICIDE']
crime_data = crime_data.dropna()
crime_data.isnull().sum().sum()
#d = {'True': True, 'False': False}
#crime_data['Arrest'].map(d)
keep_cols = ['Arrest','Domestic','District','Location Description','X Coordinate','Y Coordinate','time_hour','month']
crime_data = crime_data[keep_cols].reset_index()
X=crime_data.drop('Arrest',axis=1)
features = list(X.columns)
y = crime_data.iloc[:,1]
labelencoder = LabelEncoder()
#X['Primary Type']=X['Primary Type'].astype("category").cat.codes
X['Location Description']=X['Location Description'].astype("category").cat.codes
X['Domestic']=X['Domestic'].astype("category").cat.codes
labelencoder.fit_transform(y)
scaler = preprocessing.MinMaxScaler()
X[['X Coordinate', 'Y Coordinate','Location Description','District','time_hour','month']] = scaler.fit_transform(X[['X Coordinate', 'Y Coordinate','Location Description','District','time_hour','month']])
X=X.iloc[:,1:]

#X1=[False,]

# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(X, y, test_size = 0.25, random_state = 42)

rf = RandomForestClassifier(n_estimators = 1000, max_depth=3, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);
# For large values of C, the optimization will choose a smaller-margin hyperplane if that hyperplane does a better job of getting all the training points classified correctly.
predictions = rf.predict(test_features)
# Calculate the absolute errors
results=confusion_matrix(test_labels, predictions)
print(results)
print('Accuracy Score :',accuracy_score(test_labels, predictions)) 
print('Report : ')
print(classification_report(test_labels, predictions))
