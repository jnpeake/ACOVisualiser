import glob
import os
import pandas as pd

def getFileNames():
    tspFiles = []
    for file in glob.glob("Instances/*.tsp"):
        tspFiles.append(os.path.basename(file))
    tspFiles.sort()
    return tspFiles

def open_tsp (filename):
    tsp_file = open("Instances/" + filename, 'r')
    data_raw = tsp_file.readlines()
    tsp_file.close()
    data = []
    for line in data_raw:
        if line != "\n": 
            if line.strip()[0].isdigit():
                data.append(line)
    return data

def convert_data(data):
    df = pd.DataFrame(data, columns = ["val"])
    df2 = df["val"].str.split(n = 2, expand = True)
    df["Index"] = df2[0]
    df["X"] = df2[1]
    df["Y"] = df2[2]
    df.drop(columns = "val", inplace = True)
    df[["X", "Y"]] = df[["X", "Y"]].astype(float)
    return df