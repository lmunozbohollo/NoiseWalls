# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:28:01 2022

@author: luciamb
"""


import numpy as np
import sys
import matplotlib.pyplot as plt
from tabulate import tabulate

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

# partiicpants 2 and 6 not included due to issues with the recordings
participants = ['1','3','4','5','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

for participant in participants:
    for task in TASKS:
        SNR = findSNR(participant,task)
        NW = calcNoiseWall(participant,task)
        
        SNRs.append(SNR)
        NWs.append(NW)
    
SNRs = np.matrix(SNRs)
SNRs = SNRs.reshape((18,10))
SNRs_mean = np.mean(SNRs, axis=0)
SNRs_var = np.var(SNRs, axis=0)

NWs = np.matrix(NWs)
NWs = NWs.reshape((18,10))
NWs_mean = np.mean(NWs, axis=0)
NWs_var = np.var(NWs, axis=0)



a = []
for x in np.array(SNRs_mean).flat:
   a.append(x)

a_var = []
for x in np.array(SNRs_var).flat:
   a_var.append(x)

b = []
for x in np.array(NWs_mean).flat:
   b.append(x)

b_var = []
for x in np.array(NWs_var).flat:
   b_var.append(x)

print(a)
print(b)

n_groups = len(TASKS)

# print table with values and variances
col_names = ['Task', 'Average SNR', 'Variance SNR', 'Average NW', 'Variance NW']
data_points = [TASKS, a, a_var, b, b_var]
points = np.array(data_points).T.tolist()

# display values on table
print(tabulate(points, headers = col_names, tablefmt = "fancygrid"))

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
