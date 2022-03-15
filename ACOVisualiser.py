import streamlit as st
import pandas as pd
import numpy as np
import VisualiseTSP as vTSP
import VisualiseTour as vTour
import Utility as ut
from AntSystem import AntSystem

st.title("Ant Colony Optimisation")

marker_colour = st.sidebar.selectbox("Marker Colour", ("red", "black", "blue", "green"))
marker_size = st.sidebar.selectbox("Marker Size", ("0.25","0.5","1", "2", "3", "4"))

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
    antSys = AntSystem(data, 1)
    st.subheader("Tour")
    with st.spinner("Creating tour"):
        antSys.doTours()
        st.pyplot(vTour.renderTour(data, antSys.tours[0], marker_colour, marker_size))

if st.checkbox("Show raw tour"):
        st.subheader("Tours")
        st.write(antSys.tours)

