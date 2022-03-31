# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:28:01 2022

@author: luciamb
"""


import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.signal as signal
import math

from snr import findSNR
from noisewall import calcNoiseWall


TASKS = ["rawvep", "rawp300", "jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]


# data to plot	

if __name__ == "__main__":
    participant = False

    helptext = 'usage: {} participant\n'.format(sys.argv[0])
    helptext = helptext+'Participants included : 1 to 20'


SNRs = []
NWs = []

for participant in range(1,21):
    for task in TASKS:
        SNR = findSNR(participant,task)
        NW = calcNoiseWall(participant,task)
        
        SNRs.append(SNR)
        NWs.append(NW)
    
SNRs = np.matrix(SNRs)
SNRs = SNRs.reshape((10,20))
SNRs = np.mean(SNRs, axis=1)


NWs = np.matrix(NWs)
NWs = NWs.reshape((10,20))
NWs = np.mean(NWs, axis=1)



a = []
for x in np.array(SNRs).flat:
   a.append(x)

b = []
for x in np.array(NWs).flat:
   b.append(x)


print(a)
print(b)

n_groups = len(TASKS)


# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, a, bar_width,
alpha=opacity,
color='r',
label='SNR')

rects2 = plt.bar(index + bar_width, b, bar_width,
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
