## IMPORTS

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import geopandas as gpd

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
    gdf_copy = gdf_copy.to_crs('epsg:3857')
    gdf_copy['area'] = gdf_copy.geometry.area
    gdf_copy['area'] = gdf_copy['area']*3.86102*10**(-7)
    return gdf_copy

def get_total_area(gdf):
    base_districts = gdf.loc[gdf['Overlay'] == 'No']
    return(sum(base_districts['area']))

def slice_gdf(var, gdf, slice_label):
    slice_gdf = gdf.loc[gdf[var] == slice_label]
    return slice_gdf

def map_area(gdf):
    pass

## MAIN CODE RETURNING ANALYTICS REQUESTED BY NATIONAL ZONING ATLAS

print('\nCREATING FILES\n')

# Set global coordinate reference system variable to initialize all geoDataFrames
crs = {'init': 'epsg:4326'}

# Check to see if consolidated datasets exist for district and jurisdictional zoning and geospatial files
# For each: if yes, then read file to object in current workspace
# If no, load data for all districts in directory into a single GeoDataFrame

if (os.path.exists("consolidated/district_geodata.csv") == False):
    all_district_geodata = consolidate_data('districts_gis', 'gis')
    all_district_geodata.to_file('consolidated/district_geodata.csv')
    print('Consolidated district geodata created.')
else:
    print('Consolidated district geodata exists.')
    all_district_geodata = gpd.read_file("consolidated/district_geodata.csv")

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

if (os.path.exists('consolidated/jxtn_footprints.csv')) == False:
    all_jxtn_footprints = consolidate_data('jxtn_footprints', 'gis')
    all_jxtn_footprints.to_file('consolidated/jxtn_footprints.csv')
    print('Consolidated jurisdiction footprint data created.')
else:
    print('Consolidated jursidictional footprint data exists.')
    all_jxtn_footprints = gpd.read_file('consolidated/jxtn_footprints.csv')

# Load data for all jurisdictions in directory into a single DataFrame

''' Jurisdiction characteristics '''

print('\nJURISDICTION CHARACTERISTICS')

# Total number of jurisdictions analyzed
print('\nTotal number of jurisdictions analyzed')
print('------------------------------------------')
print('Total number of jurisdictions analyzed: ', len(all_jxtn_data))
print('Total number of districts analyzed: ', len(all_district_zoning_data))
print('Total number of geospatial files completed: ', len(all_district_geodata))

# Side-by-side barplot of jurisdiction types both with and without zoning
govt_types = all_jxtn_data.groupby(['Type of Government', 'Does It Have Zoning?']).size().reset_index(name='count')
xlabels = []
heights = []
for index, row in govt_types.iterrows():
    if govt_types.loc[index]['Does It Have Zoning?'] == 'Yes':
        zoninglabel = ' With Zoning'
    elif govt_types.loc[index]['Does It Have Zoning?'] == 'No':
        zoninglabel = ' Without Zoning'
    xlabels.append(govt_types.loc[index]['Type of Government'] + zoninglabel)
    heights.append(govt_types.loc[index]['count'])

yticks = np.arange(min(heights)-1, max(heights)+1, max(heights)-min(heights))
plt.bar(xlabels, heights)
plt.xticks(rotation = 45)
plt.yticks(yticks)
plt.title('Types of Jurisdictional Government in Dataset')
plt.tight_layout()
plt.show()

# Number and percentage of jurisdictions with zoning
print('\nPresence of zoning')
print('----------------------')
print('Number of jurisdictions with zoning: ', all_jxtn_data['Does It Have Zoning?'].value_counts()['Yes'])
print('Percentage of jurisdictions with zoning: ', all_jxtn_data['Does It Have Zoning?'].value_counts()['Yes']/len(all_jxtn_data))

# Map: % of land covered by zoning in the state/region
# zoned_regions =
# zoned_regions.plot()

# Total # pages of zoning text analyzed
print('\nZoning Text Length')
print('----------------------')
# all_jxtn_data['# of Pages in the Zoning Code'].astype(int, copy = False)
# print('Total number of pages of zoning text analyzed: ', np.sum(all_jxtn_data['# of Pages in the Zoning Code']))
#
# # Average # pages in each zoning text
# print('Average number of pages per zoning text: ', np.average(all_jxtn_data['# of Pages in the Zoning Code']))

# Calculate areas of all districts in jurisdiction
print('\nAreas zoned, by jurisdiction:')
print('---------------------------------')
for jxtn in all_district_geodata['Jurisdiction'].unique():
    print('Total area zoned, including overlays, in ', jxtn, ': ', sum(all_district_geodata.loc[all_district_geodata['Jurisdiction'] == jxtn]['area']))
#
# # Calculate total area of jurisdiction by summing areas of base districts only,
# # then converting square meters to square miles
# bolton_areas = all_district_geodata.loc[all_district_geodata['Jurisdiction'] == 'Bolton']
# totalarea = get_total_area(bolton_areas)
# print('The total area in square miles of Bolton (excluding overlays) is: ' + str(totalarea))
#
# # Calculate area of districts where single-family housing is allowable by right
# threefamily = slice_gdf('3-Family Treatment', bolton_areas, 'Public Hearing')
# num_threefamily = np.sum(threefamily['area'])
# print('The area of districts where 3-family housing is allowable by right requires a public hearing is: ', str(num_threefamily))
#
# threefamily.plot()
# plt.show()
#
# print('3-family public hearing represents ', str(round(100*num_threefamily/totalarea, 2)), '% of the area in Bolton.')