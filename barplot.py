# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 10:25:37 2022

@author: luciamb

To plot SNR vs Noise Wall of one participant

"""

from calculations import findSNR
from calculations import calcNoiseWall

import numpy as np
import matplotlib.pyplot as plt
import sys


TASKS = ["rawvep", "rawp300", "jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]


# data to plot	

if __name__ == "__main__":
    participant = False


    helptext = 'usage: {} participant\n'.format(sys.argv[0])
    helptext = helptext+'Possible participants : 1 to 20'

    if len(sys.argv) == 1:
        print("Type '{}' <participant> to select a different participant.".format(sys.argv[0]))
        participant = 1
        print("Barplot of participant {}".format(participant))

    if len(sys.argv) > 1:
        participant = int(sys.argv[1])


SNRs = []

for task in TASKS:
    SNR = findSNR(participant,task)
    SNRs.append(SNR)
    
NWs = []

for task in TASKS:
    NW = calcNoiseWall(participant,task)
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
plt.title('SNR vs Noise Wall, participant {}'.format(participant))
plt.xticks(index + bar_width, TASKS)
plt.legend()

plt.tight_layout()
plt.show()

