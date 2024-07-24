import pandas as pd
import os
import geopandas as gpd
import re
import datetime as dt

effectives = pd.DataFrame(columns = ['County', 'Jurisdiction', 'Effective Date'])

for file in os.listdir('../Excel_workbooks'):
    county = file.split('_')[0]
    jxtn = file.split('_')[1]
    try:
        thissheet = pd.read_excel('../Excel_workbooks/' + file, sheet_name='Jurisdiction', engine= 'openpyxl', index_col=0)
        x = thissheet.iloc[-2][0]
        effectives.loc[len(effectives)] = [county, jxtn, x.strftime('%B, %Y')]
    except:
        print('Possibly unzoned: ' + file)

already_done = [(x, y) for x, y in zip(effectives['County'], effectives['Jurisdiction'])]

for file in os.listdir('../NLP_INPUT/zoning_bylaws'):
    try:
        thisfile = file.split('eff')
        effective = thisfile[1][:-4]
        identifier = thisfile[0].split('_')
        county = identifier[0]
        print(county)
        jxtn = ''
        for item in identifier[1:-2]:
            jxtn += item
        print(jxtn)
        if (county, jxtn) not in already_done:
            effectives.loc[len(effectives)] = [county, jxtn, effective]
    except:
        print(file)

effectives.to_csv('effective_dates.csv')
