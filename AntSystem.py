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
    nAnts = 0
    bestTourIndex = -1
    bestTourDist = 1000000000
    bestTour = []
    rho = 0.98

    def __init__ (self, data, nAnts, alpha, beta, rho):
        self.edgeWeights.clear()
        self.ants.clear()
        self.loadFile(data)
        self.nAnts = nAnts
        self.tours.clear()
        self.pher = np.full((self.numVerts, self.numVerts), float(0.5))
        self.rho = rho
        for i in range(nAnts):
            self.ants.append(Ant(self.edgeWeights,self.pher,self.numVerts, alpha, beta))

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

    def doTours(self, nIter):
        for i in range(nIter):
            for ant in self.ants:
                ant.constructTour()
                self.tours.append(ant.currTour)
            self.getBestTour()
            self.bestTour = self.tours[self.bestTourIndex]
            print(i)
            print(self.pher)
            self.updatePher()
            self.pherDecay()
            print(self.pher)

            self.tours.clear()
        

    def getBestTour(self):
        for i, tour in enumerate(self.tours):
            dist = self.getTourDist(tour)
            if dist < self.bestTourDist:
                self.bestTourDist = dist
                self.bestTourIndex = i
                self.bestTourDist = self.bestTourDist

    def getTourDist(self, tour):
        tourDist = 0
        for i in range(len(tour)-1):
            currVert = tour[i]
            nextVert = tour[i+1]
            tourDist += self.edgeWeights[currVert][nextVert]
        tourDist+= self.edgeWeights[tour[-1]][tour[0]]
        return tourDist

    def updatePher(self):
        tour = self.bestTour
        newPher = 1/self.bestTourDist
        for i in range (len(tour)-1):
            currVert = tour[i]
            nextVert = tour[i+1]
            self.pher[currVert][nextVert] += newPher

    def pherDecay(self):
        for i,row in enumerate(self.pher):
            for j,entry in enumerate(row):
                self.pher[i][j] *= self.rho

        