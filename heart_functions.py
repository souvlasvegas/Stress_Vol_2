# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:37:59 2023

@author: AndreasMiltiadous
"""

import heartpy as hp
from tkinter import filedialog
import mne
import numpy as np
import tkinter as tk
from heartpy import exceptions
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os


root = tk.Tk()
root.withdraw()

filepath = filedialog.askopenfilename(filetypes=[("set file","*.set")])
data=mne.io.read_raw_eeglab(filepath,preload=True)

ecg=data.pick_channels(["ECG"])
#epochs=mne.make_fixed_length_epochs(ecg,duration=epoch_size,overlap=epoch_size/2)

ecg_arr=ecg.get_data()
ecg_arr=np.transpose(ecg_arr)
ecg_arr=ecg_arr.flatten()

wd, m = hp.process_segmentwise(ecg_arr, sample_rate=300, segment_width=10, segment_overlap=0.5)


filepath2 = filedialog.askopenfilename(filetypes=[("set file","*.set")])
data2=mne.io.read_raw_eeglab(filepath2,preload=True)

ecg2=data2.pick_channels(["ECG"])
#epochs=mne.make_fixed_length_epochs(ecg,duration=epoch_size,overlap=epoch_size/2)

ecg_arr2=ecg2.get_data()
ecg_arr2=np.transpose(ecg_arr2)
ecg_arr2=ecg_arr2.flatten()

wd2, m2 = hp.process_segmentwise(ecg_arr2, sample_rate=300, segment_width=10, segment_overlap=0.5)

import matplotlib.pyplot as plt

feature="bpm"

toplot=m[feature]
toplot2=m2[feature]

plt.plot(toplot)
plt.show()
plt.plot(toplot2)
plt.show()