#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 13:12:23 2021

@author: alexesmerritt
"""

import pandas as pd
file = open('/Users/alexesmerritt/Desktop/Prison Vaccinaiton Project/all_states.csv')
empty_column =[]
all_states = pd.read_csv(file)
columns = all_states.columns
for column in columns :
    if len(all_states[column].unique())==1:
        empty_column.append(column)
        
print (len(empty_column))
#rename column to match master doc stcountyfp
## format zip codes in the same way as the master doc

 ##Import master docs
##Master_doc = open('ZIP-COUNTY-FIPS_2010-03.csv')
##df_2 =pd.read_csv(Master_doc)
## Clean up zipcodes so that 
#def add_FIPS(all_states):
   ## df_new = all_states.merge(df_2, left_on=[],right_on[] how='left')
   ## return df_new.to_csv('updated_all_states.csv')
##add_FIPS(all_states)
##print(len(all_states['stateagency'].unique()))
##print((all_states['stateagency'].unique()))
    ##only 16s states
##print(len(all_states['fac_zip'].unique()))
##Confirm prisons that the CPP has and see if its about 289
##there may need to be some correct for split zip codes
    #see what the assumption
    
    ## pairing down the file 
    