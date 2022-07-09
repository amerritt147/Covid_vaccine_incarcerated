#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:57:29 2021

@author: alexesmerritt
"""
import pandas as pd


BoP_w_fips = open('BoP_w_fips.csv')
BoP_w_fip = pd.read_csv(BoP_w_fips)
df_bop = pd.DataFrame(BoP_w_fips)

pd.read_csv ('clustering1_8_24_21.gis.txt').to_csv ('clusters.csv', index=0)
cluster =open('clusters.csv')
clusters = pd.read_csv(cluster)
dfmain=pd.DataFrame(clusters)
print(dfmain.head(-6))
cluster_counties=dfmain.[dfmain.LOC_ID].unique()
print(cluster_counties)

prop_black_issue = dfmain2[(dfmain2.prop_black<10)&(dfmain2.Black_Disparity>7)]
pbi_list=prop_black_issue.COUNTY.unique()


df_overlap = df_bop[df_bop.fips.isin(cluster_counties)]
print (df_overlap)