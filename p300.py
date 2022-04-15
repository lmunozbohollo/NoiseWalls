# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 12:12:37 2022

@author: luciamb

Plots the averaged P300 response and gives the value of the max amplitude

"""

import matplotlib.pyplot as plt
import sys

from researchdata1258 import Evoked_potentials


def peakMagnitude(participant,ep):
    evoked_potential = Evoked_potentials(participant,ep)
    time,avg = evoked_potential.get_averaged_ep()
    
    fig = 'P300'
    plt.figure(fig)
    plt.plot(time,avg)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude ($\mu$V)")
    plt.title("P300 peak, participant {}".format(participant))
    
    max_val = avg[0]
    max_val_idx = 0
    
    #for i in range(len(avg)):
    for i in range(75,125):
        if avg[i] > max_val:
            max_val = avg[i]
            max_val_idx = i
        
    amplitude = max_val
    idx = max_val_idx
    
    plt.plot(time[idx],amplitude,'ro')
    plt.text(time[idx+5],amplitude,round(amplitude,2))
    
    return amplitude


def signalPwr(participant,ep):
    evoked_potential = Evoked_potentials(participant,ep)
    time,avg = evoked_potential.get_averaged_ep()
    
    max_val = avg[0]
    
    for i in range(75,125):
        if avg[i] > max_val:
            max_val = avg[i]
        
    amplitude = max_val
    
    return amplitude


# if this is the main program

if __name__ == "__main__":
    participant = False

    helptext = 'usage: {} participant\n'.format(sys.argv[0])
    helptext = helptext+'Possible participants : 1 to 20'

    if len(sys.argv) == 1:
        print("Type '{}' <participant> to select a different participant.".format(sys.argv[0]))
        participant = 1
        print("Plotting P300 of participant {}".format(participant))

    if len(sys.argv) > 1:
        participant = int(sys.argv[1])
    
        
    peakMagnitude(participant,'rawp300')

plt.show()
