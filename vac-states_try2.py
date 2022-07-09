#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 22:04:25 2021

@author: alexesmerritt
"""

import pandas as pd
import glob

files = glob.glob('./*')

# create empty df for all states data
df_allstates= pd.DataFrame()

for file in files:
    
    # read in each state file and grab all column names
    df = pd.read_csv(file, low_memory = False)
    column_names = df.columns
    
    # get smaller list of column names that have the word 'vacc' in it
    column_names_vacc = [col for col in column_names if 'vacc' in col]
    
    # other columns names to grab (we can add more to this later)
    other_cols = ['scrapedate', 'lastupdated', 'stateagency', 'facility']
    
    # read in each file again but only grab the vacc columns and other columns
    df = pd.read_csv(file, usecols = other_cols + column_names_vacc)
    
    print(df.columns)
    
    # concatenate data into one dataframe 
    # (will have NaNs for the columns where that state doesn't have data)
    df_allstates = pd.concat([df_allstates, df], axis=0, ignore_index=True)

# output to file
df_allstates.to_csv("../allstates.csv")