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
    alpha = 1
    beta = 1

    def __init__ (self, dist, pher, numVerts, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.numVerts = numVerts
        self.dist = dist
        self.pher = pher
        

    def reset(self):
        self.currTour.clear()
        self.tabu.clear()
        self.tabu = ([[False] * self.numVerts]) * self.numVerts
        

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

    def selectNext(self, curr):
        weight = []
        randVal = random.random()
        for i in range(self.numVerts):
            if self.tabu[curr][i] == True or curr == i:
                weight.append(1000000)
            else:
                weight.append((pow(self.dist[curr][i],self.alpha) + pow(self.pher[curr][i],self.beta))*randVal)
                
        minVal = min(weight)
        minIndex = weight.index(minVal)
        self.tabu[curr][minIndex] = True
        self.tabu[minIndex][curr] = True
        return minIndex

