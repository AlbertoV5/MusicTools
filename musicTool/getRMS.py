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
    frameLength = 2048
    
    num_of_frames = songLength // frameLength
    
    print("Song Length Frames:", num_of_frames)
    print("Offset", offset/song.sampfreq)
    
    # List Comprehension of all the rms for all the frames in the song
    rmsArray = np.array([onset.GetRMS(song.data[(offset + (frame*frameLength)):(offset + (frame * frameLength) + frameLength)]) 
                        for frame in range(num_of_frames)])
    
    # Interpolation of array in order to compare
    interpolationRatio = num_of_frames/128
    interpolatedArray = np.interp(np.arange(0, len(rmsArray), interpolationRatio), np.arange(0, len(rmsArray)), rmsArray)
    # RMS for all the samples
    rmsTotal = onset.GetRMS(song.data)

    # RMS min max for the interpolated array
    rmsAvg = np.average(interpolatedArray)
    rmsMin = np.min(interpolatedArray)
    rmsMax = np.max(interpolatedArray)
    
    print("RMS AVG:", rmsAvg, "RMS Total:", rmsTotal)
    print("Song Length (seconds):", song.length/song.sampfreq)
    
    plt.ylim((-48,0))
    plt.figure(figsize = (10,5))
    plt.plot(interpolatedArray)
    
    
for file in input_path.glob('**/*.wav'):
    print("--------------------")
    print(file.stem)
    ReadSong(str(file))
