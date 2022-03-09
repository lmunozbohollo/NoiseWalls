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


def calcStdSignal(participant,eeg_signal):
    if eeg_signal in ("rawvep", "rawp300"):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
    
    std_signal = np.std(eeg)
    return std_signal

    
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


# the difference between both will be the power of the voluntary eeg
power_p300 = plotPSD("004","rawp300")
power_vep = plotPSD("004","rawvep")
signal_value = power_p300 - power_vep

noise_vep = calcStdSignal("004", "rawvep")
noise_p300 = calcStdSignal("004", "rawp300")

#SNR_vep = signal_value**2 / noise_vep**2
#SNR_p300 = signal_value**2 / noise_p300**2
SNR_vep = 10e-6**2 / noise_vep**2
SNR_p300 = 10e-6**2 / noise_p300**2


noise_jawclench = calcStdSignal("004", "jawclench")
#SNR_jawclench = signal_value**2 / noise_jawclench**2
SNR_jawclench = 10e-6**2 / noise_jawclench**2


def calcMaxSTD(participant,eeg_signal):
    if eeg_signal in ("rawvep", "rawp300"):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        Fs = evoked_potential.Fs
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
        Fs = wanted_task.Fs
    
    #calculate moving standard deviation and keep max value
    std_list = []
    for i in range(len(eeg)):
        std = np.std(eeg[i:(Fs*2)+i])
        std_list.append(std)
        
    theta_max = max(std_list)
    return theta_max

def calcMinSTD(participant,eeg_signal):
    if eeg_signal in ("rawvep", "rawp300"):
        evoked_potential = Evoked_potentials(participant,eeg_signal)
        eeg = evoked_potential.eeg
        Fs = evoked_potential.Fs
        
    else:
        wanted_task = tasks_eeg(participant,eeg_signal)
        eeg = wanted_task.ch1
        Fs = wanted_task.Fs
    
    #calculate moving standard deviation and keep min value
    std_list = []
    for i in range(len(eeg)):
        std = np.std(eeg[i:(Fs*2)+i])
        # since the first 1500 values are 0, the stds at the start will be 0
        # we want to remove these
        if std > 0:
            std_list.append(std)
            
    theta_min = min(std_list)
    return theta_min


def calcRho(participant,eeg_signal):
    rho = np.sqrt(calcMaxSTD(participant,eeg_signal) / calcMinSTD(participant,eeg_signal))
    return rho

def calcNoiseWall(participant,eeg_signal):
    NoiseWall = calcRho(participant,eeg_signal) - (1 / calcRho(participant,eeg_signal))
    return NoiseWall

rho_vep = calcRho('004', 'rawvep')
NWall_vep = calcNoiseWall('004', 'rawvep')

rho_p300 = calcRho('004', 'rawp300')
NWall_p300 = calcNoiseWall('004', 'rawp300')

rho_jawclench = calcRho('004', 'jawclench')
NWall_jawclench = calcNoiseWall('004', 'jawclench')