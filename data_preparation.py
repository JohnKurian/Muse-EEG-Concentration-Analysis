#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import shutil
import os
import zipfile


try: 
    shutil.rmtree("high_frequency_datasets_csv/")
    print("deleted high_frequency_datasets_csv/")
except FileNotFoundError:
    print("folder high_frequency_datasets_csv/ does not exist")

print("creating high_frequency_datasets_csv/")
os.mkdir("high_frequency_datasets_csv/")


# In[ ]:


#open all zips and rename the csvs

for filename in os.listdir("high_frequency_datasets"):
    if (filename == ".DS_Store"):
        continue
    print("filename:", filename)

    zipdata = zipfile.ZipFile('high_frequency_datasets/'+filename)
    zipinfos = zipdata.infolist()
 
    for zipinfo in zipinfos:
        filename = filename.split(".")[0]
        filename = filename.replace("eyesopenrelaxed", "relaxedeyesopen")
        zipinfo.filename = 'high_frequency_datasets_csv/' + filename + ".csv"
        zipdata.extract(zipinfo)


# In[ ]:


#merge all csvs into one 
import pandas as pd

dfs = []


for filename in os.listdir("high_frequency_datasets_csv"):
    df = pd.read_csv("high_frequency_datasets_csv/"+filename)
    df['username'] = [filename.split("_")[0]]*len(df)
    df['activity'] = [filename.split("_")[1]]*len(df)
    df['id'] = [filename.split("museMonitor_")[1].split("_")[1].split(".")[0]]*len(df)
    dfs.append(df)
    


# In[ ]:


df = pd.concat(dfs, axis=0)


# In[ ]:


df.loc[df.activity == "eyesopenrelaxed", "activity"] = "relaxedeyesopen"


# In[ ]:


#choose only relaxedeyesopen and lostinmigration activities
df = df[(df.activity == "relaxedeyesopen") | (df.activity == "lostinmigration")]


# In[ ]:

try: 
    shutil.rmtree("dataset/original_data_main/")
    print("deleted dataset/original_data_main/")
except FileNotFoundError:
    print("folder dataset/original_data_main/ does not exist")

print("creating dataset/original_data_main/")
os.mkdir("dataset/original_data_main/")


# In[ ]:


sampled_dfs = []

for activity_id in list(df.id.unique()):
    print("id:", activity_id)
    # print(len(muse_data_subset[muse_data_subset.index < (muse_data_subset.index[0] + pd.Timedelta("1 min"))]))

    
    muse_data_subset = df[df['id'] == activity_id]
    
    muse_data_subset_id = muse_data_subset['id']
    muse_data_subset_activity = muse_data_subset['activity'].iloc[0]
    
    muse_data_subset.index = muse_data_subset.TimeStamp
    muse_data_subset.index = pd.to_datetime(muse_data_subset.index)
    
    muse_data_subset = muse_data_subset[["TimeStamp", 'RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10', 'AUX_RIGHT']]

    # muse_data_subset = muse_data_subset.resample("4ms", how="mean", fill_method='bfill')


    muse_data_subset = muse_data_subset.resample("4ms").mean().bfill()
    
    muse_data_subset.columns = ["TP9", "AF7", "AF8", "TP10", "Right AUX"]
    
    muse_data_subset["timestamps"] = pd.to_datetime(muse_data_subset.index, unit='s')

    muse_data_subset["timestamps"] = pd.to_datetime(muse_data_subset["timestamps"], unit='s').apply(lambda x: x.timestamp())

    muse_data_subset = muse_data_subset[["timestamps", "TP9", "AF7", "AF8", "TP10", "Right AUX"]]
    
    #7500  = 30 seconds
    #15000 = 30 seconds
#     if len(muse_data_subset[muse_data_subset.index < (muse_data_subset.index[0] + pd.Timedelta("1 min"))]) < 7500:
#         continue
    
    muse_data_subset.to_csv(f"dataset/original_data_main/muse_data_subset-{muse_data_subset_activity}-{activity_id}.csv", index=False)

print('data preparation done.')
    

