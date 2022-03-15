import math
from operator import index
from random import randint
import pandas as pd
import streamlit as st
import numpy as np

class Ant:
    currTour = []
    tabu = []
    numVerts = 0
    dist = []
    pher = []

    def __init__ (self, dist, pher, numVerts):
        self.currTour.clear()
        self.tabu.clear()
        self.numVerts = numVerts
        self.dist = dist
        self.pher = pher
        self.tabu = ([[False] * numVerts]) * numVerts
        

    def constructTour(self):
        first = randint(0, self.numVerts-1)
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
        for i in range(self.numVerts):
            if self.tabu[curr][i] == True or curr == i:
                weight.append(1000000)
            else:
                weight.append(self.dist[curr][i] + self.pher[curr][i])
                
        minVal = min(weight)
        minIndex = weight.index(minVal)
        self.tabu[curr][minIndex] = True
        self.tabu[minIndex][curr] = True
        return minIndex

