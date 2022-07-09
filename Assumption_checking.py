#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 15:25:21 2021

@author: alexesmerritt
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
os.chdir('/Volumes/GoogleDrive-115595450988993348370/.shortcut-targets-by-id/1LAfieGjgpLHN5FpEjgPlbLnLeRr0nfT6/Alexes_Bansal_Lab/Prison Vaccinaiton Project/vac-states')
Groupings3 = [('AK.csv','fac_inc_partiallyvaccinated','Alakasa'),
             ('AL.csv','fac_inc_vaccinated','Alabama'),
             ('AZ.csv','sum_inc_vaccinations','Arizona'),
             ('CA.csv','fac_inc_partiallyvaccinated','California'),
             ('CO.csv','sum_inc_vaccinated','Colorado'),
             ('CT.csv','sum_inc_vaccinated','Connecticut'),
             ('DE.csv','sum_inc_vaccinations_dose1','Deleware'),
             ('GA.csv', 'fac_inc_vaccinated','Georgia'),
             ('ID.csv','facility_inc_partiallyvaccinated', 'Idaho'),
             ('KS.csv','fac_inc_vaccinated','Kansas'),
             ('MN.csv','fac_inc_partiallyvaccinated','Minnesota'),
             ('MA.csv','sum_inc_partiallyvaccinated','Massachusetts'),
             ('NC.csv','sum_inc_partiallyvaccinated','North Carolina'),
             ('NH.csv','fac_inc_phase1bpartvac','New Hampshire'),
             ('NJ.csv','sum_inc_vaccinedoses','New Jersey'),
             ('PA.csv','sum_inc_vaccinated_dose1','Pennsylvania'),
             ('TN.csv','sum_inc_vaccinated','Tennesee'),
             ('UT.csv','sum_inc_vaccinated','Utah'),
             ('VA.csv','sum_inc_vaccinated','Virginia'),
             ('WI.csv','fac_inc_partiallyvaccinated','Wisconsin'),
             ('WV.csv','facilties_inc_vaccinated','West Virginia'),
             ('WA.csv','sum_vaccinated_seconddose', 'Washington'),
             ('WA.csv','sum_vaccinated_seconddose', 'Washington')]
Groupings= [('MN.csv','fac_inc_jjvaccine','Minnessota')]
            #('MN.csv','fac_inc_partiallyvaccinated','Minnessota'),
            #('MN.csv','fac_inc_fullyvaccinated','Minnessota')]
#Groupings2 = [('MA.csv','sum_vaccinated_firstdose','Massachusetts')]
#States using scrape data

for (filing, column , state) in Groupings:
    file = open(filing)
    df=pd.read_csv(file, na_values=['NR'])
    df['scrapedate'] = pd.to_datetime(df.scrapedate, format='%Y-%m-%d')
    fig,ax = plt.subplots(figsize = (10,10))
    df.groupby("facility").plot(x='scrapedate', y=column,legend=None, ax=ax);
    plt.xlabel('Date')
    plt.ylabel('Partial Vaccination')
    plt.title(state+', '+column)
    savefig = '/Volumes/GoogleDrive-115595450988993348370/.shortcut-targets-by-id/1LAfieGjgpLHN5FpEjgPlbLnLeRr0nfT6/Alexes_Bansal_Lab/Prison Vaccinaiton Project/Assumptions/'+state+'_assump_test.jpg'
    plt.savefig(savefig)
#States using lastupdated
