# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 10:25:37 2022

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
    

n_groups = len(TASKS)


# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, SNRs, bar_width,
alpha=opacity,
color='r',
label='SNR')

rects2 = plt.bar(index + bar_width, NWs, bar_width,
alpha=opacity,
color='y',
label='Noise Wall')

plt.xlabel('Task')
plt.ylabel('dB')
plt.title('SNR vs Noise Wall')
plt.xticks(index + bar_width, TASKS)
plt.legend()

plt.tight_layout()
plt.show()

