#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 17:39:26 2020

@author: albertovaldezquinto
"""

import pandas as pd
from pytube import YouTube
from pathlib import Path

csvFile = "Top of the Week_Month - BeatSaber_All (Weekly).csv"
csv = pd.read_csv(csvFile)
download_path = Path.cwd() / "downloads"

def Get_Genres_Filtered(csv, top = 10, weeks = (0,len(csv))):
    
    genresUnique = csv["Genre"].unique()
    genresFiltered = { i : 0 for i in genresUnique }

    subgenresUnique = csv["Subgenre"].unique()
    subgenresFiltered = { i : 0 for i in subgenresUnique }

    # Process Data    
    for i in range(weeks[0], weeks[1]):
        genre = csv["Genre"][i]
        subgenre = csv["Subgenre"][i]

        if int(csv["Order"][i]) <= top:
            genresFiltered[genre] += 1
            subgenresFiltered[subgenre] += 1
    
    # Sort
    
    genresFiltered = {k: v for k, v in sorted(genresFiltered.items(), key=lambda item: item[1])}
    subgenresFiltered = {k: v for k, v in sorted(subgenresFiltered.items(), key=lambda item: item[1])}
    
    return genresFiltered, subgenresFiltered

def Validate_Youtube(csv, top = 10, weeks = (0,15)):
    brokenLinks = []
    for i in range(weeks[0], int(weeks[1]*20)):
        url = csv["Youtube"][i]
        songName = csv["Song"][i]
        try:
            yt = YouTube(url)
            yt.streams.first()
        except:
            brokenLinks.append([i,songName,url])
            print(i + 1, songName, url, "BROKEN.")
    return brokenLinks

def DownloadYoutube(i, name, url):
    while True:
        try:
            print(str(i).zfill(2), name)
            yt = YouTube(url)
            audio = yt.streams.filter(only_audio=True)[0]
            file = str(i).zfill(3) + "_" + name
            
            if (download_path / (file + ".mp4")).is_file() == False:                
                return audio.download(output_path = download_path, filename = file)
            else:
                return None
        except:
            pass


def DownloadSongs(csv, weeks = (0,len(csv))):
    for i in range(weeks[0], weeks[1]):
        DownloadYoutube(i+1, csv["Song"][i], csv["Youtube"][i])


genF, subF = Get_Genres_Filtered(csv, 20)

#DownloadSongs(csv)

