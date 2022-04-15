# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 10:35:56 2022

@author: luciamb

To be used on the following dataset: http://researchdata.gla.ac.uk/1258/ 

"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import sys

class Evoked_potentials:
    EPs = ["rawvep", "rawp300"]
    Fs = 250
    
    def __init__(self,_participant,_ep,do_filter_data = True):
        self.participant = _participant
        self.ep = _ep
        fullpath = "EEG_recordings/participant{}/{}.tsv".format(str(self.participant).zfill(3),self.ep)
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
        
        # Uncomment for 20Hz cutoff
        #bLow,aLow = signal.butter(4,20/self.Fs*2,'low')
        #self.eeg = signal.lfilter(bLow,aLow,self.eeg);
        
        # Uncomment for 100Hz cutoff
        #bLow,aLow = signal.butter(4,100/self.Fs*2,'low')
        #self.eeg = signal.lfilter(bLow,aLow,self.eeg);
        
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

        self.avg = self.avg / n
        avg = self.avg
        
        time = np.linspace(0,self.navg/self.Fs,self.navg) * 1000
        return time,avg


class tasks_eeg:
    TASKS = ["jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]
    Fs = 500
    
    def __init__(self,_participant,_task,filterData=True):
        self.participant = _participant
        self.task = _task
        path = "EEG_recordings/participant{}/{}.tsv".format(str(self.participant).zfill(3),self.task)
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
        
        # Uncomment for 20Hz cutoff
        #bLow,aLow = signal.butter(4,20/self.Fs*2,'low')
        #self.ch1 = signal.lfilter(bLow,aLow,self.ch1);
        #self.ch2 = signal.lfilter(bLow,aLow,self.ch2);

        # Uncomment for 100Hz cutoff
        #bLow,aLow = signal.butter(4,100/self.Fs*2,'low')
        #self.ch1 = signal.lfilter(bLow,aLow,self.ch1);
        #self.ch2 = signal.lfilter(bLow,aLow,self.ch2);
        
        # 2secs muted
        self.ch1[0:1000] = 0
        self.ch2[0:1000] = 0


# if this is the main program

if __name__ == "__main__":
    participant = False


    helptext = 'usage: {} participant\n'.format(sys.argv[0])
    helptext = helptext+'Possible participants : 1 to 20'

    if len(sys.argv) == 1:
        print("Type '{} <participant>' to select a different participant.".format(sys.argv[0]))
        participant = 1
        print("Plotting all tasks of participant {}".format(participant))

    if len(sys.argv) > 1:
        participant = int(sys.argv[1])
    
    all_tasks = ["rawvep", "rawp300", "jawclench", "read", "colour", "wordsearch", "sudoku", "phoneApp", "lyingEC", "lyingEO"]
    
    for eeg_signal in all_tasks:
        if eeg_signal in ('rawvep', 'rawp300'):
            evoked_potential = Evoked_potentials(participant,eeg_signal)
            eeg = evoked_potential.eeg
            
            plt.figure(eeg_signal)
            plt.suptitle("Participant {}, {}".format(participant,eeg_signal))
            
            plt.subplot(211)            
            plt.plot(evoked_potential.t,eeg*1e6)
            plt.xlabel('Time (sec)')
            plt.ylabel('Amplitude ($\mu$V)')
            
            t, avg = evoked_potential.get_averaged_ep()
            plt.subplot(212)
            plt.plot(t,avg)
            plt.xlabel("Time (ms)")
            plt.ylabel("Amplitude ($\mu$V)")
            plt.title("Evoked potential")
            
        else:
            wanted_task = tasks_eeg(participant,eeg_signal)
            ch1 = wanted_task.ch1
            ch2 = wanted_task.ch2
            
            plt.figure(eeg_signal)
            plt.suptitle("Participant {}, {}".format(participant,eeg_signal))
            
            plt.subplot(211)
            plt.plot(wanted_task.t,ch1)
            plt.xlabel('Time (sec)')
            plt.ylabel('Amplitude (V)')
            plt.title("Channel 1")
            
            plt.subplot(212)
            plt.plot(wanted_task.t,ch2)
            plt.xlabel("Time (sec)")
            plt.ylabel("Amplitude (V)")
            plt.title("Channel 2")
            
plt.show()

