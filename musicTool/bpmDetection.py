#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads source-separated drums.wav and gives back bpm and note onsets

@author: albertovaldezquinto
"""

import dsp
from pathlib import Path
import pandas as pd
import os
import numpy as np

root = Path.cwd()
input_path, peaks_path, stemName = root / "input", root / "peaks", "drums.wav"

def ReadSongs_GetBPMs():
    bpmList, nameList = [], []
    for i in os.listdir(input_path):
        if ".DS_Store" != i:
            for j in os.listdir(input_path / i):
                if stemName in j:
                    stem, threshold, peaksArray = GetStemData(str(input_path / i / stemName))
    
                    if len(peaksArray) > 4:
                        bpm = GetBPM(stem, peaksArray)
                    else:
                        bpm = CalculateBPM_withBassFFT(stem, threshold)
                    
                    print(i, bpm)
                        
                    bpmList.append(bpm)
                    nameList.append(i)
                    SavePeaksAsNpy(i, peaksArray)
                
    return bpmList, nameList

def GetBPM(stem, peaks, bpmMin = 100, bpmMax = 300):
    d = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)] #Get deltas
    bpm = 60/(dsp.mode(d)/stem.sampfreq) #Convert deltas from sample to seconds to bpm
    
    while bpm < bpmMin or bpm > bpmMax: #Reduce BPM to beat subdivision bpmMin, bpmMax
        if bpm < bpmMin:
            bpm = bpm*2
        elif bpm > bpmMax:
            bpm = bpm/2
    return int(bpm*100)/100

def SavePeaksAsNpy(fileName, peaksArray):
    np.save(str(peaks_path / fileName), np.array(peaksArray), allow_pickle=True)

def GetStemData(path):
    stem = dsp.Song(path) #Read samples
    threshold = stem.CalculateThreshold_RMS() #Calculate RMS Threshold
    indexes = np.where(stem.data > threshold)[0] # Get samples higher than threshold
    peaks = indexes[np.where(np.diff(indexes) > 2048)[0] + 1]

    return stem, threshold, peaks

def CalculateBPM_withBassFFT(stem, threshold):
    bpms, peaks = dsp.GetBPMS(stem, threshold, 120) #Uses 120 Hz as High Cut
    bpm = bpms[0][1] + 0.0069 # Adding 0.0069 as a label for FFT-calculated bpms
    return bpm


bpmList, nameList = ReadSongs_GetBPMs()
df = pd.DataFrame({"Song Name": nameList, "BPM List": bpmList})
df.to_csv(str(root/"bpms.csv"))
