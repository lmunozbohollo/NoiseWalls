# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 19:42:23 2022

@author: luciamb

The dataset used for this script is: http://researchdata.gla.ac.uk/1258/

"""

from Filter_signals import Evoked_potentials
from Filter_signals import tasks_eeg

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import math


def calcVarSignal(participant,eeg_signal):
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

def peakMagnitude(participant,ep):
    evoked_potential = Evoked_potentials(participant,ep)
    time,avg = evoked_potential.get_averaged_ep()
    
    #plt.plot(time,avg)
    amplitude = max(avg)
    return amplitude
    
#p300 = peakMagnitude('004', 'rawp300')

def findSNR(participant,eeg_signal):
    #SNR = 10e-6**2 / calcVarSignal(participant,eeg_signal)
    SNR = findSignal(participant,'rawp300')**2 / calcVarSignal(participant,eeg_signal)
    #SNR = peakMagnitude('004', 'rawp300')**2 / calcVarSignal(participant, eeg_signal)
    SNR = 10*math.log10(SNR)
    return SNR


def calcMaxVar(participant,eeg_signal):
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
    for i in range(round(len(eeg)/2)):
        var = np.var(eeg[2*Fs*i:Fs*2*(i+1)])
        var_list.append(var)
        
    theta_max = max(var_list)
    #plt.plot(var_list)
    return theta_max


def calcMinVar(participant,eeg_signal):
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
    for i in range(round(len(eeg)/2)):
        var = np.var(eeg[2*Fs*i:Fs*2*(i+1)])
        # since the first 1500 values are 0, the stds at the start will be 0
        # we want to remove these
        if var > 0:
            var_list.append(var)
            
    theta_min = min(var_list)
    return theta_min


def calcRho(participant,eeg_signal):
    rho = np.sqrt(calcMaxVar(participant,eeg_signal) / calcMinVar(participant,eeg_signal))
    return rho

def calcNoiseWall(participant,eeg_signal):
    NoiseWall = calcRho(participant,eeg_signal) - (1 / calcRho(participant,eeg_signal))
    NoiseWall = 10*math.log10(NoiseWall)
    return NoiseWall

