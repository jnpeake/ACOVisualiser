from operator import index
import random
import pandas as pd
import streamlit as st
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

    def __init__ (self, dist, pher, numVerts, alpha, beta, nnList):
        self.alpha = alpha
        self.beta = beta
        self.numVerts = numVerts
        self.dist = dist
        self.pher = pher
        self.nnList = nnList

    def reset(self):
        self.currTour.clear()
        self.tabu.clear()
        self.tabu = [False] * self.numVerts
        

    def constructTour(self):
        self.reset()
        first = random.randint(0, self.numVerts-1)
        curr = first
        i = 0
        self.currTour.append(first)
        while i < self.numVerts-1:
            curr = self.selectNext(curr)
            self.currTour.append(curr)
            i+=1
        self.currTour.append(first)
        self.two_opt()
        return self.currTour

    def selectNext(self, curr):
        weight = []
        randVal = random.random()
        validMove = False
        for i in self.nnList[curr]:
            if i >= len(self.tabu):
                print("hmm")
                print(i)
                print(len(self.tabu))
            if self.tabu[i] == True or curr == i:
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

    def selectClosest(self, index):
        sortedDist = sorted(self.dist[index])
        sortedIndex = np.argsort(self.dist[index])
        for i in sortedIndex[1:]:
            if self.tabu[i] == False:
                return i


    def two_opt(self):
        best = self.currTour
        improved = True
        while improved:
            improved = False
            for i in range(1, len(self.currTour) - 2):
                for j in range(i + 1, len(self.currTour)):
                    if j - i == 1: continue
                    if self.cost_change(best[i - 1], best[i], best[j - 1], best[j]) < 0:
                        best[i:j] = best[j - 1:i - 1:-1]
                        improved = True
            self.currTour = best
        

    def cost_change(self, n1, n2, n3, n4):
        return self.dist[n1][n3] + self.dist[n2][n4] - self.dist[n1][n2] - self.dist[n3][n4]

