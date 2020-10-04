#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Only .wav 16 bits for now.

@author: albertovaldezquinto
"""

import pandas as pd
from pathlib import Path
import onset
import matplotlib.pyplot as plt
import numpy as np

dr = Path.cwd()
input_path, output_path = dr / "input", dr / "output"

def Format(line):
    return format(line, ".4f")

def Round(value):
    return int(value*(10**4))/(10**4)

def ReadSong(filePath, title):
    # Read waveform to numpy array
    song = onset.Song(filePath)
    baseLength = song.length / song.sampfreq
    firstPart = song.data[0:int(song.sampfreq*10)]
    
    # Get Song Offset
    threshold = np.average(np.absolute(firstPart)) * 2
    offset = np.where(song.data > threshold)[0][0]
    offsetSeconds = offset / song.sampfreq
    
    # Get frame information
    songLength = song.data.shape[0] - offset
    frameLength = 2048
    num_of_frames = songLength // frameLength
        
    # List Comprehension of all the rms for all the frames in the song
    rmsArray = np.array([onset.GetRMS(song.data[(offset + (frame*frameLength)):(offset + (frame * frameLength) + frameLength)]) 
                        for frame in range(num_of_frames)])
    
    # Get Song End, endset as the last frame where rms > gateThreshold
    gateThreshold = -72
    try:
        endFrame = np.where(rmsArray < gateThreshold)[0][0]
        rmsArray = rmsArray[:endFrame]
        endset = endFrame * frameLength
    except:
        endset = songLength
    endsetSeconds = endset / song.sampfreq

    # Interpolation of array in order to compare
    interpolationLength = 128
    interpolationRatio = num_of_frames/interpolationLength
    interpolatedArray = np.interp(np.arange(0, len(rmsArray), interpolationRatio), np.arange(0, len(rmsArray)), rmsArray)

    # RMS Values, total and interpolated
    rmsTotal = onset.GetRMS(song.data)
    rmsAvg = np.average(interpolatedArray)
    rmsMin, rmsMax = Round(np.min(interpolatedArray)), Round(np.max(interpolatedArray))
    rmsMinPos, rmsMaxPos = np.argmin(interpolatedArray), np.argmax(interpolatedArray)
        
    # Plot
    fig, ax = plt.subplots()
    plt.grid(True)
    ax.plot(interpolatedArray)
    ax.scatter(rmsMinPos, rmsMin, c = "Green", marker = "X")
    ax.scatter(rmsMaxPos, rmsMax, c = "Red", marker = "X")
    
    # Save Dictionary
    data = {"Title":[title], "RMS Mean (dB)": [Round(rmsAvg)], "RMS Total (dB)": [Round(rmsTotal)], 
            "RMS Min (dB)": [(Round(rmsMinPos), Round(rmsMin))], "RMS Max (dB)": [(Round(rmsMaxPos), Round(rmsMax))],
            "Offset (sec)": [Round(offsetSeconds)], "Endset (sec)": [Round(endsetSeconds)],
            "Base Length (sec)": [Round(baseLength)]}
    
    # Print out
    for parameter in data.keys():
        print(parameter, ":", data[parameter][0]) 
    print("--------------------\n")
    
    df = pd.DataFrame(data)
    df.to_csv('songs.csv', mode='a', header=False, index = False)

    

def ReadAllSongs():
    dictionary = {"Title":[], "RMS Mean (dB)": [], "RMS Total (dB)": [], 
                  "RMS Min (dB)": [], "RMS Max (dB)": [], "Offset (sec)": [], 
                  "Endset (sec)": [], "Length (sec)": []}

    df = pd.DataFrame(dictionary)
    df.to_csv('songs.csv', index = False)
    
    for file in wavFileList:
        ReadSong(str(input_path / (file + '.wav')), file)


wavFileList = [file.stem for file in input_path.glob('**/*.wav')]

ReadAllSongs()







