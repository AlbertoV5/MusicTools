#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP3 to WAV source separation using Spleeter

@author: albertovaldezquinto
"""
from spleeter.separator import Separator
from pathlib import Path


dr = Path.cwd()
input_path, output_path = dr / "input", dr / "output"

def Spleet():
    
    separator = Separator('spleeter:4stems')

    for file_path in input_path.glob('**/*.mp3'):
        separator.separate_to_file(file_path, output_path)    


Spleet()