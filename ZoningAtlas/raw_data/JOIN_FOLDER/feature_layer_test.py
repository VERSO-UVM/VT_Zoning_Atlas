import os
import pandas as pd
import geopandas as gpd
import numpy as np

planning_layer = gpd.read_file('final_consolidated_layers/VTPlanningAtlas_zoned_jxtns_071824.geoJSON', driver = 'GeoJSON')

for county in sorted(planning_layer['COUNTY'].unique()):
    print(county)
    df = planning_layer.loc[planning_layer['COUNTY'] == county]
    df = df.groupby('JXTN')
    for x in sorted(df['JXTN']):
        print(x)

print(len(planning_layer))

print(len(planning_layer['JXTN'].unique()))

print(planning_layer['1FDP'].unique())

print(planning_layer['COUNTY'].unique())