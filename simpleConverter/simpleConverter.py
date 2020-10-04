#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 23:48:06 2020

@author: albertovaldezquinto
"""

from pathlib import Path
from pydub import AudioSegment

input_path, output_path = Path.cwd() / "input", Path.cwd() / "output"

for file in input_path.glob('**/*.mp4'):
    print(file)
    AudioSegment.from_file(file).export(file.split(".")[0] + ".mp3", format='mp3')
