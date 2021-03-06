# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:57:22 2022

@author: luciamb

Calculates the Noise Wall of each task for a participant

"""

import numpy as np
import sys
import math
from tabulate import tabulate

from researchdata1258 import Evoked_potentials
from researchdata1258 import tasks_eeg

# First we find the max and min variance of each task

def calcMaxVar(participant,eeg_signal):
    '''
    Here we use a sliding window spanning 2 seconds to find the maximum variance
    
    Returns: max variance (theta_max)
    
    '''
    
    if eeg_signal in ('rawvep', 'rawp300'):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        Fs = evoked_potential.Fs
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
        Fs = wanted_task.Fs
    
    #calculate moving variance and keep max value
    var_list = []
    for i in range(round(len(eeg)/5)):
        var = np.var(eeg[5*Fs*i:Fs*5*(i+1)])
        var_list.append(var)
        
    theta_max = max(var_list)
    return theta_max


def calcMinVar(participant,eeg_signal):
    '''
    Here we use a sliding window spanning 2 seconds to find the minimum variance
    
    Returns: min variance (theta_min)
    
    '''
    
    if eeg_signal in ('rawvep', 'rawp300'):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        Fs = evoked_potential.Fs
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
        Fs = wanted_task.Fs
    
    #calculate moving variance and keep min value
    var_list = []
    for i in range(round(len(eeg)/5)):
        var = np.var(eeg[5*Fs*i:Fs*5*(i+1)])
        # since the first 1500 values are 0, the stds at the start will be 0
        # we want to remove these
        if var > 0:
            var_list.append(var)
            
    theta_min = min(var_list)
    return theta_min


# Find the noise uncertainty, rho

def calcRho(participant,eeg_signal):
    '''
    Use theta_max and theta_min to find the noise uncertainty
    
    Returns: rho
    
    '''
    
    rho = np.sqrt(calcMaxVar(participant,eeg_signal) / calcMinVar(participant,eeg_signal))
    return rho


# Calculate the noise wall

def calcNoiseWall(participant,eeg_signal):
    '''
    Use the noise uncertainty to find the Noise Wall
    
    Returns: NoiseWall
    
    '''
    
    NoiseWall = calcRho(participant,eeg_signal) - (1 / calcRho(participant,eeg_signal))
    NoiseWall = 10*math.log10(NoiseWall)
    return NoiseWall



# if this is the main program

if __name__ == "__main__":

    participant = False
    
    all_tasks = ["rawvep", "rawp300", "jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]

    helptext = 'usage: {} participant\n'.format(sys.argv[0])
    helptext = helptext+'Possible participants : 1 to 20'

    if len(sys.argv) == 1:
        print("Type '{}' <participant> to select a different participant.".format(sys.argv[0]))
        participant = 1
        print("Returning Noise Walls for all tasks of participant {}".format(participant))

    if len(sys.argv) > 1:
        participant = int(sys.argv[1])
    
    rho_values = []
    nw_values = []
    
    for task in all_tasks:
        rho_values.append(calcRho(participant, task))
        nw_values.append(calcNoiseWall(participant, task))
    
    col_names = ['Task', 'rho', 'Noise Wall']
    data_points = [all_tasks, rho_values, nw_values]
    points = np.array(data_points).T.tolist()
    
    # display values on table
    print(tabulate(points, headers = col_names, tablefmt = "fancygrid"))
    
