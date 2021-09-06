#Inherited from https://www.kaggle.com/j105sahil/eeg-brainwave-dataset-mental-state

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

import xgboost as xgb

import warnings
warnings.filterwarnings('ignore')


muse_data = pd.read_csv("dataset/real_time_data/debbie_eyes_open_250hz.csv")

muse_data_subset = muse_data[["TimeStamp", 'RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10', 'AUX_RIGHT']]

muse_data_subset.to_csv("dataset/testing_data/muse_data_subset-concentrating-1.csv", index=False)


from EEG_generate_training_matrix import gen_training_matrix

data_directory_path = "dataset/testing_data/"
preprocessed_data_file_name = "out_testing.csv"

gen_training_matrix(data_directory_path, preprocessed_data_file_name, cols_to_ignore = -1)

