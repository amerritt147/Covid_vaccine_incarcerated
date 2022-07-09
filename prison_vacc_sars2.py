#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:04:30 2021

@author: alexesmerritt
"""
### Goal:combine the files and include a new coloumn that addresses the original file name

import pandas as pd
import os


folder = '/Users/alexesmerritt/Desktop/Prison Vaccinaiton Project/vac-states/'
files = []
for file in os.listdir(folder):
    if file.endswith('.csv'):
        files.append(folder+file)
print(files)

all_states = pd.DataFrame()
for filed in files: 
    df = pd.read_csv(filed,  low_memory=False)
    df["state"] = filed ## Double check what states actually need state 
    all_states=pd.concat([all_states, df])
    
all_states.to_csv('all_states.csv')
#


## Get pop data on the same file