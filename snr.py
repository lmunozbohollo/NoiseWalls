# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 17:00:34 2022

@author: luciamb

Calculates the SNR of each task for a participant

"""

import numpy as np
import sys
import scipy.signal as signal
import math
from tabulate import tabulate

from p300 import signalPwr
from researchdata1258 import Evoked_potentials
from researchdata1258 import tasks_eeg


def calcVarSignal(participant,eeg_signal):
    '''
    Find the variance of each raw signal
    
    Returns: var_signal
    
    '''
    
    if eeg_signal in ('rawvep', 'rawp300'):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
    
    var_signal = np.var(eeg)
    return var_signal

    
def findSignal(participant,ep):
    evoked_potential = Evoked_potentials(participant,ep)
    eeg = evoked_potential.eeg
    
    # Define window length (4 seconds)
    win = 4 * Evoked_potentials.Fs
    freqs, psd = signal.welch(eeg, Evoked_potentials.Fs, nperseg=win)
    
    psd_peak = max(psd)
    return psd_peak


def findSNR(participant,eeg_signal):
    '''
    Use the variance and signal amplitude to find the SNR 
    
    Returns: var_signal
    
    '''
    
    #SNR = 10e-6**2 / calcVarSignal(participant,eeg_signal)
    #SNR = findSignal(participant,'rawp300')**2 / calcVarSignal(participant,eeg_signal)
    SNR = signalPwr(participant, 'rawp300')**2 / calcVarSignal(participant, eeg_signal)
    SNR = 10*math.log10(SNR)
    return SNR




# if this is the main program

if __name__ == "__main__":

    participant = False
    
    all_tasks = ["rawvep", "rawp300", "jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]

    helptext = 'usage: {} participant\n'.format(sys.argv[0])
    helptext = helptext+'Possible participants : 1 to 20'

    if len(sys.argv) == 1:
        print("Type '{}' <participant> to select a different participant.".format(sys.argv[0]))
        participant = 1
        print("Returning SNRs for all tasks of participant {}".format(participant))

    if len(sys.argv) > 1:
        participant = int(sys.argv[1])
    
    SNRs = []
    
    for task in all_tasks:
        SNRs.append(findSNR(participant, task))
    
    col_names = ['Task', 'SNR']
    data_points = [all_tasks, SNRs]
    points = np.array(data_points).T.tolist()
    
    # display values on table
    print(tabulate(points, headers = col_names, tablefmt = "fancygrid"))
    
    
