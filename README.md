# NoiseWalls

This repository is to be cloned to your computer and into the same folder download the EEG recordings of participants from the GitLab repository. 

First run 'Filter_signals.py' which filters the raw data of the evoked potentials using the Evoked_potentials class and the rest of recordings using the tasks_eeg class.

Then run 'calculations.py' to carry out all the steps to find the SNR and Noise Wall of the different tasks. The code is set to run for participant 4 and gives out the SNR and Noise Wall of the vep, p300 and jawclench files.

To find the SNR of other tasks use the line of code:

```
10e-6**2 / calcStdSignal(participant, task)
```

To find the Noise Wall use the line of code:

```
calcNoiseWall(participant, task)
```

