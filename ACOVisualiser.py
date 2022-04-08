from asyncio.windows_events import NULL
from logging import PlaceHolder
from AntSystem import AntSystem
from multiprocessing import Pool

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

parser.add_argument('--opt',type=int,help='The optimum value of the used TSP, if known')
parser.add_argument('--novelty', '-n', action="store_true", help = 'Enables the novelty matrix structure & related behaviours')
parser.add_argument('--stagnation', '-s',type = int, help = 'The number of iterations without improvement before the ACO is considered to be stagnant')

args = parser.parse_args()

nAnts = args.nAnts
nIter = args.nIter
alpha = args.alpha
beta = args.beta
rho = args.rho
numNN = args.numNN

data_raw = ut.open_tsp(args.tsp)
data = ut.convert_data(data_raw)

f = open ("test1.txt", 'w')

def doExperiment():
    antSys = AntSystem(data, nAnts, alpha, beta, rho, numNN, args.novelty, args.stagnation)
    startTime = time.time()
    for j in range(nIter):
        antSys.doTourGen(j)
    endTime = time.time()
    if(args.opt == NULL):
        print("BEST TOUR - " + str(antSys.bestTourDist) + " | TIME - " + str(endTime-startTime))
        return("BEST TOUR - " + str(antSys.bestTourDist) + " | TIME - " + str(endTime-startTime))
    else:
        percentage = ((antSys.bestTourDist - args.opt)/ args.opt) * 100
        print("BEST TOUR - " + str(antSys.bestTourDist) + " | TIME - " + str(endTime-startTime) + " | " + str(percentage) + "% from opt" )
        return("BEST TOUR - " + str(antSys.bestTourDist) + " | TIME - " + str(endTime-startTime) + " | " + str(percentage) + "% from opt" )
       
if __name__ == '__main__':
    with Pool(2) as p: 
        for result in p.starmap(doExperiment, [() for _ in range(args.nExp)]):
            f.write("\n"+result)
    f.close()

    




