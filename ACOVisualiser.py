import streamlit as st
import pandas as pd
import numpy as np
import VisualiseTSP as vTSP
import VisualiseTour as vTour
import Utility as ut
from AntSystem import AntSystem

st.title("Ant Colony Optimisation")

marker_colour = st.sidebar.selectbox("Marker Colour", ("red", "black", "blue", "green"), index = 0)
marker_size = st.sidebar.selectbox("Marker Size", ("0.25","0.5","1", "2", "3", "4"), index = 3)
nAnts = st.sidebar.number_input("Number of Ants", min_value = 1, max_value = 100)
nIter = st.sidebar.number_input("Number of Iterations", min_value = 1, max_value = 1000)
alpha = st.sidebar.number_input("Alpha", min_value = 1, max_value = 10)
beta = st.sidebar.number_input("Beta", min_value = 1, max_value = 10)
rho = st.sidebar.number_input("Rho", format="%.2f", min_value = 0.01, max_value = 1.0, value = 0.98)

option = st.selectbox('Select TSP', (ut.getFileNames()))
data_raw = vTSP.open_tsp(option)
data = vTSP.convert_data(data_raw)
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("TSP")
    with st.spinner("Rendering TSP..."):
        st.pyplot(vTSP.renderPlot(data, marker_colour, marker_size))
with col2:
    antSys = AntSystem(data, nAnts, alpha, beta, rho)
    st.subheader("Tour")
    with st.spinner("Creating tour"):
        antSys.doTours(nIter)
        st.pyplot(vTour.renderTour(data, antSys.bestTour, marker_colour, marker_size))

st.subheader("Best tour distance: "+ str(antSys.bestTourDist))

if st.checkbox("Show raw best tour"):
        st.subheader("Best tour")
        st.write(antSys.bestTour)

