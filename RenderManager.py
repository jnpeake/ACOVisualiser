import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class RenderManager:

    markerColour = ""
    lineColour = ""
    markerSize = ""

    def __init__(self, markerColour, lineColour, markerSize):
        self.markerColour = markerColour
        self.lineColour = lineColour
        self.markerSize = markerSize


    def renderTour(self, data, tour):
        fig, ax = plt.subplots()
        plt.xscale("linear")
        plt.yscale("linear")
        plt.xticks([])
        plt.yticks([])
        ax.axis('equal')
        dataList = data.values.tolist()
        for i in range(len(tour)-1):
            vert = tour[i]
            nextVert = tour[i+1]        
            xVals = [dataList[vert][1], dataList[nextVert][1]]
            yVals = [dataList[vert][2], dataList[nextVert][2]]
            ax.plot(xVals, yVals, marker = "o", markersize = self.markerSize, linewidth = "1", c = self.lineColour, mec = self.markerColour, mfc = self.markerColour)
        

        firstLastX = [dataList[tour[-2]][1], dataList[tour[-1]][1]]
        firstLastY = [dataList[tour[-2]][2], dataList[tour[-1]][2]]    
        ax.plot(firstLastX, firstLastY, marker = "o", markersize = self.markerSize, linewidth = "1", c = self.lineColour,  mec = self.markerColour, mfc = self.markerColour)

        return fig

    def renderPher(self, data, pher):
        fig, ax = plt.subplots()
        plt.xscale("linear")
        plt.yscale("linear")
        plt.xticks([])
        plt.yticks([])
        ax.axis('equal')
        pherMin = pher.min()
        dataList = data.values.tolist()
        for i in range(len(pher)):
            for j in range (len(pher[i])):
                if pher[i][j] is not pherMin:
                    xVals = [dataList[i][1], dataList[j][1]]
                    yVals = [dataList[i][2], dataList[j][2]]
                    ax.plot(xVals, yVals, marker = "o", markersize = self.markerSize, linewidth = (pher[i][j] - (pher.min()))*100, c = self.lineColour, mec = self.markerColour, mfc = self.markerColour)
        return fig

   

    def renderPlot(self, data):
        fig, ax = plt.subplots()
        plt.xscale("linear")
        plt.yscale("linear")
        plt.xticks([])
        plt.yticks([])
        ax.axis('equal')
        ax.plot(data["X"], data["Y"], marker = "o", linewidth = 0, markersize = self.markerSize, c = self.markerColour)
        
        return fig