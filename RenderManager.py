import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RenderManager:

    def __init__(self, markerColour, lineColour, markerSize, data):
        self.markerColour = markerColour
        self.lineColour = lineColour
        self.markerSize = markerSize
        self.pherFig = plt.figure(1)
        self.tourFig = plt.figure(2)
        self.plotFig = plt.figure(3)
        self.pherAx = self.pherFig.add_subplot(1,1,1)
        self.tourAx = self.tourFig.add_subplot(1,1,1)
        self.plotAx = self.plotFig.add_subplot(1,1,1)
        self.setAxSettings(self.pherAx)
        self.setAxSettings(self.tourAx)
        self.setAxSettings(self.plotAx)
        self.dataList = data.values.tolist()
        

    def renderTour(self, tour):
        ax = self.tourAx
        self.setAxSettings(ax)
        for i in range(len(tour)-1):
            vert = tour[i]
            nextVert = tour[i+1]        
            xVals = [self.dataList[vert][1], self.dataList[nextVert][1]]
            yVals = [self.dataList[vert][2], self.dataList[nextVert][2]]
            ax.plot(xVals, yVals, marker = "o", markersize = self.markerSize, linewidth = "1", c = self.lineColour, mec = self.markerColour, mfc = self.markerColour)
        

        firstLastX = [self.dataList[tour[-2]][1], self.dataList[tour[-1]][1]]
        firstLastY = [self.dataList[tour[-2]][2], self.dataList[tour[-1]][2]]    
        ax.plot(firstLastX, firstLastY, marker = "o", markersize = self.markerSize, linewidth = "1", c = self.lineColour,  mec = self.markerColour, mfc = self.markerColour)

        return self.tourFig

    def renderPher(self, pher):
        ax = self.pherAx
        self.setAxSettings(ax)
        #pherMin = pher.min()

        #for i in range(len(pher)):
           # for j in range (len(pher[i])):
               # if pher[i][j] is not pherMin:
                 #   xVals = [self.dataList[i][1], self.dataList[j][1]]
                  #  yVals = [self.dataList[i][2], self.dataList[j][2]]
                   # ax.plot(xVals, yVals, marker = "o", markersize = self.markerSize, linewidth = (pher[i][j] - (pher.min()))*100, c = self.lineColour, mec = self.markerColour, mfc = self.markerColour)
        ax.matshow(pher)
        return self.pherFig

   

    def renderPlot(self, data):
        ax = self.plotAx
        self.setAxSettings(ax)
        ax.plot(data["X"], data["Y"], marker = "o", linewidth = 0, markersize = self.markerSize, c = self.markerColour)
        
        return self.plotFig

    def setAxSettings(self, ax):
        ax.clear()
        ax.set_xscale("linear")
        ax.set_yscale("linear")
        ax.set_xticks([])
        ax.set_yticks([])
