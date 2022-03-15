import math
import pandas as pd
import streamlit as st
import numpy as np
from Ant import Ant

class AntSystem:
    edgeWeights = []
    pher = []
    numVerts = 0
    ants = []
    tours = []
    nIter = 0

    def __init__ (self, data, nIter):
        self.edgeWeights.clear()
        self.ants.clear()
        self.loadFile(data)
        self.nIter = nIter
        self.tours.clear()
        pher = np.ones([self.numVerts, self.numVerts])
        np.negative(pher)
        for i in range(nIter):
            self.ants.append(Ant(self.edgeWeights, pher, self.numVerts))

    def loadFile(self, data):
        self.calcDistances(data)

    def calcDistances(self, data):
        dataList = data.values.tolist()
        self.numVerts = len(dataList)
        for i in range(len(dataList)):
            weights  =[]
            for j in range(len(dataList)):
                x0 = dataList[i][1]
                y0 = dataList[i][2]

                x1 = dataList[j][1]
                y1 = dataList[j][2]

                dist = (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)
                dist = math.sqrt(dist)
                weights.append(math.ceil(dist))
            self.edgeWeights.append(weights)

    def doTours(self):
        for i in range(self.nIter):
            for ant in self.ants:
                ant.constructTour()
                self.tours.append(ant.currTour)
        