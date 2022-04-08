import math
import pandas as pd
import numpy as np
import time
from Ant import Ant
import sys
np.set_printoptions(threshold=sys.maxsize)


class AntSystem:
    edgeWeights = []
    pher = []
    novelty = []
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


    def __init__ (self, data, nAnts, alpha, beta, rho, numNN, novelty, stagnantNum):
        self.reset()
        self.loadFile(data)
        self.data = data
        self.nAnts = nAnts
        self.rho = rho
        self.numNN = numNN
        self.calcNN()
        self.greedyTour()
        self.lastImproved = 0
        self.iterBestTour = []
        self.iterBestDist = 100000000000
        self.pher = np.full((self.numVerts, self.numVerts), float(1/(self.greedyLength*(1-rho))))
        self.novelty = np.full((self.numVerts, self.numVerts), float(1/(self.greedyLength*(1-rho))))
        self.noveltyEnabled = novelty
        self.stagnantNum = stagnantNum
        for i in range(nAnts):
            self.ants.append(Ant(self.edgeWeights,self.pher,self.numVerts, alpha, beta, self.nnList, self.novelty, self.noveltyEnabled))
        a = math.exp(math.log(0.05) / self.numVerts)
        self.mmasConst = (1 - a) / ((self.numVerts + 1) * a * 0.5)
    
    def reset(self):
        self.edgeWeights.clear()
        self.pher.clear()
        self.novelty.clear()
        self.ants.clear()
        self.tours.clear()
        self.bestTour.clear()
        self.nnList.clear()


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

                dist = ((x0 - x1) * (x0 - x1)) + ((y0 - y1) * (y0 - y1))
                dist = math.sqrt(dist)
                weights.append(round(dist))
            self.edgeWeights.append(weights)
    
    def calcNN(self):
        for weightList in self.edgeWeights:
            sortedIndicies = np.argsort(np.array(weightList))
           
            self.nnList.append(sortedIndicies[1:self.numNN-1])

    def doTourGen(self, iter):
        for ant in self.ants:
            if self.noveltyEnabled:
                if self.lastImproved >= self.stagnantNum:
                    ant.constructTour(True)
                else:
                    ant.constructTour(False)
            else:
                ant.constructTour(False)
            self.tours.append(ant.currTour.copy())
        self.lastImproved += 1
        self.getIterBestTour()
        self.two_opt()
        self.iterBestDist = self.getTourDist(self.iterBestTour)
        self.getBestTour()
        self.bestTourDist = self.getTourDist(self.bestTour)
        self.updatePher()
        self.pherDecay()
        if self.noveltyEnabled:           
            self.updateNovelty()
            self.noveltyIncrease()
        self.tours.clear()
        self.iterBestTour = []
        self.iterBestDist = 10000000000

        

    def getBestTour(self):
        if self.iterBestDist < self.bestTourDist:
            self.bestTour = self.iterBestTour.copy()
            self.bestTourDist = self.iterBestDist
            self.lastImproved = 0
            #print("Original Original: " + str(dist))


    def getIterBestTour(self):
        for i, tour in enumerate(self.tours):
            dist = self.getTourDist(tour)
            if dist < self.iterBestDist:
                self.iterBestTour = tour.copy()
                self.iterBestDist = dist


    def getTourDist(self, tour):
        tourDist = 0
        for i in range(len(tour)-1):
            currVert = tour[i]
            nextVert = tour[i+1]
            tourDist += self.edgeWeights[currVert][nextVert]
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

    def updateNovelty(self):
        tour = self.bestTour
        newNovelty = 1/self.bestTourDist
        for i in range (len(tour)-1):
            currVert = tour[i]
            nextVert = tour[i+1]
            self.novelty[currVert][nextVert] -= newNovelty

    def pherDecay(self):
        self.pher = np.dot(self.pher, self.rho)

    def noveltyIncrease(self):
        self.novelty = np.divide(self.novelty, self.rho)

    def greedyTour(self):
        gTour = []
        for i in range(self.numVerts):
            gTour.append(i)
        self.greedyLength = self.getTourDist(gTour)

    def two_opt(self):
        #print("Orig 2: " + str(self.getTourDist(self.bestTour)))
        best = self.iterBestTour
        improved = True
        while improved:
            improved = False
            for i in range(1, len(self.iterBestTour) - 2):
                for j in range(i + 1, len(self.iterBestTour)):
                    if j - i == 1: continue
                    if self.cost_change(best[i - 1], best[i], best[j - 1], best[j]) < 0:
                        best[i:j] = best[j - 1:i - 1:-1]
                        improved = True

    def cost_change(self, n1, n2, n3, n4):
        return self.edgeWeights[n1][n3] + self.edgeWeights[n2][n4] - self.edgeWeights[n1][n2] - self.edgeWeights[n3][n4]



        