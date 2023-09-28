## IMPORTS

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import geopandas as gpd
import warnings # To suppress warning displays in console output


## FUNCTION DECLARATION

def consolidate_data(folder, gis_or_zoning): # gis_or_zoning is a string variable with value of either 'gis' or 'zoning'
    counter = 0
    base_dir = os.path.join(os.getcwd(), folder)
    for gjson in os.listdir(base_dir):
        thisfile = gjson
        if thisfile !='.DS_Store':
            f = os.path.join(base_dir, thisfile)
            with open(f, 'r') as filename:
                if gis_or_zoning == 'gis':
                    this_jxtn = load_gis(f)
                else:
                    if gis_or_zoning == 'zoning':
                        this_jxtn = load_zoning(filename)
                    else:
                        print('Need to specify type of dataframe')
                        return(-1)
                if counter == 0:
                    all_VT_zoning = this_jxtn
                    counter = 1
                else:
                    all_VT_zoning = pd.concat([this_jxtn, all_VT_zoning])
            filename.close()
        print(str(gjson), gis_or_zoning, 'consolidated.')
    all_VT_zoning=all_VT_zoning.reset_index(drop = True)
    return all_VT_zoning

def load_gis(filename):
    gdf = gpd.read_file(filename)
    gdf = get_areas(gdf)
    return gdf

def load_zoning(filename): # can be used to load .csv of either jurisdiction or district data
    df = pd.read_csv(filename)
    return df

def get_areas(gdf):
    gdf_copy = gdf.copy()
    gdf_copy = gdf_copy.to_crs('epsg:3083')
    gdf_copy['area'] = gdf_copy.geometry.area
    gdf_copy['area'] = gdf_copy['area']*3.86102*10**(-7)
    return gdf_copy

def get_total_area(gdf):
    base_districts = gdf.loc[gdf['Overlay'] == 'No']
    return(round(sum(base_districts['area']), 1))

def slice_gdf(var, gdf, slice_label):
    slice_gdf = gdf.loc[gdf[var] == slice_label]
    return slice_gdf

def map_area(gdf):
    pass

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

## MAIN CODE RETURNING ANALYTICS REQUESTED BY NATIONAL ZONING ATLAS

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

print('\nCREATING FILES\n')

# Set global coordinate reference system variable to initialize all geoDataFrames
crs = {'init': 'epsg:4326'}

# Check to see if consolidated datasets exist for district and jurisdictional zoning and geospatial files
# For each: if yes, then read file to object in current workspace
# If no, load data for all districts in directory into a single GeoDataFrame

if (os.path.exists("consolidated/district_geodata.geojson") == False):
    all_district_geodata = consolidate_data('districts_gis', 'gis')
    all_district_geodata.to_json()
    all_district_geodata.to_file('consolidated/district_geodata.geojson')
    print('Consolidated district geodata created.')
else:
    print('Consolidated district geodata exists.')
    all_district_geodata = gpd.read_file("consolidated/district_geodata.geojson")

if(os.path.exists('consolidated/district_zoning_data.csv') == False):
    all_district_zoning_data = pd.DataFrame(all_district_geodata, copy = True).drop(columns = ['geometry','area'])
    all_district_zoning_data.to_csv('consolidated/district_zoning_data.csv')
    print('Consolidated district zoning data created.')
else:
    print('Consolidated district zoning data exists.')
    all_district_zoning_data = pd.read_csv('consolidated/district_zoning_data.csv')

if (os.path.exists('consolidated/jxtn_data.csv') == False):
    all_jxtn_data = consolidate_data('jxtns', 'zoning')
    all_jxtn_data.to_csv('consolidated/jxtn_data.csv')
else:
    print('Consolidated jurisdiction attribute data exists.')
    all_jxtn_data = pd.read_csv('consolidated/jxtn_data.csv')

if (os.path.exists('consolidated/jxtn_footprints.geojson')) == False:
    all_jxtn_footprints = consolidate_data('jxtn_footprints', 'gis')
    all_jxtn_footprints.to_json()
    all_jxtn_footprints.to_file('consolidated/jxtn_footprints.geojson')
    print('Consolidated jurisdiction footprint data created.')
else:
    print('Consolidated jursidictional footprint data exists.')
    all_jxtn_footprints = gpd.read_file('consolidated/jxtn_footprints.geojson')

# Load data for all jurisdictions in directory into a single DataFrame

''' Jurisdiction characteristics '''

print('\nJURISDICTION CHARACTERISTICS')

# Total number of jurisdictions analyzed
print('\nTotal number of jurisdictions analyzed')
print('------------------------------------------')
print('Total number of jurisdictions analyzed: ', len(all_jxtn_data))
print('Total number of districts analyzed: ', len(all_district_zoning_data))
print('Total number of geospatial files completed: ', len(all_district_geodata))

#Side-by-side barplot of jurisdiction types both with and without zoning
govt_types = all_jxtn_data.groupby(['Type of Government', 'Does It Have Zoning?']).size().reset_index(name='count')
xlabels = []
heights = []
for index, row in govt_types.iterrows():
    if govt_types.loc[index]['Does It Have Zoning?'] == 'Yes':
        zoninglabel = ' With Zoning'
    elif govt_types.loc[index]['Does It Have Zoning?'] == 'No':
        zoninglabel = ' Without Zoning'
    xlabels.append(govt_types.loc[index]['Type of Government'] + '\n' + zoninglabel)
    heights.append(govt_types.loc[index]['count'])

plt.bar(xlabels, heights)
plt.title('Types of Jurisdictional Government in Dataset')
plt.tight_layout()
plt.show()

# Number and percentage of jurisdictions with zoning
print('\nPresence of zoning')
print('----------------------')
print('Number of jurisdictions with zoning: ', all_jxtn_data['Does It Have Zoning?'].value_counts()['Yes'])
print('Percentage of jurisdictions with zoning: ', all_jxtn_data['Does It Have Zoning?'].value_counts()['Yes']/len(all_jxtn_data))

cmap = (mpl.colors.ListedColormap(['lightgray', 'green']))
all_jxtn_footprints.plot(column = 'Does It Have Zoning?', categorical=True, cmap=cmap, legend=True)
plt.title('Zoned and unzoned jurisdictions,\nAddison and Chittenden Counties, VT')
plt.axis('off')
plt.show()

# Total # pages of zoning text analyzed
print('\nZoning Text Length')
print('----------------------')
all_jxtn_footprints['# of Pages in the Zoning Code'].astype(int, copy = False)
print('Total number of pages of zoning text analyzed: ', np.sum(all_jxtn_footprints['# of Pages in the Zoning Code']))

# Average # pages in each zoning text
print('Average number of pages per zoning text: ', round(np.average(all_jxtn_footprints['# of Pages in the Zoning Code']), 1))

# Shortest and longest texts
minpages = np.min(all_jxtn_footprints.loc[all_jxtn_footprints['# of Pages in the Zoning Code']!=0]['# of Pages in the Zoning Code'])
print('Shortest zoning text: ', str(minpages) + ' pages\nJurisdiction(s):', str(all_jxtn_data.loc[all_jxtn_footprints['# of Pages in the Zoning Code'] == minpages]['Jurisdiction']))
maxpages = np.max(all_jxtn_footprints['# of Pages in the Zoning Code'])
print('Longest zoning text: ', str(maxpages) + ' pages\nJurisdiction(s):', str(all_jxtn_footprints.loc[all_jxtn_footprints['# of Pages in the Zoning Code'] == maxpages]['Jurisdiction']))

# Oldest district analyzed

# Average # of districts per locality
print('\nNumber of districts per locality: ', round(len(all_district_zoning_data)/len(all_district_zoning_data['Jurisdiction'].unique()), 1))

# Total # and % of districts mapped and unmapped

# Calculate areas of all districts in jurisdiction
# Format as table
divider = '----------------------------------------------------------------------'
print('\n')
print('Total area zoned by jurisdiction:'.center(len(divider)))
print(divider)
print('JURISDICTION'.ljust(15), '\tINCLUDING OVERLAYS\tEXCLUDING OVERLAYS')
for jxtn in all_district_geodata['Jurisdiction'].unique():
    thisjxtn = all_district_geodata.loc[all_district_geodata['Jurisdiction'] == jxtn]
    thisjxtn_wo_overlays = get_total_area(thisjxtn)
    print(jxtn.ljust(25), '\t', str(round(sum(all_district_geodata.loc[all_district_geodata['Jurisdiction'] == jxtn]['area']), 1)).ljust(20), thisjxtn_wo_overlays)
