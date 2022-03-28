# NoiseWalls

This repository is to be cloned to your computer. Into the same folder download the EEG recordings of participants from the database, found at http://researchdata.gla.ac.uk/1258/

First run 'Filter_signals.py' which filters the raw data of the evoked potentials using the Evoked_potentials class and the rest of recordings using the tasks_eeg class.

Then run 'calculations.py' to carry out all the steps to calculate the SNR and Noise Wall of the different tasks. The code is set to run for participant 4.

Finally, 'barplot.py' outputs a barplot with the noise wall and snr data of one participant.
