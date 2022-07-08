#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:54:22 2022

@author: alexesmerritt
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
file = open('/Users/alexesmerritt/Desktop/UCLA DATA/historical_facility_counts.csv')
df = pd.read_csv(file, low_memory = False, encoding= 'unicode_escape',na_values='nan')


##Dropping a few irrelevant columns
df=df.drop(['Residents.Confirmed', 'Staff.Confirmed', 'Residents.Deaths','Staff.Deaths', 'Residents.Tested','Residents.Active', 'Staff.Active','Residents.Tadmin'],axis=1)
df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
facility_ids=list(df['Facility.ID'].unique())
states=list(df['State'].unique())
df['County.FIPS'].astype(str)
df=df.dropna(subset=['Residents.Initiated','Residents.Completed'], how='all')
df = df.loc[~((df['Residents.Initiated'] == np.nan) & (df['Residents.Completed'] == np.nan))]




df['Initiated.Coverage']=df['Residents.Initiated']/df['Residents.Population']
df['Completed.Coverage']=df['Residents.Completed']/df['Residents.Population']
df = df.loc[~((df['Initiated.Coverage'] == np.nan) & (df['Completed.Coverage'] == np.nan))]
df = df.loc[~((df['Initiated.Coverage'] == 0) & (df['Completed.Coverage'] == 0))]



df_f=df.loc[df['Jurisdiction']=='federal'] 
df_s=df.loc[df['Jurisdiction']=='state']    

##working with federal data
federal_fac=list(df_f['Facility.ID'].unique())
print(len(federal_fac))
no_ts_popf=[]
for fac in federal_fac:
    df_ffac=df_f.loc[df_f['Facility.ID']==fac]
    res_completed=df_ffac['Residents.Completed'].unique()
    if len(res_completed)==1:
        federal_fac.remove(fac)
    feb20_pop=list(df_ffac['Population.Feb20'].unique())
    res_pop=list(df_ffac['Residents.Population'].unique())
    if len(res_pop)==1: 
        if np.isnan(res_pop[0]):
            no_ts_popf.append(fac)    
fed_w_ts_pop= [item for item in federal_fac if item not in no_ts_popf]       
##working with state data
state_fac=list(df_s['Facility.ID'].unique())
print(len(state_fac))
no_ts_pops=[]
for fac in state_fac:
    df_sfac=df_s.loc[df_s['Facility.ID']==fac]
    res_completed=df_sfac['Residents.Completed'].unique()
    res_initiated=df_sfac['Residents.Initiated'].unique()
    if len(res_completed)==1 & len(res_initiated)==1:
        state_fac.remove(fac)
    feb20_pop=list(df_sfac['Population.Feb20'].unique())
    res_pop=list(df_sfac['Residents.Population'].unique())
    if len(res_pop)==1: 
        if np.isnan(res_pop[0]):
            no_ts_pops.append(fac)
state_w_ts_pop=  [item for item in state_fac if item not in no_ts_pops]           
            
sets=[state_w_ts_pop,fed_w_ts_pop]
for x in sets:
    print(len(x))  
df_states=df_s.loc[df_s['Facility.ID'].isin(state_w_ts_pop)]
df_states["Initiated.Coverage"].mask( df_states["Initiated.Coverage"] > 1, 1 , inplace=True )
df_states["Completed.Coverage"].mask( df_states["Completed.Coverage"] > 1, 1 , inplace=True )
df_feds=df_f.loc[df_f['Facility.ID'].isin(fed_w_ts_pop)]
df_feds["Completed.Coverage"].mask( df_feds["Completed.Coverage"] > 1, 1 , inplace=True )



def make_monotonic(df, cols=None):
    if cols is None:
        cols = df.columns

    df1 = df.copy()[cols]

    while True:
        mon_inc = (df1.diff().fillna(0) >= 0).all(axis=1)
        if mon_inc.all():
            break
        df1 = df1[mon_inc]
    return df1

df_state=pd.DataFrame()
for fac in state_w_ts_pop:
    df_fac=df_states.loc[df_states['Facility.ID']==fac]
    df_fac['Mono.Initiated.Rate']=make_monotonic(df_fac,cols=['Initiated.Coverage'])
    df_fac['Mono.Completed.Rate']=make_monotonic(df_fac,cols=['Completed.Coverage'])      
    df_state=pd.concat([df_fac,df_state])        


df_fed=pd.DataFrame()
for fac in fed_w_ts_pop:
    df_fac=df_feds.loc[df_feds['Facility.ID']==fac]
    df_fac['Mono.Completed.Rate']=make_monotonic(df_fac,cols=['Completed.Coverage'])     
    df_fed=pd.concat([df_fac,df_fed])    
    
    
df_both=pd.concat([df_fed,df_state],ignore_index=True)    

df_both.set_index('Date', inplace=True)
df2=pd.DataFrame()

for fac in df_both['Facility.ID'].unique():
    df_fac=df_both.loc[df_both['Facility.ID']==fac]    
    df_fac=df_fac.sort_values("Date")
    df_fac=df_fac.reset_index()
    
    start_date=df_fac['Date'][0]
    df_fac['Days']=(df_fac['Date']-start_date).dt.days
    df_fac['Days']= pd.to_numeric(df_fac['Days'])
    df_fac['Days_since_last']=df_fac['Days']-df_fac['Days'].shift(1)
    df2=pd.concat([df_fac,df2],ignore_index=True)
    
    
    
    
    