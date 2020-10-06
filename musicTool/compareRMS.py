#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compare .npy

@author: albertovaldezquinto
"""

from pathlib import Path
import pandas as pd
import numpy as np

dr = Path.cwd()
samplePool_path = dr / "output" / "framesArrays"
output_file = dr / "results.csv"

referenceFile = Path(input("Enter reference .npy:\n").replace("'", ""))
reference = np.load(referenceFile, allow_pickle=True) * -1

# Normalize to 1.0
#reference = reference/np.max(reference)

# Basic Lists
sampleList = [[file.stem, np.load(file, allow_pickle=True)] for file in samplePool_path.glob('**/*.npy')]
print(np.shape(reference))

dotList = [[sample[0] for sample in sampleList],[np.dot(reference, sample[1]) for sample in sampleList]]
# Normalize to 1.0

# Dictionary and DataFrame
dotDict = {"Title":dotList[0], "Score":dotList[1]}
df = pd.DataFrame(dotDict)
df = df.sort_values(by="Score", ascending=False)
df.to_csv(output_file, sep=",")
