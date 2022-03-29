from logging import PlaceHolder
import streamlit as st
import pandas as pd
import numpy as np
from RenderManager import RenderManager as rm
import Utility as ut
from AntSystem import AntSystem

st.title("Ant Colony Optimisation")

marker_colour = st.sidebar.selectbox("Marker Colour", ("red", "black", "blue", "green"), index = 0)
line_colour = st.sidebar.selectbox("Line Colour", ("red", "black", "blue", "green"), index = 0)
marker_size = st.sidebar.selectbox("Marker Size", ("0.25","0.5","1", "2", "3", "4"), index = 3)
nAnts = st.sidebar.number_input("Number of Ants", min_value = 1, max_value = 100)
nIter = st.sidebar.number_input("Number of Iterations", min_value = 1, max_value = 10000)
alpha = st.sidebar.number_input("Alpha", min_value = 1, max_value = 10)
beta = st.sidebar.number_input("Beta", min_value = 1, max_value = 10)
rho = st.sidebar.number_input("Rho", format="%.2f", min_value = 0.01, max_value = 1.0, value = 0.98)
numNN = st.sidebar.number_input("Nearest Neighbours", min_value = 4, max_value = 32, value = 16)

option = st.selectbox('Select TSP', (ut.getFileNames()))
data_raw = ut.open_tsp(option)
data = ut.convert_data(data_raw)
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

renderManager = rm(marker_colour, line_colour, marker_size)


st.subheader("TSP")
with st.spinner("Rendering TSP..."):
    st.pyplot(renderManager.renderPlot(data))

antSys = AntSystem(data, nAnts, alpha, beta, rho, numNN, renderManager)

prog_bar = st.progress(0)
placeholder = st.empty()

for i in range(nIter):
    antSys.doTourGen()
    if nIter > 1:
        prog_bar.progress(i/(nIter-1))
    if i % 10 == 0:
        with placeholder.container():
            col1, col2= st.columns(2)
            with col1:
                tourPlaceholder = st.pyplot(renderManager.renderTour(data, antSys.bestTour))
            with col2:
                pherPlaceholder = st.pyplot(renderManager.renderPher(data, antSys.pher))
            print(str(i) + ": "+ str(antSys.bestTourDist))
    
    

st.subheader("Best tour distance: "+ str(antSys.bestTourDist))

if st.checkbox("Show raw best tour"):
        st.subheader("Best tour")
        st.write(antSys.bestTour)

