#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: albertovaldezquinto
"""

import pandas as pd
from pathlib import Path
import onset
import matplotlib.pyplot as plt
import numpy as np

dr = Path.cwd()
input_path, output_path = dr / "input", dr / "output"

def ReadSong(filePath):
    song = onset.Song(filePath)
    firstPart = song.data[0:int(song.sampfreq*10)]
        
    threshold = np.average(np.absolute(firstPart)) * 2
    
    offset = np.where(song.data > threshold)[0][0]
    
    songLength = song.data.shape[0] - offset
    frameLength = int(1 * song.sampfreq)
    
    num_of_frames = songLength // frameLength
    
    rmsList = []
    print("Song Length Frames:", num_of_frames)
    print("Offset", offset/song.sampfreq)
    
    for frame in range(num_of_frames):
        start = offset + (frame * frameLength)
        end = start + frameLength
        
        rmsList.append(onset.GetRMS(song.data[start:end]))

    ratio = num_of_frames/100
    
    a = np.array(rmsList)
    b = np.interp(np.arange(0, len(a), ratio), np.arange(0, len(a)), a)
    rmsAvg = np.average(b)
    
    rmsTotal = onset.GetRMS(song.data)
    rmsMin = np.min(b)
    print("RMS AVG:", rmsAvg, "RMS Total:", rmsTotal)
    plt.plot(b)
    
    
for file in input_path.glob('**/*.wav'):
    print("--------------------")
    print(file.stem)
    ReadSong(str(file))
