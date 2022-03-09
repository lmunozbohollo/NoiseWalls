# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 10:35:56 2022

@author: luciamb
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal


class Evoked_potentials:
    EPs = ["rawvep", "rawp300"]
    Fs = 250
    
    def __init__(self,_participant,_ep,do_filter_data = True):
        self.participant = _participant
        self.ep = _ep
        fullpath = 'participant'+self.participant+'/'+self.ep+'.tsv'
        #fullpath = "participant{}/{}.tsv".format(self.participant,self.EPs[_ep])
        self.data = np.loadtxt(fullpath)
        self.t = np.linspace(0,len(self.data)/self.Fs,len(self.data))
        self.eeg = self.data[:,0]*1e6
        self.oddball_flags = self.data[:,2]
        self.oddball_samples = np.argwhere(self.oddball_flags > 0.5)
        self.initial_samples_to_ignore = 0
        if do_filter_data:
            self.__filter_data()

    def __filter_data(self):
        # Remove DC
        bHigh,aHigh = signal.butter(2,0.25/self.Fs*2,'high')
        self.eeg = signal.lfilter(bHigh,aHigh,self.eeg);
        # for VEP
        self.initial_samples_to_ignore = int(self.Fs / 0.5) * 3

        # Remove 50Hz noise
        b50,a50 = signal.butter(4,[48/self.Fs*2,52/self.Fs*2],'stop')
        self.eeg = signal.lfilter(b50,a50,self.eeg);

        # Remove 150Hz interference
        b100,a100 = signal.butter(4,[98/self.Fs*2,102/self.Fs*2],'stop')
        self.eeg = signal.lfilter(b100,a100,self.eeg);
        
        ign = self.initial_samples_to_ignore
        self.eeg[0:ign] = 0 # to not plot first few seconds
        
    def get_averaged_ep(self):
        """
        Calculates the evoked potential usign the oddball samples and
        averages over them.
        Returns: timestamps,vep
        """
        self.navg = int(self.Fs)
        self.avg = np.zeros(self.navg)
        
        n = 0
        for [ob] in self.oddball_samples:
            if ((ob+self.navg) < len(self.eeg)) and (ob > self.initial_samples_to_ignore):
                self.avg = self.avg + self.eeg[int(ob):int(ob+self.navg)]
                n = n + 1
        
        avg = self.avg
        
        time = np.linspace(0,self.navg/self.Fs,self.navg) * 1000
        return time,avg


class tasks_eeg:
    TASKS = ["jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]
    Fs = 500
    
    def __init__(self,_participant,_task,filterData=True):
        self.participant = _participant
        self.task = _task
        path = 'participant'+self.participant+'/'+self.task+'.tsv'
        self.data = np.loadtxt(path)
        
        self.t = np.linspace(0,len(self.data)/self.Fs,len(self.data))
        self.ch1 = self.data[:,7]*1e6
        self.ch2 = self.data[:,8]*1e6
        if not filterData:
            return

        # Remove DC
        bHigh,aHigh = signal.butter(4,1/self.Fs*2,'high')
        self.ch1 = signal.lfilter(bHigh,aHigh,self.ch1);
        self.ch2 = signal.lfilter(bHigh,aHigh,self.ch2);
        
        # Remove 50Hz noise
        b50,a50 = signal.butter(4,[48/self.Fs*2,52/self.Fs*2],'stop')
        self.ch1 = signal.lfilter(b50,a50,self.ch1);
        self.ch2 = signal.lfilter(b50,a50,self.ch2);
        
        # Remove 150Hz interference
        b150,a150 = signal.butter(4,[148/self.Fs*2,152/self.Fs*2],'stop')
        self.ch1 = signal.lfilter(b150,a150,self.ch1);
        self.ch2 = signal.lfilter(b150,a150,self.ch2);

        # 2secs muted
        self.ch1[0:1000] = 0
        self.ch2[0:1000] = 0


def plotEPofOneSubject(participant,ep):
    plt.figure(ep)
    plt.suptitle("Participant {}, {}".format(participant,ep))
    evoked_potential = Evoked_potentials(participant,ep)
    eeg = evoked_potential.eeg

    plt.subplot(211)
    plt.plot(evoked_potential.t,eeg*1e6)
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude ($\mu$V)')
    plt.title("Raw filtered data")

    t, avg = evoked_potential.get_averaged_ep()
    plt.subplot(212)
    plt.plot(t,avg)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude ($\mu$V)")
    plt.title("Evoked potential")