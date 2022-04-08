from logging import PlaceHolder
from AntSystem import AntSystem

import string
import pandas as pd
import numpy as np
import time
import Utility as ut
import sys
import argparse

parser = argparse.ArgumentParser(description='An ACO solver for TSP with novelty matrix structure')
parser.add_argument('nAnts', metavar = 'nAnts', type = int, help = 'The number of ants used in the ACO algorithm' )
parser.add_argument('nIter', metavar = 'nIter', type = int, help = 'The number of iterations used in the ACO algorithm' )
parser.add_argument('nExp', metavar = 'nExp', type = int, help = 'The number of experiments performed with these settings' )
parser.add_argument('alpha', metavar = 'alpha', type = float, help = 'The value of the Alpha parameter, controlling pheromone influence' )
parser.add_argument('beta', metavar = 'beta', type = float, help = 'The value of the Beta parameter, controlling heuristic influence' )
parser.add_argument('rho', metavar = 'rho', type = float, help = 'The value of the Rho parameter, controlling pheromone decay' )
parser.add_argument('numNN', metavar = 'numNN', type = int, help = 'The size of the nearest neighbour list used in the ACO algorithm')
parser.add_argument('tsp', metavar='tsp',type=str,help='The filename of the TSP to be used')

args = parser.parse_args()

nAnts = args.nAnts
nIter = args.nIter
alpha = args.alpha
beta = args.beta
rho = args.rho
numNN = args.numNN

data_raw = ut.open_tsp(args.tsp)
data = ut.convert_data(data_raw)


for i in range(args.nExp):
    antSys = AntSystem(data, nAnts, alpha, beta, rho, numNN)
    startTime = time.time()
    for i in range(nIter):
        antSys.doTourGen(i)
    endTime = time.time()

    print("BEST TOUR: " + str(antSys.bestTourDist) + " | TIME: " + str(endTime-startTime))
    




