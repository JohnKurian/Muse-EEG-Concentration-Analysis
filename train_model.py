#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Inherited from https://www.kaggle.com/j105sahil/eeg-brainwave-dataset-mental-state

import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:

import shutil

import warnings
warnings.filterwarnings('ignore')

# import os
# os.listdir('../input')


# In[ ]:


pd.set_option('display.float_format', lambda x: '%.3f' % x)


# In[ ]:


# #Script to convert from mean centered to 0 - 1600 uv
# data = res[1:]
# data = 0.48828125 * (np.array(data))
# 1680 * ((data) - data.min()) / (data.max() - data.min())


# In[ ]:


try: 
    shutil.rmtree("dataset/transformed_data_main/")
    print("deleted dataset/transformed_data_main/")
except FileNotFoundError:
    print("folder dataset/transformed_data_main/ does not exist")
    
print("creating dataset/transformed_data_main/")
os.mkdir("dataset/transformed_data_main/")


# In[ ]:


#Inherited from https://github.com/jordan-bird/eeg-feature-generation

# data transformation from 0 - 1600 to mean centering around 0
# https://github.com/alexandrebarachant/muse-lsl/issues/11


for x in os.listdir("dataset/original_data_main"):

    # Ignore non-CSV files
    if not x.lower().endswith('.csv'):
        continue
    print("processing ", x)
    df = pd.read_csv("dataset/original_data_main/"+x)
    for electrode in ["TP9", "TP10", "AF7", "AF8", "Right AUX"]:    
        data = df[electrode]
        data = 0.48828125 * (np.array(data))
        data = 1680 * ((data) - data.min()) / (data.max() - data.min())
        df[electrode] = data
    df.to_csv("dataset/transformed_data_main/"+x, index=False)


# In[ ]:


from EEG_generate_training_matrix import gen_training_matrix

data_directory_path = "dataset/transformed_data_main/"
preprocessed_data_file_name = "out_main.csv"

print("generating training matrix...")
gen_training_matrix(data_directory_path, preprocessed_data_file_name, cols_to_ignore = -1)


# In[ ]:


nRowsRead = None # specify 'None' if want to read whole file
# mental-state.csv has 2360 rows in reality, but we are only loading/previewing the first 1000 rows
df = pd.read_csv(preprocessed_data_file_name, delimiter=',', nrows = nRowsRead)
df.dataframeName = preprocessed_data_file_name
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns')


# In[ ]:


df = df.applymap(complex)
df = df.astype(float)


# In[ ]:


from sklearn import ensemble

model = ensemble.RandomForestClassifier(n_estimators=100,max_depth=20)


# In[ ]:


msk = np.random.rand(len(df)) < 0.7

train = df[msk]
test = df[~msk]

y_train = train["Label"]
y_test = test["Label"]

X_train = train.drop("Label", axis=1)
X_test = test.drop("Label", axis=1)

print("training model...")
model.fit(X_train, y_train)


# In[ ]:


y_pred = model.predict(X_test)


# In[ ]:


from sklearn import metrics

count_misclassified = (y_test != y_pred).sum()
print('Misclassified samples: {}'.format(count_misclassified))
accuracy = metrics.accuracy_score(y_test, y_pred)
print('Accuracy: {:.2f}'.format(accuracy))


# In[ ]:


from sklearn.metrics import confusion_matrix
y_true = y_test
matrix = confusion_matrix(y_true, y_pred)
matrix.diagonal()/matrix.sum(axis=1)


# In[ ]:


classwise_accuracy = matrix.diagonal()/matrix.sum(axis=1)


# In[ ]:


activities = ['relaxedeyesopen', 'lostinmigration']

for index, activity in enumerate(activities): 
    print(activity, classwise_accuracy[index])


# In[ ]:


from joblib import dump, load
dump(model, 'model.joblib') 
print("model training done.")
