#This scripts converts muse monitor data to feature matrix 

#Inherited from https://www.kaggle.com/j105sahil/eeg-brainwave-dataset-mental-state

# A modified version of muse-lsl is used https://github.com/xloem/muse-lsl/tree/bleak
# This version does not require external bluetooth module for Mac

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import matplotlib.pyplot as plt

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


# muse_data = pd.read_csv("dataset/real_time_data/debbie_playing_league_part_1.csv")

# muse_data_subset = muse_data[["TimeStamp", 'RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10', 'AUX_RIGHT']]

# muse_data_subset = muse_data_subset.dropna()

# muse_data_subset.index = muse_data_subset.TimeStamp
# muse_data_subset.index = pd.to_datetime(muse_data_subset.index)

# muse_data_subset = muse_data_subset[["TimeStamp", 'RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10', 'AUX_RIGHT']]

# muse_data_subset = muse_data_subset.resample("4ms", how="mean", fill_method='ffill')

# muse_data_subset.columns = ["TP9", "AF7", "AF8", "TP10", "Right AUX"]

# muse_data_subset["timestamps"] = pd.to_datetime(muse_data_subset.index, unit='s')

# muse_data_subset["timestamps"] = pd.to_datetime(muse_data_subset["timestamps"], unit='s').apply(lambda x: x.timestamp())

# muse_data_subset = muse_data_subset[["timestamps", "TP9", "AF7", "AF8", "TP10", "Right AUX"]]

# muse_data_subset.to_csv("dataset/testing_data/muse_data_subset-concentrating-1.csv", index=False)


# muse_data_subset.to_csv("dataset/testing_data/muse_data_subset-concentrating-1.csv", index=False)


from EEG_generate_training_matrix import gen_training_matrix

data_directory_path = "dataset/testing_data_main/"
preprocessed_data_file_name = "out_testing_main.csv"

gen_training_matrix(data_directory_path, preprocessed_data_file_name, cols_to_ignore = -1)

