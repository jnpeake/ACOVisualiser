from operator import index
import random
import pandas as pd
import numpy as np


class Ant:
    currTour = []
    tabu = []
    numVerts = 0
    dist = []
    pher = []
    nnList = []
    alpha = 1
    beta = 1

    def __init__ (self, dist, pher, numVerts, alpha, beta, nnList, novelty):
        self.alpha = alpha
        self.beta = beta
        self.numVerts = numVerts
        self.dist = dist
        self.pher = pher
        self.nnList = nnList
        self.novelty = novelty

    def reset(self):
        self.currTour.clear()
        self.tabu.clear()
        self.tabu = [False] * self.numVerts
        

    def constructTour(self, stagnated):
        self.reset()
        first = random.randint(0, self.numVerts-1)
        curr = first
        i = 0
        self.currTour.append(first)
        self.tabu[first] = True
        while i < self.numVerts-1:
            if(stagnated == False):
                curr = self.selectNext(curr)
            else:
                curr = self.selectNextStagnated(curr)
            self.currTour.append(curr)
            i+=1
        self.currTour.append(first)
        return self.currTour

    def selectNext(self, curr):
        weight = []
        randVal = random.random()
        validMove = False
        for i in self.nnList[curr]:
            if curr == i or self.tabu[i] == True:
                weight.append(-1)
            else:
                weight.append((pow(self.pher[curr][i],self.alpha) + pow(1/self.dist[curr][i],self.beta))*randVal)
                validMove = True
            
        if validMove == True:
            maxVal = max(weight)
            maxIndex = self.nnList[curr][weight.index(maxVal)]

        else:
            maxIndex = self.selectClosest(curr)

        self.tabu[maxIndex] = True
        return maxIndex

    def selectNextStagnated(self, curr):
        weight = []
        randVal = random.random()
        validMove = False
        for i in self.nnList[curr]:
            if curr == i or self.tabu[i] == True:
                weight.append(-1)
            else:
                weight.append((self.novelty[curr][i] + (1/self.dist[curr][i])) * randVal)
                validMove = True
            
        if validMove == True:
            maxVal = max(weight)
            maxIndex = self.nnList[curr][weight.index(maxVal)]

        else:
            maxIndex = self.selectClosest(curr)

        self.tabu[maxIndex] = True
        return maxIndex

    def selectClosest(self, index):
        sortedDist = sorted(self.dist[index])
        sortedIndex = np.argsort(self.dist[index])
        for i in sortedIndex[1:]:
            if self.tabu[i] == False:
                return i


    