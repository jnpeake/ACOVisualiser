import math
import pandas as pd
import streamlit as st
import numpy as np
import RenderManager as rm
import time
from Ant import Ant
import sys
np.set_printoptions(threshold=sys.maxsize)


class AntSystem:
    edgeWeights = []
    pher = []
    numVerts = 0
    ants = []
    tours = []
    nnList = []
    nIter = 0
    nAnts = 0
    numNN = 16
    bestTourIndex = -1
    bestTourDist = 1000000000
    bestTour = []
    rho = 0.98
    greedyLength = 0
    mmasConst = 0
    pherMin = 0
    markerSize = 0
    data = []
    markerColour = ""
    lineColour = ""


    def __init__ (self, data, nAnts, alpha, beta, rho, numNN, rm):
        self.reset()
        self.loadFile(data)
        self.data = data
        self.nAnts = nAnts
        self.rho = rho
        self.numNN = numNN
        self.calcNN()
        self.greedyTour()
        self.renderManager = rm
        self.pher = np.full((self.numVerts, self.numVerts), float(1/(self.greedyLength*(1-rho))))
        for i in range(nAnts):
            self.ants.append(Ant(self.edgeWeights,self.pher,self.numVerts, alpha, beta, self.nnList))
        a = math.exp(math.log(0.05) / self.numVerts)
        self.mmasConst = (1 - a) / ((self.numVerts + 1) * a * 0.5)
    
    def reset(self):
        self.edgeWeights.clear()
        self.pher.clear()
        self.ants.clear()
        self.tours.clear()
        self.bestTour.clear()

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
    
    def calcNN(self):
        print(self.numNN)
        for weightList in self.edgeWeights:
            sortedIndicies = np.argsort(np.array(weightList))
           
            self.nnList.append(sortedIndicies[1:self.numNN-1])

    def doTourGen(self):
        for ant in self.ants:
            ant.constructTour()
            self.tours.append(ant.currTour)
        self.getBestTour()
        self.two_opt()
        self.bestTourDist = self.getTourDist(self.bestTour)
        # print("After LS 2: " +  str(self.bestTourDist))
        self.updatePher()
        self.pherDecay()
        self.tours.clear()

        

    def getBestTour(self):
        for i, tour in enumerate(self.tours):
            dist = self.getTourDist(tour)
            if dist < self.bestTourDist:
                self.bestTour = tour.copy()
                self.bestTourDist = dist
                #print("Original Original: " + str(dist))


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
        pherMax = 1/((1-self.rho) * self.bestTourDist)
        self.pherMin = pherMax * self.mmasConst
        for i in range (len(tour)-1):
            currVert = tour[i]
            nextVert = tour[i+1]
            self.pher[currVert][nextVert] += newPher
        self.pher = np.clip(self.pher, self.pherMin, pherMax)

    def pherDecay(self):
        self.pher = np.dot(self.pher, self.rho)

    def greedyTour(self):
        gTour = []
        for i in range(self.numVerts):
            gTour.append(i)
        self.greedyLength = self.getTourDist(gTour)

    def two_opt(self):
        #print("Orig 2: " + str(self.getTourDist(self.bestTour)))
        best = self.bestTour
        improved = True
        while improved:
            improved = False
            for i in range(1, len(self.bestTour) - 2):
                for j in range(i + 1, len(self.bestTour)):
                    if j - i == 1: continue
                    if self.cost_change(best[i - 1], best[i], best[j - 1], best[j]) < 0:
                        best[i:j] = best[j - 1:i - 1:-1]
                        improved = True

    def cost_change(self, n1, n2, n3, n4):
        return self.edgeWeights[n1][n3] + self.edgeWeights[n2][n4] - self.edgeWeights[n1][n2] - self.edgeWeights[n3][n4]



        