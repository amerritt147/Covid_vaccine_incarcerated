#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 14:27:48 2022

@author: alexesmerritt
"""

import pandas as pd
import numpy as np

file = open('Data/historical_state_counts.csv')
df_UCLA = pd.read_csv(file, low_memory = False, encoding= 'unicode_escape',na_values='NR')

df_UCLA['Date'] = pd.to_datetime(df_UCLA.Date, format='%Y-%m-%d')

l3=['Residents.Confirmed', 'Staff.Confirmed',
       'Residents.Deaths', 'Staff.Deaths', 'Residents.Tadmin',
       'Residents.Tested', 'Residents.Active', 'Staff.Active','Staff.Initiated','Staff.Initiated.Pct', 'Residents.Completed', 'Staff.Completed',
       'Residents.Completed.Pct', 'Residents.Vadmin', 'Staff.Vadmin','Residents.Initiated.Pct']
for col in l3: 
    df_UCLA=df_UCLA.drop(col,axis=1)   
df_UCLA=df_UCLA.dropna(axis=0,subset=['Residents.Initiated'])
df_UCLA['Month']=pd.DatetimeIndex(df_UCLA['Date']).month
df_UCLA['Year']=pd.DatetimeIndex(df_UCLA['Date']).year









df_UCLA['ts_pop']=''
state_month_year=[]
df_UCLA_p=pd.DataFrame()
file_ts_pop=open('Data/Cleaned/state_pops.csv')
df_ts_pop=pd.read_csv(file_ts_pop)

UCLA_states=list(df_UCLA['State'].unique())
ts_states=list(df_ts_pop['name'].unique())
add_states=[item for item in UCLA_states if item not in ts_states]
months=list(range(1,12))



for row in range(0,len(df_ts_pop)):
    state=df_ts_pop['name'][row]
    month=df_ts_pop['month'][row]
    year=df_ts_pop['year'][row]
    pop=df_ts_pop['pop'][row]
    state_month_year.append([state,month,year,pop])

for (state,month,year,pop) in state_month_year:
    df_date=df_UCLA.loc[(df_UCLA['State']==state)&(df_UCLA['Month']==month)&(df_UCLA['Year']==year)]
    df_date['ts_pop']=pop
    df_UCLA_p=pd.concat([df_date,df_UCLA_p],ignore_index=True)



df_UCLA=df_UCLA_p








file2=open('Data/state_aggregate_denominators.csv')
df_denom=pd.read_csv(file2)

pop_pairs=[]
for row in range(0,52):
    pop_pairs.append((df_denom['State'][row],df_denom['Residents.Population'][row]))

df_UCLA['Population_Dec2021']=""
df_UCLA2=pd.DataFrame()
for (state,pop) in pop_pairs:
    df_state=df_UCLA.loc[df_UCLA['State']==state]
    df_state['Population_Dec2021']=pop
    df_UCLA2=pd.concat([df_UCLA2,df_state],ignore_index=True)
df_UCLA=df_UCLA2
df_UCLA['Residents.Initiated.Rate']=df_UCLA['Residents.Initiated']/df_UCLA['Population_Dec2021']


df_UCLA_new=df_UCLA


file_grouping=open('/Users/alexesmerritt/Downloads/State groupings - Sheet1.csv')
df_groupings=pd.read_csv(file_grouping)
df_groupings.drop('UCLA notes', axis=1, inplace=True)
df_groupings.drop('Matches with CPP', axis=1, inplace=True)
df_UCLA_new['Prioritization?']=""
df_UCLA_new['Date_prioritized']="" 
df_UCLA_new['Phase_state']="" 
df_4=pd.DataFrame() 
for (state,prioritized,prior_date,phase) in df_groupings.values:
    df_state=df_UCLA_new.loc[df_UCLA_new['State']==state]
    df_state['Prioritization?']=prioritized
    df_state['Date_prioritized']=prior_date
    df_state['Phase_state']=phase
    df_4=pd.concat([df_4,df_state],ignore_index=True)
#df_state['Prioritization?']=[prioritized]*int(df_state.shape[0])    

df=df_4


##Removing the problem dates in Alaska
AK_problem_dates=['2021-04-18', '2021-04-25',
'2021-05-02', '2021-05-09', '2021-05-16', '2021-05-23',
'2021-05-30', '2021-06-06', '2021-06-13']

df_ak=df.loc[df['State']=='Alaska']

df_ak_probs=df_ak.loc[df_ak['Date'].isin(AK_problem_dates)]
df.drop(df_ak_probs.index, axis=0,inplace=True)
##Removing the problem dates in Wisconsin
WI_problem_dates=['2022-01-23']

df_wi=df.loc[df['State']=='Wisconsin']

df_wi_probs=df_wi.loc[df_wi['Date'].isin(WI_problem_dates)]
df.drop(df_wi_probs.index, axis=0,inplace=True)

##Removing Arizona
states=['Alabama', 'Alaska', 'California', 'Colorado',
       'Connecticut', 'Delaware', 'Federal', 'Georgia', 'Idaho', 'Kansas',
       'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
       'Missouri', 'New Hampshire', 'New Jersey', 'North Carolina',
       'North Dakota', 'Ohio', 'Pennsylvania', 'South Carolina',
       'Virginia', 'Washington', 'West Virginia', 'Wisconsin']

df=df.loc[df['State'].isin(states)]

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
state_real_start_zip=[('New Jersey','2020-12-15'),('Arizona','2021-03-05'),('Kansas','2021-01-21'),('Massachusetts','2021-01-21'),('Pennsylvania','2021-04-05')]
df_corrected_date=pd.DataFrame(state_real_start_zip,columns=['State','Start_Date'])
#df_corrected_date['Start_Date']=pd.to_datetime(df_corrected_date.Start_Date, format='%Y-%m-%d')
weird_start_states=list(df_corrected_date['State'].unique())
df['Date_prioritized']=pd.to_datetime(df.Date_prioritized, format='%m/%d/%Y')

df_concat=pd.DataFrame()



for state in df['State'].unique():
    df_state=df.loc[df['State']==state]
    df_state['Mono.Initiated.Rate']=make_monotonic(df_state,cols=['Residents.Initiated.Rate'])

    if state in weird_start_states:
        new_start=list(df_corrected_date.loc[df_corrected_date['State']==state,'Start_Date'])
        cols=df_state.columns
        new_row=[new_start[0], state, np.nan, np.nan,np.nan, np.nan, np.nan,np.nan, np.nan, 0]
        df_state.append(new_row, ignore_index=True)
    print(state)
    
    df_state=df_state.sort_values("Date")
    df_state=df_state.reset_index()
    
    start_date=df_state['Date'][0]
    df_state['Days']=(df_state['Date']-start_date).dt.days
    df_state['Days']= pd.to_numeric(df_state['Days'])
    df_state['Days_since_last']=df_state['Days']-df_state['Days'].shift(1)
    df_state['Days_since_prior']=(df_state['Date']-df_state['Date_prioritized']).dt.days
    
    if state=='Virginia':
        df_state["Mono.Initiated.Rate"].mask( df_state["Mono.Initiated.Rate"] > 1, 1 , inplace=True )
        
    df_concat= pd.concat([df_state,df_concat])
df_final=df_concat












df_final.to_csv('Data/Cleaned/UCLA_statewide_temporal.csv')

df=df_final

df=df.drop('index', axis=1)
pd.set_option('display.max_columns', None)



df_start=df.loc[df['State']=='Arizona']