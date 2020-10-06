#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Only .wav 16 bits for now.

@author: albertovaldezquinto
"""

import pandas as pd
from pathlib import Path
import dsp
import matplotlib.pyplot as plt
import numpy as np

dr = Path.cwd()

input_path, output_path = dr / "input", dr / "output"
framesArray_path, plot_path = output_path / "framesArrays", output_path / "plots"

def CreateDirectories():
    if not Path.is_dir(output_path):
        Path.mkdir(output_path)
    if not Path.is_dir(input_path):
        Path.mkdir(input_path)
    if not Path.is_dir(framesArray_path):
        Path.mkdir(framesArray_path)
    if not Path.is_dir(plot_path):
        Path.mkdir(plot_path)
        
def Format(line):
    return format(line, ".4f")

def Round(value):
    return int(value*(10**4))/(10**4)

def PlotRMS(interpolatedArray, rmsMinPos, rmsMin, rmsMaxPos, rmsMax, title, interpolationLength):
    fig, ax = plt.subplots()
    plt.grid(True)
    ax.plot(interpolatedArray)
    ax.set_ylim((-60,0))
    ax.set_xlim((-6,interpolationLength))
    ax.scatter(rmsMinPos, rmsMin, c = "Green", marker = "X")
    ax.scatter(rmsMaxPos, rmsMax, c = "Red", marker = "X")
    ax.set_title(title)
    fig.savefig(plot_path / (title + ".png"))
    plt.close(fig)
    
    
def ReadSong(filePath, title):
    # Read waveform to numpy array
    song = dsp.Song(filePath)
    firstPart = song.data[0:int(song.sampfreq*10)]
    
    # Get Song Offset
    threshold = np.average(np.absolute(firstPart)) * 2
    offset = np.where(song.data > threshold)[0][0]
    offsetSeconds = offset / song.sampfreq
    
    # Prepare values for frames
    song.data = song.data[offset:]
    songLength = song.data.shape[0]
    frameLength = 2048
    num_of_frames = songLength // frameLength
    
    # List Comprehension for all the frames in the song, get RMS
    rmsArray = np.array([dsp.GetRMS_dB(song.data[(frame*frameLength):((frame * frameLength) + frameLength)]) 
                        for frame in range(num_of_frames)])
    
    # Prepare values for finding quiet frames / silence
    gateThreshold = -72
    gateHoldLength = 20
    
    # Find all frames with low rms (silence), find all the indexes where silence is longer than X frames and grab the last occurence
    try:
        quietFrames = np.where(rmsArray < gateThreshold)
        splitIndexes = np.where(np.diff(quietFrames) > gateHoldLength)[0] + 1
        endFrame = np.split(quietFrames, splitIndexes)[-1][0]    
        endset = endFrame * frameLength
        # Only use data before endFrame
        rmsArray = rmsArray[:endFrame]
    except:
        endset = songLength
    endsetSeconds = endset / song.sampfreq

    # Prepare values for interpolation
    interpolationLength = 128
    interpolationRatio = num_of_frames/interpolationLength
    
    # Interpolation of array in order to compare
    interpolatedArray = np.interp(np.arange(0, len(rmsArray), interpolationRatio), np.arange(0, len(rmsArray)), rmsArray)

    # RMS Values, total and interpolated
    rmsTotal = dsp.GetRMS_dB(song.data[offset:endset])
    rmsAvg = np.average(interpolatedArray)
    rmsMin, rmsMax = Round(np.min(interpolatedArray)), Round(np.max(interpolatedArray))
    rmsMinPos, rmsMaxPos = np.argmin(interpolatedArray), np.argmax(interpolatedArray)
        
    # Plot
    PlotRMS(interpolatedArray, rmsMinPos, rmsMin, rmsMaxPos, rmsMax, title, interpolationLength)
    # Save numpy array of rms frames
    np.save(str(framesArray_path / (title + ".npy")), interpolatedArray, allow_pickle=True)
    
    # Save Dictionary
    dictionary = {"Title":[title], "RMS Mean (dB)": [Round(rmsAvg)], "RMS Total (dB)": [Round(rmsTotal)], 
            "RMS Min (dB)": [(Round(rmsMinPos), Round(rmsMin))], "RMS Max (dB)": [(Round(rmsMaxPos), Round(rmsMax))],
            "Offset (sec)": [Round(offsetSeconds)], "Endset (sec)": [Round(endsetSeconds)],
            "Length (sec)": [Round((endset-offset)/song.sampfreq)]}
    
    # Print out
    for parameter in dictionary.keys():
        print(parameter, ":", dictionary[parameter][0]) 
    print("--------------------\n")
    
    df = pd.DataFrame(dictionary)
    df.to_csv(output_path / '_data.csv', mode='a', header=False, index = False)


def ReadAllSongs():
    dictionary = {"Title":[], "RMS Mean (dB)": [], "RMS Total (dB)": [], 
                  "RMS Min (dB)": [], "RMS Max (dB)": [], "Offset (sec)": [], 
                  "Endset (sec)": [], "Length (sec)": []}

    df = pd.DataFrame(dictionary)
    df.to_csv(output_path / '_data.csv', index = False)
    
    for file in wavFileList:
        ReadSong(str(input_path / (file + '.wav')), file)


wavFileList = [file.stem for file in input_path.glob('**/*.wav')]

CreateDirectories()
ReadAllSongs()




