# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 19:42:23 2022

@author: luciamb
"""

from Filter_signals import Evoked_potentials
from Filter_signals import tasks_eeg

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import math


def calcVarSignal(participant,eeg_signal):
    if eeg_signal in ("rawvep", "rawp300"):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
    
    var_signal = np.var(eeg)
    return var_signal

    
def plotPSD(participant,ep):
    evoked_potential = Evoked_potentials(participant,ep)
    eeg = evoked_potential.eeg
    
    # Define window length (4 seconds)
    win = 4 * Evoked_potentials.Fs
    freqs, psd = signal.welch(eeg, Evoked_potentials.Fs, nperseg=win)
    
    # Plot the power spectrum
    plt.figure('PSD'+ep, figsize=(8, 4))
    plt.plot(freqs, psd, color='k', lw=2)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power spectral density ($V^2$ / Hz)')
    plt.title("Welch's periodogram")
    psd_peak = max(psd)
    return psd_peak

def findSNR(participant,eeg_signal):
    #SNR = 10e-6**2 / calcVarSignal(participant,eeg_signal)
    SNR = 10**2 / calcVarSignal(participant,eeg_signal)
    SNR = 10*math.log10(SNR)
    return SNR

# the difference between both will be the power of the voluntary eeg
#power_p300 = plotPSD("004","rawp300")
#power_vep = plotPSD("004","rawvep")
#signal_value = power_p300 - power_vep


#SNR_vep = signal_value**2 / noise_vep**2
#SNR_p300 = signal_value**2 / noise_p300**2
SNR_vep = findSNR('004','rawvep')
SNR_p300 = findSNR('004','rawp300')


#SNR_jawclench = signal_value**2 / noise_jawclench**2
SNR_jawclench = findSNR('004','jawclench')


def calcMaxVar(participant,eeg_signal):
    if eeg_signal in ("rawvep", "rawp300"):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        Fs = evoked_potential.Fs
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
        Fs = wanted_task.Fs
    
    #calculate moving variance and keep median value
    var_list = []
    for i in range(len(eeg)):
        var = np.var(eeg[i:(Fs*2)+i])
        var_list.append(var)
        
    theta_max = np.median(var_list)
    return theta_max

def calcMinVar(participant,eeg_signal):
    if eeg_signal in ("rawvep", "rawp300"):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        Fs = evoked_potential.Fs
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
        Fs = wanted_task.Fs
    
    #calculate moving variance and keep min value
    var_list = []
    for i in range(len(eeg)):
        var = np.var(eeg[i:(Fs*2)+i])
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

rho_vep = calcRho('004', 'rawvep')
NWall_vep = calcNoiseWall('004', 'rawvep')

rho_p300 = calcRho('004', 'rawp300')
NWall_p300 = calcNoiseWall('004', 'rawp300')

rho_jawclench = calcRho('004', 'jawclench')
NWall_jawclench = calcNoiseWall('004', 'jawclench')
