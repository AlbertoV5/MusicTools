#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uses selenium to go through the youtube channels and pytube to download data

"""
from selenium import webdriver
from pytube import YouTube
from pathlib import Path
import time
import pandas as pd

dr = Path.cwd()
input_path, output_path = dr / "input", dr / "output"
downloadedList = []

''' SCRAPING FUNCTIONS '''

def ScrollToTheBottom(driver, scrolls = 60, scrollDistance = 1080):
    scrollPosition = scrollDistance
    for i in range(scrolls):
        scrollPosition += scrollDistance
        command = "window.scrollTo(0," + str(scrollPosition) + ");"
        driver.execute_script(command)
        time.sleep(2)

def FetchAllVideos(driver):
    titleList, urlList = [],[]
    
    titles = driver.find_elements_by_id("video-title")
    
    for i in titles:
        url = i.get_attribute("href")
        title = i.get_attribute("title").replace(",","")     
        
        if url not in urlList:
            titleList.append(title)
            urlList.append(url)

    return pd.DataFrame({"Title":titleList, "Url":urlList})

def Drive(channelurl):
    channelName = channelurl.split("/")[-2]
    
    if input_path / (channelName + ".csv") not in input_path.glob('**/*.csv'):
        driver = webdriver.Chrome(dr / "chromedriver")
        driver.get(channelurl)
        
        ScrollToTheBottom(driver, 60)
        
        videos = FetchAllVideos(driver)
        videos.to_csv(input_path / (channelName + ".csv"), sep=",", index = True)

    
''' DOWNLOADING FUNCTIONS '''

def SaveDownloaded(downloadedList, channelName):
    df = pd.DataFrame({"Title":[i[0] for i in downloadedList], "Status":[i[1] for i in downloadedList], "Url":[i[2] for i in downloadedList]})
    df.to_csv(output_path / (channelName + ".csv"), sep=",", index = True)

def DownloadAudio(i, csv, output, minDuration = 60, maxDuration = 600):
    while True:
        try:
            url = csv["Url"][i]
            yt = YouTube(url)
            video_title = csv["Title"][i]
            
            if yt.length < maxDuration and yt.length > minDuration: #lenght in seconds, 1 min to 10 min
                print(i, "Downloaded:", video_title)
                yt.streams.filter(only_audio=True)[0].download(output, video_title)
                downloadedList.append([video_title, "Downloaded", url])
            else:
                print(i, "Not Downloaded:", video_title + " is too long or too short", yt.length/60, "minutes long.")
                downloadedList.append([video_title, "Not Downloaded", url])

            print("--------------------")
            return True
        except:
            print("Pytube error. Re-trying...")
            
        

def DownloadAll():
    for csvFile in input_path.glob('**/*.csv'):
        channelName = csvFile.stem
        csv = pd.read_csv(csvFile)
        print(channelName, "total videos: " + str(len(csv["Title"])))

        for i in range(len(csv["Title"])):
            DownloadAudio(i, csv, output_path / channelName, 60, 600)
        
        SaveDownloaded(downloadedList, channelName)
        
    print("\nDone.")  
    
#Drive("https://www.youtube.com/channel/UCl8iwAEa4i5LsFMXbiI2J-g/videos") #Ninety9Lives
#Drive("https://www.youtube.com/channel/UCan3YouC9b0wi1XNm5v-10w/videos") #Fixt Neon
#Drive("https://www.youtube.com/user/MonstercatMedia/videos") #Monstercat uncaged
#Drive("https://www.youtube.com/user/MrGbullet/videos") #Japan Step
#Drive("https://www.youtube.com/user/DESTINY681/videos") #J-CORE
#Drive("https://www.youtube.com/user/Fixtmusic/videos") #FIXT
#Drive("https://www.youtube.com/channel/UCUVCey_IfNryc9wDiZd3I3w/videos") #RhythmGameMusic
#Drive("https://www.youtube.com/user/Liquicity/videos") #Liquicity
#Drive("https://www.youtube.com/user/djzardonic/videos?view=0&sort=dd&shelf_id=0") #Zardonic
#Drive("https://www.youtube.com/user/UKFDrumandBass/videos") #UKF DnB
#Drive("https://www.youtube.com/channel/UCSPmWM7k8LGyYUYZP8hX1MA/videos") #Dubstep uNk
#Drive("https://www.youtube.com/user/FunkyyPanda/videos") #FunkyPanda
#Drive("https://www.youtube.com/channel/UCSNHkzchuSim4nDdQf3jcvA/videos") #Community released mixes
#Drive("https://www.youtube.com/c/NoCopyrightSounds/videos")

Drive("https://www.youtube.com/user/KannibalenRecords/videos")

DownloadAll()


