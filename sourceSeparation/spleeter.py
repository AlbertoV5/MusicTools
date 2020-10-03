# -*- coding: utf-8 -*-
"""
Source Separation

First time run it will download the 4 stems model

Replace spaces with underscores for the song names on input

Works on macOS
"""
import os
from pathlib import Path

input_path = Path.cwd() / "input"

files = []
for file in os.listdir(input_path):
    if "mp3" in file or "wav" in file:
        files.append(input_path / file)

files.sort()

os.system("cd " + str(Path.cwd()))

for i in range(len(files)):
    os.system("spleeter separate -i" + str(files[i]) + " -o output -p spleeter:4stems")

