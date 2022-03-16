# -*- coding: utf-8 -*-
"""
Created on Tue Mar 8 17:25:37 2022

@author: luciamb
"""

from calculations import findSNR
from calculations import calcNoiseWall

import numpy as np
import matplotlib.pyplot as plt


TASKS = ["rawvep", "rawp300", "jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]


# data to plot

SNRs = []

for task in TASKS:
    SNR = findSNR('004',task)
    SNRs.append(SNR)
    
NWs = []

for task in TASKS:
    NW = calcNoiseWall('004',task)
    NWs.append(NW)
    

