# NoiseWalls

This repository is to be cloned to your computer. Into the same folder download the EEG recordings of participants from the database, found at http://researchdata.gla.ac.uk/1258/


The files will produce the following outputs when run indenpendently:

* 'researchdata1258.py' : Loads and filters the raw data. Plots all tasks for 1 participant.

* 'p300.py' : Calculates the averaged P300 peak. Plots the P300 and shows the maximum amplitude.

* 'noisewall.py' : Calculates the minimum and maximum variances of each signal using a sliding window. Prints out a table with the uncertainty (rho) and noise wall values for each task.

* 'snr.py' : Calls p300.py to get the signal power. Calculates the variance of each raw signal. Prints out a table with the snr values for each task.


## Packages

In order to run this code make sure the following packages are installed in your device:

```
pip install numpy
pip install matplotlib
pip install scipy
pip install sys
pip install math
pip install tabulate
```
