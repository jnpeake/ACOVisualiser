import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def renderTour(data, tour, colour, size):
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
        ax.plot(xVals, yVals, marker = "o", markersize = size, linewidth = "1", color = colour)
    

    firstLastX = [dataList[tour[-2]][1], dataList[tour[-1]][1]]
    firstLastY = [dataList[tour[-2]][2], dataList[tour[-1]][2]]    
    ax.plot(firstLastX, firstLastY, marker = "o", markersize = size, linewidth = "1", color = colour)

    return fig