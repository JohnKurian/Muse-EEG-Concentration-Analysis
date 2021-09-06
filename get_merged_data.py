#open all zips and rename the csvs
import os
import zipfile

print("merging..")
for filename in os.listdir("high_frequency_datasets"):
    
    zipdata = zipfile.ZipFile('high_frequency_datasets/'+filename)
    zipinfos = zipdata.infolist()
 
    for zipinfo in zipinfos:
        zipinfo.filename = 'high_frequency_datasets_csv/' + filename.split(".")[0] + ".csv"
        zipdata.extract(zipinfo)

#merge all csvs into one 
dfs = []

for filename in os.listdir("high_frequency_datasets_csv"):
    df = pd.read_csv("high_frequency_datasets_csv/"+filename)
    df['username'] = [filename.split("_")[0]]*len(df)
    df['activity'] = [filename.split("_")[1]]*len(df)
    df['id'] = [filename.split("_")[4].split(".")[0]]*len(df)
    dfs.append(df)
    
merged = pd.concat(dfs, axis=0)

merged.to_csv("high_frequency_data_merged.csv", index=False)
print("done")