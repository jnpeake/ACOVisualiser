import glob
import os

def getFileNames():
    tspFiles = []
    for file in glob.glob("Instances/*.tsp"):
        tspFiles.append(os.path.basename(file))
    return tspFiles