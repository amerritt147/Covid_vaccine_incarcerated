#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 15:31:33 2022

@author: alexesmerritt
"""

import pandas as pd
file = open('/Users/alexesmerritt/Desktop/UCLA DATA/historical_state_jurisdiction_counts.csv')
df = pd.read_csv(file, low_memory = False, encoding= 'unicode_escape',na_values='NR')
print(df.columns)

l3=[]
for col in l3: 
    df=df.drop(col,axis=1)

useful_measures=['Staff.Initiated',
'Residents.Initiated' 'Residents.Tadmin' 'Residents.Completed'
'Residents.Vadmin' 'Staff.Tested' 'Staff.Completed'
'Residents.Initiated.Pct' 'Staff.Initiated.Pct' 'Staff.Vadmin']
