#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://python-pytube.readthedocs.io/en/latest/

"""
from selenium import webdriver
from pytube import YouTube
import os
import time

def Drive(link):
    dr = os.getcwd()
    driver = webdriver.Chrome(dr + "/" + "chromedriver")
    driver.get(link)
    
    wait_time = 2
    scrolls = 60
    amount = 1080
    refList = []
    
    for i in range(scrolls):
        amount = amount + 1080
        command = "window.scrollTo(0," + str(amount) + ");"
        driver.execute_script(command)
        time.sleep(wait_time)
        
    data = ""
    
    titles = driver.find_elements_by_id("video-title")
    try:
        for i in titles:
            ref = i.get_attribute("href")
            title = i.get_attribute("title")
            print(title + " = " + ref)
            if ref not in refList:
                refList.append(ref)
                data = data + str(title) + "|||" + str(ref) + "\n"
    except:
        print("nope")
    #wd.quit()
        
    with open("linkname.txt","w+") as file:
        file.write(data)


def Download(links):
    with open(links,"r") as file:
        links = file.read()
        seq = links.split("\n")
    
    dr = os.getcwd() + "/output"
    _id = 0
    print("Total videos: " + str(len(seq)))
    
    for i in seq:
        url = i.split("|||")[1]
        video_name = i.split("|||")[0] + "_" + str(_id)
        _id+=1
        print(url)
        while True:
            try:
                video = YouTube(url)
                if int(video.length) < 600 and int(video.length) > 60:
                    print("Length: " + str(video.length/60) + " minutes")
                    stream = video.streams
                    audio_stream = stream.filter(only_audio=True)
                    audio_stream[0].download(dr, video_name)
                    print("Downloaded: " + video_name)
                    print("URL: " + url)
                    print(str(_id) + "/" + str(len(seq)))
                    print("--------------------")
                else:
                    print("Length: " + str(video.length/60) + " minutes")
                    print("Video " + video_name + " is too long or too short (1 min. < t < 10min.). Won't download.")

                break
            except:
                print("Error.")
                #time.sleep(2)
                        
    print("\nDone.")  
    
#Drive("https://www.youtube.com/user/KannibalenRecords/videos") #Kannibalen Records
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

Download("current.txt")


