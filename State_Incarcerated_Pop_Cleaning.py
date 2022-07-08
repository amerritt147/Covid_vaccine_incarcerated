#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 13:15:22 2022

@author: alexesmerritt
"""
import pandas as pd
import numpy as np
##___this data set puts state name in columns 'name'

##State decarceration data from the  marshall project
file = open('DATA/Original/prison_populations.csv') ##data from PPP
df=pd.read_csv(file, low_memory = False, encoding= 'unicode_escape',na_values='NR')
##Creating and cleaning columns thatrelate to date
df['Date'] = pd.to_datetime(df.as_of_date, format='%m/%d/%Y') 
df['month']=pd.DatetimeIndex(df['Date']).month
df['year']=pd.DatetimeIndex(df['Date']).year
df=df.drop(['as_of_date'],axis=1)

##Using loop to add nan values for months that do not have population data
months=list(range(1,12))
years=[2020,2021,2022]
states=list(df['name'].unique())

for state in states:
    for year in years:
        for month in months: 
            df_match=df.loc[(df['name']==state)&(df['month']==month)&(df['year']==year)]
            if len(df_match.index)==0: 
                data=[state, np.nan, month, np.nan, np.nan, year]
                df_extra=pd.DataFrame([data],columns=['name', 'abbreviation', 'month', 'pop', 'Date', 'year'])
                df=pd.concat([df_extra,df],ignore_index=True)


df=df[~(df['Date'] < '2020-03-01')] ##removing population data from before March 2020. 

##CONSIDERING MACRCH 2020 (or the first available data point after march 2020) THE INITIAL POPULATION AND CALCULATING THE CHANGE IN POPULATION FROM THAT POINT MONTHLY
df_new=pd.DataFrame()
for state in df['name'].unique(): 
    df_state=df.loc[df['name']==state]
    df_state=df_state.sort_values("Date")
    df_state=df_state.reset_index()
    mar2020=df_state['pop'][0] 
    df_state['pop_change']=(df_state['pop']-mar2020)/mar2020
    df_new=pd.concat([df_state,df_new],ignore_index=True)


##Find states that saw an incarcerated population decrease of 20% or more
df_20=df_new.loc[df_new['pop_change']<-0.2]
decarceration_states=df_20['name'].unique()
allstates=df_new['name'].unique()

df_new.to_csv('Data/Cleaned/state_pops.csv')
