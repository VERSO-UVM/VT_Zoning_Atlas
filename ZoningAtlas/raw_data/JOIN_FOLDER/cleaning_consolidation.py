import os
import pandas as pd
import geopandas as gpd
import numpy as np

def units_assignment(df):
    df_copy = df.copy()
    columns = [str(x) + '_UNITS' for x in df_copy.columns[19::] if x != None]
    unitsdf = pd.DataFrame(columns = columns)
    for index, row in df_copy.iloc[1::2, :].iterrows():
        thesecolvals = row.to_list()[19::]
        unitsdf.loc[len(unitsdf)] = thesecolvals
    df_copy = df_copy.iloc[0::2, :].reset_index(drop = True)
    unitsdf['DISTRICT'] = [val for index, val in enumerate(df_copy['ABB_DIST_NAME'])]
    df_copy = df_copy.set_index('ABB_DIST_NAME', drop = True).join(unitsdf.set_index('DISTRICT'))

    return df_copy

def check_dupe_columns(df):
    for index, col1 in enumerate(df.columns):
        for col2 in df.columns[index+1::]:
            if col1 == col2 and np.all([df[col1], df[col2]]):
                df = df.drop(col1, axis='columns')
            elif col1 != col2:
                pass
            else:
                print(df[col1])
                print(df[col2])
            # elif col1 == col2 and df[col1] == df[col2]:
            #     print('Columns duplicated but do not match')
    return df

# Function to standardize dataframe column names

column_mapper ={'County' : 'COUNTY',
                'Jurisdiction': 'JXTN',
                # : 'PARENT_JXTN'
                'Abbreviated District Name' : 'ABB_DIST_NAME',
                'Full District Name' : 'DIST_NAME',
                'Mapped But Extinct?' : 'EXT_DIST',
                'Overlay District?' : 'OVER',
                'District Mapped' : 'DIST_MAP',
                'Type of Residential District?' : 'DIST_TYPE',
                'Affordable Housing District?' : 'AFF_DIST',
                'Elderly Housing District?' : 'ELD_DIST',
                'Notes - Write any explanations here.': 'NOTES',
                '1-Family Allowed?' : '1FDP',
                '2-Family Allowed?' : '2FDP',
                '3-Family Allowed?' : '3FDP',
                '4+-Family Allowed?' : '4FDP',
                '5+-Family Allowed?' : '5FDP',
                '1F Minimum Lot Size (acres)' : '1F_MIN_LOT',
                '1F Front Setback (ft)' : '1F_FSET',
                 # '1F_FSET_UNITS',
                '1F Side Setback (ft)': '1F_SSET',
                # : '1F_SSET_UNITS',
                '1F Rear Setback (ft)' : '1F_RSET',
                # : '1F_RSET_UNITS',
                '1F Max. Lot Coverage - Buildings (%)' : '1F_MAX_LOT_BLDG',
                # : '1F_MAX_LOT_BLDG_UNITS'
                '1F Max. Lot coverage - Buildings & Impervious Surface (%)' : '1F_MAX_LOT_IMP',
                # : '1F_MAX_LOT_IMP_UNITS'
                '1F Minimum Parking Spaces' : '1F_PARK',
                # : '1F_PARK_UNITS',
                '1F Max. Stories' : '1F_STORIES',
                # : '1F_STORIES_UNITS',
                '1F Max. Height (ft)' : '1F_HEIGHT',
                # : '1F_HEIGHT_UNITS',
                '1F Floor to Area Ratio' : '1F_FTA',
                # : '1F_FTA_UNITS',
                '1F Minimum Unit Size (sq. ft.)' : '1F_MIN_UNIT',
                # : '1F_MIN_UNIT_UNITS',
                '2F Affordable Housing Only' : '2F_AFF',
                '2F Elderly Housing Only' : '2F_ELD',
                '2F Minimum Lot Size (acres)': '2F_MIN_LOT',
                # : '2F_MIN_LOT_UNITS',
                '2F Maximum Density (units/acre)' : '2F_MAX_DENS',
                # : '2F_MAX_DENS_UNITS',
                '2F Front Setback (ft)' : '2F_FSET',
                # : '2F_FSET_UNITS',
                '2F Side Setback (ft)' : '2F_SSET',
                # : '2F_SSET_UNITS',
                '2F Rear Setback (ft)' : '2F_RSET',
                # : '2F_RSET_UNITS',
                '2F Max. Lot Coverage - Buildings (%)' : '2F_MAX_LOT_BLDG',
                # : '2F_MAX_LOT_BLDG_UNITS',
                '2F Max. Lot coverage - Buildings & Impervious Surface (%)' : '2F_MAX_LOT_IMP',
                # : '2F_MAX_LOT_IMP_UNITS',
                '2F Minimum Parking Spaces per Studio or 1BR' : '2F_PARK_1BR',
                # : '2F_PARK_1BR_UNITS',
                '2F Minimum Parking Spaces per 2+ BR' : '2F_PARK_2BR',
                # : '2F_PARK_2BR_UNITS',
                '2F Max. Stories' : '2F_STORIES',
                # : '2F_STORIES_UNITS',
                '2F Max. Height (ft)' : '2F_HEIGHT',
                # : '2F_HEIGHT_UNITS',
                '2F Floor to Area Ratio' : '2F_FTA',
                # : '2F_FTA_UNITS',
                '2F Minimum Unit Size (sq. ft.)' : '2F_MIN_UNIT',
                # : '2F_MIN_UNIT_UNITS',
                '3F Affordable Housing Only' : '3F_AFF',
                '3F Elderly Housing Only' : '3F_ELD',
                '3F Minimum Lot Size (acres)' : '3F_MIN_LOT',
                # : '3F_MIN_LOT_UNITS',
                '3F Maximum Density (units/acre)' : '3F_MAX_DENS',
                # : '3F_MAX_DENS_UNITS',
                '3F Front Setback (ft)' : '3F_FSET',
                # : '3F_FSET_UNITS',
                '3F Side Setback (ft)' : '3F_SSET',
                # : '3F_SSET_UNITS',
                '3F Rear Setback (ft)' : '3F_RSET',
                # : '3F_RSET_UNITS',
                '3F Max. Lot Coverage - Buildings (%)' : '3F_MAX_LOT_BLDG',
                # : '3F_MAX_LOT_BLDG_UNITS',
                '3F Max. Lot coverage - Buildings & Impervious Surface (%)' : '3F_MAX_LOT_IMP',
                # : '3F_MAX_LOT_IMP_UNITS',
                '3F Minimum Parking Spaces per Studio or 1BR' : '3F_PARK_1BR',
                # : '3F_PARK_1BR_UNITS',
                '3F Minimum Parking Spaces per 2+ BR' : '3F_PARK_2BR',
                # : '3F_PARK_2BR_UNITS',
                '3F Connection to Sewer and/or Water Required' : '3F_CNXN_H2O',
                '3F Connection or Proximity to Public Transit Required' : '3F_CNXN_TRANSIT',
                '3F Max. Stories' : '3F_STORIES',
                # : '3F_STORIES_UNITS',
                '3F Max. Height (ft)' : '3F_HEIGHT',
                # : '3F_HEIGHT_UNITS',
                '3F Floor to Area Ratio' : '3F_FTA',
                # : '3F_FTA_UNITS',
                '3F Minimum Unit Size (sq. ft.)' : '3F_MIN_UNIT',
                # : '3F_MIN_UNIT_UNITS',
                '3F Max. Bedrooms' : '3F_BEDROOMS',
                # : '3F_BEDROOMS_UNITS',
                '4F Affordable Housing Only' : '4F_AFF',
                '4F Elderly Housing Only' : '4F_ELD',
                '4F Minimum Lot Size (acres)' : '4F_MIN_LOT',
                # : '4F_MIN_LOT_UNITS',
                '4F Maximum Density (units/acre)' : '4F_MAX_DENS',
                # : '4F_MAX_DENS_UNITS',
                '4F Front Setback (ft)' : '4F_FSET',
                # : '4F_FSET_UNITS',
                '4F Side Setback (ft)' : '4F_SSET',
                # : '4F_SSET_UNITS',
                '4F Rear Setback (ft)' : '4F_RSET',
                # : '4F_RSET_UNITS',
                '4F Max. Lot Coverage - Buildings (%)' : '4F_MAX_LOT_BLDG',
                # : '4F_MAX_LOT_BLDG_UNITS',
                '4F Max. Lot coverage - Buildings & Impervious Surface (%)' : '4F_MAX_LOT_IMP',
                # : '4F_MAX_LOT_IMP_UNITS',
                '4F Minimum Parking Spaces per Studio or 1BR' : '4F_PARK_1BR',
                # : '4F_PARK_1BR_UNITS',
                '4F Minimum Parking Spaces per 2+ BR' : '4F_PARK_2BR',
                # : '4F_PARK_2BR_UNITS',
                '4F Connection to Sewer and/or Water Required' : '4F_CNXN_H2O',
                '4F Connection or Proximity to Public Transit Required' : '4F_CNXN_TRANSIT',
                '4F Max. Stories' : '4F_STORIES',
                # : '4F_STORIES_UNITS',
                '4F Max. Height (ft)' : '4F_HEIGHT',
                # : '4F_HEIGHT_UNITS',
                '4F Floor to Area Ratio' : '4F_FTA',
                # : '4F_FTA_UNITS',
                '4F Minimum Unit Size (sq. ft.)' : '4F_MIN_UNIT',
                # : '4F_MIN_UNIT_UNITS',
                '4F Max. Bedrooms' : '4F_BEDROOMS',
                # : '4F_BEDROOMS_UNITS',
                '4F Max. Units Per Building' : '4F_MAX_UNIT',
                # : '4F_MAX_UNIT_UNITS',
                'Affordable Housing Allowed?' : 'AFFDP',
                'AFF Definition' : 'AFF_DEF',
                'AFF Elderly Housing Only' : 'AFF_ELD_ONLY',
                'AFF Minimum Lot Size (acres)' : 'AFF_MIN_LOT',
                # : 'AFF_MIN_LOT_UNITS',
                'AFF Maximum Density (units/acre)' : 'AFF_MAX_DENS',
                # : 'AFF_MAX_DENS_UNITS',
                'AFF Minimum Parking Spaces per Studio or 1BR' : 'AFF_PARK_1BR',
                # : 'AFF_PARK_1BR_UNITS',
                'AFF Minimum Parking Spaces per 2+ BR' : 'AFF_PARK_2BR',
                # : 'AFF_PARK_2BR_UNITS',
                # : 'AFF_CNXN_H2O',
                # : 'AFF_CNXN_TRANSIT',
                'AFF Minimum Unit Size (sq. ft.)' : 'AFF_MIN_UNIT',
                # : 'AFF_MIN_UNIT_UNITS',
                'AFF Max. Bedrooms' : 'AFF_BEDROOMS',
                # : 'AFF_BEDROOMS_UNITS',
                'AFF Max. Units Per Building' : 'AFF_MAX_UNIT',
                # : 'AFF_MAX_UNIT_UNITS',
                'ADUs Allowed?' : 'ADUDP',
                'ADU Employee or Family Occupancy Required' : 'ADU_EMP_REQD',
                'ADU Renter Occupancy Required' : 'ADU_RENTER_PROH',
                'ADU Owner Occupancy Required' : 'ADU_OWNER_REQD',
                'ADU Elderly Housing Only' : 'ADU_ELD',
                'ADU Minimum Lot Size (acres)' : 'ADU_MIN_LOT',
                # : 'ADU_MIN_LOT_UNITS',
                'ADU Minimum Parking Spaces' : 'ADU_PARK',
                # : 'ADU_PARK_UNITS',
                'ADU Restricted to Only Primary Structure' : 'ADU_PRIM_STRUC',
                'ADU Max. ADU Size (%)' : 'ADU_MAX_PCT',
                # : 'ADU_MAX_PCT_UNITS',
                'ADU Max. ADU Size (sq. ft.)' : 'ADU_MAX_SIZE',
                # : 'ADU_MAX_SIZE_UNITS',
                'ADU Max. Bedrooms' : 'ADU_BEDROOMS',
                # : 'ADU_BEDROOMS_UNITS',
                'PRDs Allowed?' : 'PRDDP',
                'PRD Mobile or Manufactured Home Park' : 'PRD_MHP',
                'PRD Minimum Lot Size (acres)' : 'PRD_MIN_LOT',
                # : 'PRD_MIN_LOT_UNITS',
                'PRD Maximum Density (units/acre)' : 'PRD_MAX_DENS',
                # : 'PRD_MAX_DENS_UNITS',
                'PRD Max. Units' : 'PRD_MAX_UNIT',
                # : 'PRD_MAX_UNIT_UNITS',
                # : 'SPNOTES',
                # : 'TTIPNOTES',
                '5F Affordable Housing Only' : '5F_AFF',
                '5F Elderly Housing Only' : '5F_ELD',
                '5F Minimum Lot Size (acres)' : '5F_MIN_LOT',
                '5F Maximum Density (units/acre)' : '5F_MAX_DENS',
                '5F Front Setback (ft)' : '5F_FSET',
                '5F Side Setback (ft)' : '5F_SSET',
                '5F Rear Setback (ft)' : '5F_RSET',
                '5F Max. Lot Coverage - Buildings (%)' : '5F_MAX_LOT_BLDG',
                '5F Max. Lot coverage - Buildings & Impervious Surface (%)' : '5F_MAX_LOT_IMP',
                '5F Minimum Parking Spaces per Studio or 1BR' : '5F_PARK_1BR',
                '5F Minimum Parking Spaces per 2+ BR' : '5F_PARK_2BR',
                '5F Connection to Sewer and/or Water Required' : '5F_CNXN_H2O',
                '5F Connection or Proximity to Public Transit Required' : '5F_CNXN_TRANSIT',
                '5F Max. Stories' : '5F_STORIES',
                '5F Max. Height (ft)' : '5F_FEET',
                '5F Floor to Area Ratio' : '5F_FTA',
                '5F Minimum Unit Size (sq. ft.)' : '5F_MIN_UNIT',
                '5F Max. Bedrooms' : '5F_BEDROOMS',
                '5F Max. Units Per Building' : '5F_MAX_UNIT',
                'Base residential density (units/acre)' : 'BASE_DENS',
                '1F Frontage (ft)' : '1F_FRONT',
                '2F Frontage (ft)' : '2F_FRONT',
                '3F Frontage (ft)' : '3F_FRONT',
                '4F Frontage (ft)' : '4F_FRONT',
                '5F Frontage (ft)' : '5F_FRONT',
                'PUD required with Subdivision' : 'PUD_SUBDV',
                'PUD Threshold #' : 'PUD_THRESH',
                'PUD Allowed' : 'PUD_ALLOW',
                'PUD requiring land conservation' : 'PUD_CONSERVE',
#                 # : 'GIS_ID'
}
    # return [column_mapper.get(col, col) for col in columns]

# In[8]:

# Function to standardize editor column names
editor_column_mapper = {'Status':'STAT',
                 'Last Updated': 'LAST_UPDATE',
                 'Jurisdiction Status': 'JXTN_STAT',
                 'State': 'STATE',
                 'County': 'COUNTY',
                 'Jurisdiction': 'JXTN',
                 'District Mapped': 'DIST_MAP',
                 'Juridiction Last Updated': 'JXTN_UPDATE',
                 'Parent Jurisdiction': 'PARENT_JXTN',
                 'Abbreviated District Name': 'ABB_DIST_NAME',
                 'Visible Atlas Notes': 'NOTES',
                 '3-Family Max Stories': '3F_STORIES',
                 '3-Family Max Stories Units': '3F_STORIES_UNITS',
                 '3-Family Max Height': '3F_MAX_HEIGHT',
                 '3-Family Max Height Units': '3F_MAX_HEIGHT_UNITS',
                 '3-Family Min Unit Size': '3F_MIN_UNIT',
                 '3-Family Min Unit Size Units': '3F_MIN_UNIT_UNITS',
                 '3-Family Max Bedrooms': '3F_BEDROOMS',
                 '3-Family Max Bedrooms Units': '3F_BEDROOMS_UNITS',
                 '4+-Family Max Density': '4F_MAX_DENSITY',
                 '4+-Family Max Density Units': '4F_MAX_DENSITY_UNITS',
                 '4+-Family Max Lot Coverage Buildings': '4F_MAX_LOT_BLDG',
                 '4+-Family Max Lot Coverage Buildings Units': '4F_MAX_LOT_BLDG_UNITS',
                 '4+-Family Max Stories': '4F_STORIES',
                 '4+-Family Max Stories Units': '4F_STORIES_UNITS',
                 '4+-Family Max Height': '4F_HEIGHT',
                 '4+-Family Max Height Units': '4F_HEIGHT_UNITS',
                 '4+-Family Min Unit Size': '4F_MIN_UNIT',
                 '4+-Family Min Unit Size Units': '4F_MIN_UNIT_UNITS',
                 '4+-Family Max Bedrooms': '4F_BEDROOMS',
                 '4+-Family Max Bedrooms Units': '4F_BEDROOMS_UNITS',
                 'Affordable Max Density': 'AFF_MAX_DENS',
                 'Affordable Max Density Units': 'AFF_MAX_DENS_UNITS',
                 'Affordable Min Unit Size': 'AFF_MIN_UNIT',
                 'Affordable Min Unit Size Units': 'AFF_MIN_UNIT_UNITS',
                 'Affordable Max Bedrooms': 'AFF_BEDROOMS',
                 'Affordable Max Bedrooms Units': 'AFF_BEDROOMS_UNITS',
                 'ADU Max Bedrooms': 'ADU_BEDROOMS',
                 'ADU Max Bedrooms Units': 'ADU_BEDROOMS_UNITS',
                 'PRD Min Development Size': 'PRD_MIN_LOT',
                 'PRD Max Density': 'PRD_MAX_DENS',
                 'PRD Max Density Units': 'PRD_MAX_DENS_UNITS',
                 'PRD Max Units': 'PRD_MAX_UNIT',
                 'PRD Max Units Units': 'PRD_MAX_UNIT_UNITS',
                 'Full District Name': 'DIST_NAME',
                 'Effective Start Date': 'BYLAW_EFF',
                 'Changed or Expired': 'CHANGE_EXP',
                 'District Mapped But Extinct': 'EXT_DIST',
                 'Overlay': 'OVER',
                 'Type of Zoning District': 'DIST_TYPE',
                 'Affordable Housing District': 'AFF_DIST',
                 'Elderly Housing District': 'ELD_DIST',
                 '1-Family Treatment': '1FDP',
                 '2-Family Treatment': '2FDP',
                 '3-Family Treatment': '3FDP',
                 '4+-Family Treatment': '4FDP',
                 '1-Family Min. Lot': '1F_MIN_LOT',
                 '1-Family Min. Lot Size': '1F_MIN_LOT',
                 '1-Family Min. Lot Units': '1F_MIN_LOT_UNITS',
                 '1-Family Min. Lot Size Units': '1F_MIN_LOT_UNITS',
                 '1-Family Front Setback': '1F_FSET',
                 '1-Family Front Setback Units': '1F_FSET_UNITS',
                 '1-Family Side Setback': '1F_SSET',
                 '1-Family Side Setback Units': '1F_SSET_UNITS',
                 '1-Family Rear Setback': '1F_RSET',
                 '1-Family Rear Setback Units': '1F_RSET_UNITS',
                 '1-Family Max. Lot Coverage - Buildings': '1F_MAX_LOT_BLDG',
                 '1-Family Max Lot Coverage - Buildings': '1F_MAX_LOT_BLDG',
                 '1-Family Max. Lot Coverage - Buildings Units': '1F_MAX_LOT_BLDG_UNITS',
                 '1-Family Max Lot Coverage - Buildings Units': '1F_MAX_LOT_BLDG_UNITS',
                 '1-Family Max. Lot Coverage - Buildings & Impervious Surface': '1F_MAX_LOT_IMP',
                 '1-Family Max Lot Coverage - Buildings & Impervious Surface': '1F_MAX_LOT_IMP',
                 '1-Family Max. Lot Coverage - Buildings & Impervious Surface Units': '1F_MAX_LOT_IMP_UNITS',
                 '1-Family Max Lot Coverage - Buildings & Impervious Surface Units': '1F_MAX_LOT_IMP_UNITS',
                 '1-Family Min. # Parking Spaces': '1F_PARK',
                 '1-Family Min. Parking': '1F_PARK',
                 '1-Family Min. # Parking Spaces Units': '1F_PARK_UNITS',
                 '1-Family Min. Parking Units': '1F_PARK_UNITS',
                 '1-Family Max. Stories': '1F_STORIES',
                 '1-Family Max Stories': '1F_STORIES',
                 '1-Family Max. Stories Units': '1F_STORIES_UNITS',
                 '1-Family Max Stories Units': '1F_STORIES_UNITS',
                 '1-Family Max. Height': '1F_HEIGHT',
                 '1-Family Max Height': '1F_HEIGHT',
                 '1-Family Max. Height Units': '1F_HEIGHT_UNITS',
                 '1-Family Max Height Units': '1F_HEIGHT_UNITS',
                 '1-Family Floor to Area Ratio': '1F_FTA',
                 '1-Family Floor to Area Ratio Units': '1F_FTA_UNITS',
                 '1-Family Min. Unit Size': '1F_MIN_UNIT',
                 '1-Family Min. Unit Size Units': '1F_MIN_UNIT_UNITS',
                 '2-Family Affordable Housing Only': '2F_AFF',
                 '2-Family Elderly Housing Only': '2F_ELD',
                 '2-Family Min. Lot': '2F_MIN_LOT',
                 '2-Family Min. Lot Units': '2F_MIN_LOT_UNITS',
                 '2-Family Max. Density': '2F_MAX_DENS',
                 '2-Family Max. Density Units': '2F_MAX_DENS_UNITS',
                 '2-Family Front Setback': '2F_FSET',
                 '2-Family Front Setback Units': '2F_FSET_UNITS',
                 '2-Family Side Setback': '2F_SSET',
                 '2-Family Side Setback Units': '2F_SSET_UNITS',
                 '2-Family Rear Setback': '2F_RSET',
                 '2-Family Rear Setback Units': '2F_RSET_UNITS',
                 '2-Family Max. Lot Coverage - Buildings': '2F_MAX_LOT_BLDG',
                 '2-Family Max. Lot Coverage - Buildings Units' : '2F_MAX_LOT_BLDG_UNITS',
                 '2-Family Max. Lot Coverage - Buildings & Impervious Surface': '2F_MAX_LOT_IMP',
                 '2-Family Max. Lot Coverage - Buildings & Impervious Surface Units': '2F_MAX_LOT_IMP_UNITS',
                 '2-Family Min. # Parking Spaces Per Studio or 1BR': '2F_PARK_1BR',
                 '2-Family Min. # Parking Spaces Per Studio or 1BR Units': '2F_PARK_1BR_UNITS',
                 '2-Family Min. # Parking Spaces Per 2+ BR': '2F_PARK_2BR',
                 '2-Family Min. # Parking Spaces Per 2+ BR Units': '2F_PARK_2BR_UNITS',
                 '2-Family Max. Stories': '2F_STORIES',
                 '2-Family Max. Stories Units': '2F_STORIES_UNITS',
                 '2-Family Max. Height': '2F_HEIGHT',
                 '2-Family Max. Height Units': '2F_HEIGHT_UNITS',
                 '2-Family Max Density': '2F_MAX_DENS',
                 '2-Family Max Density Units': '2F_MAX_DENS_UNITS',
                 '2-Family Max Lot Coverage Buildings': '2F_MAX_LOT_BLDG',
                 '2-Family Max Lot Coverage Buildings Units': '2F_MAX_LOT_BLDG_UNITS',
                 '2-Family Max Stories': '2F_STORIES',
                 '2-Family Max Stories Units': '2F_STORIES_UNITS',
                 '2-Family Max Height': '2F_HEIGHT',
                 '2-Family Max Height Units': '2F_HEIGHT_UNITS',
                 '2-Family Min Unit Size': '2F_MIN_UNIT',
                 '2-Family Min Unit Size Units': '2F_MIN_UNIT_UNITS',
                 '2-Family Floor to Area Ratio': '2F_FTA',
                 '2-Family Floor to Area Ratio Units': '2F_FTA_UNITS',
                 '2-Family Min. Unit Size': '2F_MIN_UNIT',
                 '2-Family Min. Unit Size Units': '2F_MIN_UNIT_UNITS',
                 '3-Family Affordable Housing Only': '3F_AFF',
                 '3-Family Elderly Housing Only': '3F_ELD',
                 '3-Family Min. Lot': '3F_MIN_LOT',
                 '3-Family Min. Lot Units': '3F_MIN_LOT_UNITS',
                 '3-Family Max. Density': '3F_MAX_DENS',
                 '3-Family Max. Density Units': '3F_MAX_DENS_UNITS',
                 '3-Family Front Setback': '3F_FSET',
                 '3-Family Front Setback Units': '3F_FSET_UNITS',
                 '3-Family Side Setback': '3F_SSET',
                 '3-Family Side Setback Units': '3F_SSET_UNITS',
                 '3-Family Rear Setback': '3F_RSET',
                 '3-Family Rear Setback Units': '3F_RSET_UNITS',
                 '3-Family Max. Lot Coverage - Buildings': '3F_MAX_LOT_BLDG',
                 '3-Family Max. Lot Coverage - Buildings Units' : '3F_MAX_LOT_BLDG_UNITS',
                 '3-Family Max. Lot Coverage - Buildings & Impervious Surface': '3F_MAX_LOT_IMP',
                 '3-Family Max. Lot Coverage - Buildings & Impervious Surface Units': '3F_MAX_LOT_IMP_UNITS',
                 '3-Family Min. Parking Spaces Per Studio or 1BR': '3F_PARK_1BR',
                 '3-Family Min. Parking Spaces Per Studio or 1BR Units': '3F_PARK_1BR_UNITS',
                 '3-Family Min. Parking Spaces Per 2+ BR': '3F_PARK_2BR',
                 '3-Family Min. Parking Spaces Per 2+ BR Units': '3F_PARK_2BR_UNITS',
                 '3-Family Min. # Parking Spaces Per Studio or 1BR': '3F_PARK_1BR',
                 '3-Family Min. # Parking Spaces Per Studio or 1BR Units': '3F_PARK_1BR_UNITS',
                 '3-Family Min. # Parking Spaces Per 2+ BR': '3F_PARK_2BR',
                 '3-Family Min. # Parking Spaces Per 2+ BR Units': '3F_PARK_2BR_UNITS',
                 '3-Family Connection to Sewer and/or Water Required': '3F_CNXN_H2O',
                 '3-Family Connection or Proximity to Public Transit Required': '3F_CNXN_TRANSIT',
                 '3-Family Max. Stories': '3F_STORIES',
                 '3-Family Max. Stories Units': '3F_STORIES_UNITS',
                 '3-Family Max. Height': '3F_HEIGHT',
                 '3-Family Max. Height Units': '3F_HEIGHT_UNITS',
                 '3-Family Floor to Area Ratio': '3F_FTA',
                 '3-Family Floor to Area Ratio Units': '3F_FTA_UNITS',
                 '3-Family Min. Unit Size': '3F_MIN_UNIT',
                 '3-Family Min. Unit Size Units': '3F_MIN_UNIT_UNITS',
                 '3-Family Max. Bedrooms': '3F_BEDROOMS',
                 '3-Family Max. Bedrooms Units': '3F_BEDROOMS_UNITS',
                 '3-Family Max Density': '3F_MAX_DENS',
                 '3-Family Max Density Units': '3F_MAX_DENS_UNITS',
                 '3-Family Max Lot Coverage Buildings': '3F_MAX_LOT_BLDG',
                 '3-Family Max Lot Coverage Buildings Units': '3F_MAX_LOT_BLDG_UNITS',
                 '4+-Family Affordable Housing Only': '4F_AFF',
                 '4+-Family Elderly Housing Only': '4F_ELD',
                 '4+-Family Min. Lot': '4F_MIN_LOT',
                 '4+-Family Min. Lot Units': '4F_MIN_LOT_UNITS',
                 '4+-Family Max. Density': '4F_MAX_DENS',
                 '4+-Family Max. Density Units': '4F_MAX_DENS_UNITS',
                 '4+-Family Front Setback': '4F_FSET',
                 '4+-Family Front Setback Units': '4F_FSET_UNITS',
                 '4+-Family Side Setback': '4F_SSET',
                 '4+-Family Side Setback Units': '4F_SSET_UNITS',
                 '4+-Family Rear Setback': '4F_RSET',
                 '4+-Family Rear Setback Units': '4F_RSET_UNITS',
                 '4+-Family Max. Lot Coverage - Buildings': '4F_MAX_LOT_BLDG',
                 '4+-Family Max. Lot Coverage - Buildings Units': '4F_MAX_LOT_BLDG_UNITS',
                 '4+-Family Max. Lot Coverage - Buildings & Impervious Surface': '4F_MAX_LOT_IMP',
                 '4+-Family Max. Lot Coverage - Buildings & Impervious Surface Units': '4F_MAX_LOT_IMP_UNITS',
                 '4+-Family Min. Parking Spaces Per Studio or 1BR': '4F_PARK_1BR',
                 '4+-Family Min. Parking Spaces Per Studio or 1BR Units': '4F_PARK_1BR_UNITS',
                 '4+-Family Min. Parking Spaces Per 2+ BR': '4F_PARK_2BR',
                 '4+-Family Min. # Parking Spaces Per Studio or 1BR': '4F_PARK_1BR',
                 '4+-Family Min. Parking Spaces Per 2+ BR Units': '4F_PARK_2BR_UNITS',
                 '4+-Family Min. # Parking Spaces Per Studio or 1BR Units': '4F_PARK_1BR_UNITS',
                 '4+-Family Min. # Parking Spaces Per 2+ BR': '4F_PARK_2BR',
                 '4+-Family Min. # Parking Spaces Per 2+ BR Units': '4F_PARK_2BR_UNITS',
                 '4+-Family Connection to Sewer and/or Water Required': '4F_CNXN_H2O',
                 '4+-Family Connection or Proximity to Public Transit Required': '4F_CNXN_TRANSIT',
                 '4+-Family Max. Stories': '4F_STORIES',
                 '4+-Family Max. Stories Units': '4F_STORIES_UNITS',
                 '4+-Family Max. Height': '4F_HEIGHT',
                 '4+-Family Max. Height Units': '4F_HEIGHT_UNITS',
                 '4+-Family Floor to Area Ratio': '4F_FTA',
                 '4+-Family Floor to Area Ratio Units': '4F_FTA_UNITS',
                 '4+-Family Min. Unit Size': '4F_MIN_UNIT',
                 '4+-Family Min. Unit Size Units': '4F_MIN_UNIT_UNITS',
                 '4+-Family Max. Bedrooms': '4F_BEDROOMS',
                 '4+-Family Max. Bedrooms Units': '4F_BEDROOMS_UNITS',
                 '4+-Family Max. Units': '4F_MAX_UNIT',
                 '4+-Family Max. Units Units': '4F_MAX_UNIT_UNITS',
                 'Affordable Housing (AH) Treatment': 'AFFDP',
                 'AH - Definition': 'AFF_DEF',
                 'AH - Elderly Housing Only': 'AFF_ELD_ONLY',
                 'AH Min. Lot': 'AFF_MIN_LOT',
                 'AH Min. Lot Units': 'AFF_MIN_LOT_UNITS',
                 'AH Max. Density': 'AFF_MAX_DENS',
                 'AH Max. Density Units': 'AFF_MAX_DENS_UNITS',
                 'AH Min. Parking Spaces Per Studio or 1BR': 'AFF_PARK_1BR',
                 'AH Min. Parking Spaces Per Studio or 1BR Units': 'AFF_PARK_1BR_UNITS',
                 'AH Min. Parking Spaces Per 2+ BR': 'AFF_PARK_2BR',
                 'AH Min. Parking Spaces Per 2+ BR Units': 'AFF_PARK_2BR_UNITS',
                 'AH Connection to Sewer and/or Water Required': 'AFF_CNXN_H2O',
                 'AH Connection or Proximity to Public Transit Required': 'AFF_CNXN_TRANSIT',
                 'AH Min. Unit Size': 'AFF_MIN_UNIT',
                 'AH Min. Unit Size Units': 'AFF_MIN_UNIT_UNITS',
                 'AH Max. Bedrooms': 'AFF_BEDROOMS',
                 'AH Max. Bedrooms Units': 'AFF_BEDROOMS_UNITS',
                 'AH Max. Units': 'AFF_MAX_UNIT',
                 'AH Max. Units Units': 'AFF_MAX_UNIT_UNITS',
                 'Accessory Dwelling Unit (ADU) Treatment': 'ADUDP',
                 'ADU Employee or Family Occupancy Required': 'ADU_EMP_REQD',
                 'ADU Renter Occupancy Prohibited': 'ADU_RENTER_PROH',
                 'ADU Owner Occupancy Required': 'ADU_OWNER_REQD',
                 'ADU Elderly Housing Only': 'ADU_ELD',
                 'ADU Min. Lot': 'ADU_MIN_LOT',
                 'ADU Min. Lot Units': 'ADU_MIN_LOT_UNITS',
                 'ADU Min. Parking Spaces': 'ADU_PARK',
                 'ADU Min. Parking Spaces Units': 'ADU_PARK_UNITS',
                 'ADU Restricted to Only Primary Structure (i.e., No Outbuildings like Garages)': 'ADU_PRIM_STRUC',
                 'ADU Max. Percent Main Unit': 'ADU_MAX_PCT',
                 'ADU Max. Percent Main Unit Units': 'ADU_MAX_PCT_UNITS',
                 'ADU Max. Size': 'ADU_MAX_SIZE',
                 'ADU Max Size (% of Main)': 'ADU_MAX_SIZE',
                 'ADU Max. Size Units': 'ADU_MAX_SIZE_UNITS',
                 'ADU Max Size (% of Main) Units': 'ADU_MAX_SIZE_UNITS',
                 'ADU Max Size (sq ft)': 'ADU_MAX_SIZE_SQFT',
                 'ADU Max Size (sq ft) Units': 'ADU_MAX_SIZE_SQFT_UNITS',
                 'ADU Max. Bedrooms': 'ADU_BEDROOMS',
                 'ADU Max. Bedrooms Units': 'ADU_BEDROOMS_UNITS',
                 'Planned Residential Development (PRD) Treatment': 'PRDDP',
                 'Mobile or Manufactured Home Park': 'PRD_MHP',
                 'PRD Min. Lot': 'PRD_MIN_LOT',
                 'PRD Min. Development Size': 'PRD_MIN_LOT',
                 'PRD Min. Lot Units': 'PRD_MIN_LOT_UNITS',
                 'PRD Max. Density': 'PRD_MAX_DENS',
                 'PRD Max. Density Units': 'PRD_MAX_DENS_UNITS',
                 'PRD Max. Units': 'PRD_MAX_UNIT',
                 'PRD Max. Units Per Development Units': 'PRD_MAX_UNIT_UNITS',
                 'PRD Max. Units Units': 'PRD_MAX_UNIT_UNITS',
                 'Special Notes': 'SPNOTES',
                 'Tooltip Notes': 'TTIPNOTES',
                 '5+Family Affordable Housing Only': '5F_AFF',
                 '5+Family Elderly Housing Only': '5F_ELD',
                 '5+Family Min. Lot (ACRES)': '5F_MIN_LOT',
                 '5+Family Max. Density (UNITS/ACRE)': '5F_MAX_DENS',
                 '5+Family Front Setback (# of feet)': '5F_FSET',
                 '5+Family Side Setback (# of feet)': '5F_SSET',
                 '5+Family Rear Setback (# of feet)': '5F_RSET',
                 '5+Family Max. Lot Coverage - Buildings (%)': '5F_MAX_LOT_BLDG',
                 '5+Family Max. Lot Coverage - Buildings & Imperviou': '5F_MAX_LOT_IMP',
                 '5+Family Min. # Parking Spaces Per Studio or 1BR': '5F_PARK_1BR',
                 '5+Family Min. # Parking Spaces Per 2+ BR': '5F_PARK_2BR',
                 '5+Family Connection to Sewer and/or Water Required': '5F_CNXN_H2O',
                 '5+Family Connection or Proximity to Public Transit': '5F_CNXN_TRANSIT',
                 '5+Family Max. Height (# of stories)': '5F_STORIES',
                 '5+Family Max. Height (# of feet)': '5F_FEET',
                 '5+Family Floor to Area Ratio': '5F_FTA',
                 '5+Family Min. Unit Size (SF)': '5F_MIN_UNIT',
                 '5+Family Max. # Bedrooms Per Unit': '5F_BEDROOMS',
                 '5+Family Max. # Units Per Building': '5F_MAX_UNIT',
                 'Base Residential Density (#dwellings/acre)': 'BASE_DENS',
                 '1-Family Lot Frontage Requirement': '1F_FRONT',
                 '2-Family Lot Frontage Requirement': '2F_FRONT',
                 '3-Family Lot Frontage Requirement': '3F_FRONT',
                 '4-Family Lot Frontage Requirement': '4F_FRONT',
                 '5+-Family Lot Frontage Requirement': '5F_FRONT',
                 'PUD required with Subdivision': 'PUD_SUBDV',
                 'PUD required with Subdivision Units': 'PUD_SUBDV_UNITS',
                 'PUD Threshold #': 'PUD_THRESH',
                 'PUD allowed': 'PUD_ALLOW',
                 'PUD Allowed': 'PUD_ALLOW',
                 'PUD requiring land conservation': 'PUD_CONSERVE',
                 'Unique GIS schema identifier': 'GIS_ID', 'PRD Treatment': 'PRDDP',
                'PRD Mobile or Manufactured': 'PRD_MHP',
                'PRD Min Development Size Units': 'PRD_MIN_LOT_UNITS',
                'ADU Treatment': 'ADUDP',
                'ADU Employee/Family Required': 'ADU_EMP_REQD',
                'ADU Renter Prohibited': 'ADU_RENTER_PROH',
                'ADU Elderly Only': 'ADU_ELD',
                'ADU Min Lot Size': 'ADU_MIN_LOT',
                'ADU Min Lot Size Units': 'ADU_MIN_LOT_UNITS',
                'ADU Min Parking': 'ADU_PARK',
                'ADU Min Parking Units': 'ADU_PARK_UNITS',
                'ADU Only Primary Structure': 'ADU_PRIM_STRUC',
                'Affordable Max Units per Building': 'AFF_MAX_UNIT',
                'Affordable Max Units per Building Units': 'AFF_MAX_UNIT_UNITS',
                'Affordable Min Parking Per Studio/1BR': 'AFF_PARK_1BR',
                'Affordable Min Parking Per Studio/1BR Units': 'AFF_PARK_1BR_UNITS',
                'Affordable Min Parking Per 2+ BR': 'AFF_PARK_2BR',
                'Affordable Min Parking Per 2+ BR Units': 'AFF_PARK_2BR_UNITS',
                'Affordable Sewer/Water Required': 'AFF_CNXN_H2O',
                'Affordable Public Transit Required': 'AFF_CNXN_TRANSIT',
                '4+-Family Max Units per Building': '4F_MAX_UNIT',
                '4+-Family Max Units per Building Units': '4F_MAX_UNIT_UNITS',
                'Affordable Housing Treatment': 'AFFDP',
                'Affordable Housing Definition': 'AFF_DEF',
                'Affordable Elderly Only': 'AFF_ELD',
                'Affordable Min Lot Size': 'AFF_MIN_LOT',
                'Affordable Min Lot Size Units': 'AFF_MIN_LOT_UNITS',
                '4+-Family Max Lot Coverage Buildings & Impervious': '4F_MAX_LOT_IMP',
                '4+-Family Max Lot Coverage Buildings & Impervious Units': '4F_MAX_LOT_IMP_UNITS',
                '4+-Family Min Parking Per Studio/1BR': '4F_PARK_1BR',
                '4+-Family Min Parking Per Studio/1BR Units': '4F_PARK_1BR_UNITS',
                '4+-Family Min Parking Per 2+ BR': '4F_PARK_2BR',
                '4+-Family Min Parking Per 2+ BR Units': '4F_PARK_2BR_UNITS',
                '4+-Family Sewer/Water Required': '4F_CNXN_H2O',
                '4+-Family Public Transit Required': '4F_CNXN_TRANSIT',
                '4+-Family Affordable Only': '4F_AFF',
                '4+-Family Elderly Only': '4F_ELD',
                '4+-Family Min Lot Size': '4F_MIN_LOT',
                '4+-Family Min Lot Size Units': '4F_MIN_LOT_UNITS',
                '3-Family Max Lot Coverage Buildings & Impervious': '3F_MAX_LOT_IMP',
                '3-Family Max Lot Coverage Buildings & Impervious Units': '3F_MAX_LOT_IMP_UNITS',
                '3-Family Min Parking Per Studio/1BR': '3F_PARK_1BR',
                '3-Family Min Parking Per Studio/1BR Units': '3F_PARK_1BR_UNITS',
                '3-Family Min Parking Per 2+ BR': '3F_PARK_2BR',
                '3-Family Min Parking Per 2+ BR Units': '3F_PARK_2BR_UNITS',
                '3-Family Sewer/Water Required': '3F_CNXN_H2O',
                '3-Family Public Transit Required': '3F_CNXN_TRANSIT',
                '3-Family Affordable Only': '3F_AFF',
                '3-Family Elderly Only': '3F_ELD',
                '3-Family Min Lot Size': '3F_MIN_LOT',
                '3-Family Min Lot Size Units': '3F_MIN_LOT_UNITS',
                '2-Family Max Lot Coverage Buildings & Impervious': '2F_MAX_LOT_IMP',
                '2-Family Max Lot Coverage Buildings & Impervious Units': '2F_MAX_LOT_IMP_UNITS',
                '2-Family Min Parking Per Studio/1BR': '2F_PARK_1BR',
                '2-Family Min Parking Per Studio/1BR Units': '2F_PARK_1BR_UNITS',
                '2-Family Min Parking Per 2+ BR': '2F_PARK_2BR',
                '2-Family Min Parking Per 2+ BR Units': '2F_PARK_2BR_UNITS',
                '2-Family Affordable Only': '2F_AFF',
                '2-Family Elderly Only': '2F_ELD',
                '2-Family Min Lot Size': '2F_MIN_LOT',
                '2-Family Min Lot Size Units': '2F_MIN_LOT_UNITS',
                'Most Common Nonresidential Use Permitted': 'COMMON_NONRES_USE'
                        }

editor_column_mapper_supp = {}

for key in editor_column_mapper.keys():
    editor_column_mapper_supp[key.replace('AH', 'Affordable')
        .replace('.', '')
        .replace(' -', '')
        .replace(' #', '')
        .replace(' Housing', '')] = editor_column_mapper[key]

excel_editor = [
    'Bennington_Peru',
    'Caledonia_Barnet',
    'Caledonia_Burke',
    'Caledonia_Danville',
    'Caledonia_Groton',
    'Caledonia_Hardwick',
    'Caledonia_Kirby',
    'Caledonia_Lyndon',
    'Caledonia_Peacham',
    'Caledonia_Ryegate',
    'Caledonia_SaintJohnsbury',
    'Caledonia_Stannard',
    'Caledonia_Sutton',
    'Caledonia_Waterford',
    'Orange_BradfordTown',
    'Orange_Braintree',
    'Orange_Chelsea',
    'Orange_Newbury',
    'Orange_Randolph',
    'Orange_Strafford',
    'Windham_Brattleboro',
    'Windham_Dover',
    'Windham_Londonderry',
    'Windham_Marlboro',
    'Windham_Rockingham',
    'Windham_Stratton',
    'Windham_Wardsboro',
    'Windham_Westminster',
    'Windham_Whitingham',
    'Windham_Wilmington',
    'Windham_Windham'
]

editor_noneditor_mix = [
    'Lamoille_JohnsonTownJohnsonVillage',
    'Washington_Northfield',
    'Windham_Dummerston',
    'Windsor_Chester',
    'Windsor_Hartford',
    'Windsor_Rochester',
    'Windsor_Weathersfield'
]

# In[9]:

# Function to disambiguate treatments
def disambiguate_treatments(df):
    for index, row in df.iterrows():
        if index > 18 and index <= 30:
            df.at[index, 0] = '1F ' + df.loc[index, 0]
        if index > 30 and index <= 46:
            df.at[index, 0] = '2F ' + df.loc[index, 0]
        if index > 46 and index <= 65:
            df.at[index, 0] = '3F ' + df.loc[index, 0]
        if index > 65 and index <= 85:
            df.at[index, 0] = '4F ' + df.loc[index, 0]
        if index > 85 and index <= 105:
            df.at[index, 0] = '5F ' + df.loc[index, 0]
        if index > 105 and index <= 114:
            df.at[index, 0] = 'AFF ' + df.loc[index, 0]
        if index > 114 and index <= 124:
            df.at[index, 0] = 'ADU ' + df.loc[index, 0]
        if index > 124 and index <= 128:
            df.at[index, 0] = 'PRD ' + df.loc[index, 0]
        if index > 128 and index < len(df.columns):
            df.at[index, 0] = 'PUD ' + df.loc[index, 0]
    return(df)

def fix_values(df, valmapper, editor):
    df_copy = df.copy()
    fixed_jxtns = [x.replace('(', '').replace(')', '').replace(' - ', ' ') for x in df_copy['JXTN']]
    df_copy['JXTN'] = fixed_jxtns
    if editor == True:
        try:
            fixed_parent_jxtns = [x.replace('(', '').replace(')', '').replace(' - ', ' ') for x in df_copy['PARENT_JXTN']]
            df_copy['PARENT_JXTN'] = fixed_parent_jxtns
        except:
            pass
    if editor == False:
        df_copy.replace(valmapper, inplace = True)
    return df_copy

def fix_conditionals(df):
    for col in df.columns:
        try:
            if '_COND_ALT' in col and col not in yesno_cols:
                non_cond_col = col[:-9]
                fixed_col = []
                fixed_cond_col = []
                for index, strval in enumerate(df[non_cond_col]):
                    if strval != 'Yes' and strval != 'No' and strval != 't' and strval != 'f':
                        try:
                            fltval = float(strval)
                            fixed_col.append(fltval)
                            fixed_cond_col.append(np.NaN)
                        except:
                            fixed_col.append('')
                            fixed_cond_col.append(strval)
                    else:
                        fixed_col.append(strval)
                        fixed_cond_col.append('')
                df[col] = fixed_cond_col
                df[non_cond_col] = fixed_col
        except:
            print(df[['COUNTY', 'JXTN', 'ABB_DIST_NAME', col]])
            print(df[non_cond_col])
            df = df.drop(col, axis = 'columns', inplace = True)
    return(df)

def drop_annoying_cols(df, cols):
    df_copy = df.copy()
    df_copy.drop(cols, axis='columns', inplace = True)
    return df_copy

joined = '02_joined/'
excel_csvs = 'CSVs'
preprocessed = '00_preprocessed_CSVs'
conds_fixed = '03_conditionals_fixed'
standard_cols = '01_standardized_columns/'
abb_cols = '03_abbreviated_columns'
output_gis_dir = 'geoJSONs_ZONED_nonEditor'
final_individual_layers = 'final_individual_layers'
dirs = [joined, 'geoJSONs_ZONED_complete']
all_zoned_jxtns = []
counter = 0

annoying_editor_columns = [
    'STAT',
    'JXTN_STAT',
    'Jurisdiction Last Updated',
    'STATE',
    'CHANGE_EXP',
    'EXT_DIST'
]

vtplanning_cols = [ '1FDP', '2FDP', '3FDP','4FDP', 'ADUDP', 'AFFDP','PRDDP', 'COUNTY', 'JXTN', 'ABB_DIST_NAME',
                    'DIST_NAME', 'BYLAW_EFF', 'OVER', '3F_CNXN_H2O', '4F_CNXN_H2O', '5F_CNXN_H2O', 'AFF_CNXN_H2O',
                    '3F_CNXN_TRANSIT', '4F_CNXN_TRANSIT', '5F_CNXN_TRANSIT', '1F_MIN_LOT', '2F_MIN_LOT',
                    '3F_MIN_LOT', '4F_MIN_LOT', '5F_MIN_LOT', '2F_MAX_DENS', '3F_MAX_DENS',
                    '4F_MAX_DENS', '5F_MAX_DENS', '1F_MIN_LOT_COND_ALT', '2F_MIN_LOT_COND_ALT',
                    '3F_MIN_LOT_COND_ALT', '4F_MIN_LOT_COND_ALT', '2F_MAX_DENS_COND_ALT',
                    '3F_MAX_DENS_COND_ALT', '4F_MAX_DENS_COND_ALT', 'PRD_MHP',
                    '3F_CNXN_H2O_COND_ALT', '4F_CNXN_H2O_COND_ALT', '5F_CNXN_H2O_COND_ALT', 'AFF_CNXN_H2O_COND_ALT',
                    '3F_CNXN_TRANSIT_COND_ALT', '4F_CNXN_TRANSIT_COND_ALT', '5F_CNXN_TRANSIT_COND_ALT',
                    'geometry']

yesno_cols = ['2F_AFF', '2F_ELD', '3F_AFF', '3F_ELD', '4F_AFF', '4F_ELD', '5F_AFF', '5F_ELD',
              '3F_CNXN_H2O', '4F_CNXN_H2O', '5F_CNXN_H2O', 'AFF_CNXN_H2O',
              '3F_CNXN_TRANSIT', '4F_CNXN_TRANSIT', '5F_CNXN_TRANSIT', 'AFF_CNXN_TRANSIT',
              'AFF_DEF', 'AFF_ELD_ONLY', 'PRD_MHP', 'ADU_EMP_REQD', 'ADU_RENTER_PROH', 'ADU_OWNER_REQD',
              'ADU_ELD', 'ADU_PRIM_STRUC'
              ]

excel_mapper = {'Allowed/Permitted (Hearing not required)': 'Allowed/Conditional',
                'Allowed/Permitted (Hearing Not required)': 'Allowed/Conditional',
                'Public Hearing Required': 'Public Hearing',
                'no': 'No', 'yes': 'Yes', 'Primarily residential': 'Primarily Residential'}

ghost_cols = []
unjoined = []
all_unzoned_jxtns = []
gis_dir = 'geoJSONs_ZONED'
all_zoned_jxtns = []

# for val in sorted(column_mapper.values()):
#     print(val)

# editor_files = gpd.read_file('final_consolidated_layers/Editor_layer.geojson')
# for index, row in editor_files.iterrows():
#     all_zoned_jxtns.append(row)
#
# print('Done with Editor layer')
#
# for file in os.listdir(joined):
#     if file != '.DS_Store':
#         df = gpd.read_file(os.path.join(joined, file))
#         all_zoned_jxtns.append(df)
#         final_layer = gpd.GeoDataFrame(pd.concat(all_zoned_jxtns, ignore_index=True))
#         print('NonEditor district complete')
#
# print('Done with nonEditor layer')
#
# final_layer.to_file('final_consolidated_layers/Editor_nonEditor_join1.geoJSON', driver = 'GeoJSON')

''' STEP ZERO: Join unzoned jxtns into single layer'''

# for file_name in os.listdir('geoJSONs_UNZONED'):
#
#     try:
#         df = gpd.read_file(os.path.join('geoJSONs_UNZONED', file_name), low_memory=False, header=0)
#         all_unzoned_jxtns.append(df)
#     except:
#         print(file_name)
#
#
# final_layer = gpd.GeoDataFrame(pd.concat(all_unzoned_jxtns, ignore_index=True))
#
# final_layer.replace({'Addison County': 'Addison',
#                      'Bennington County': 'Bennington',
#                      'Chittenden County': 'Chittenden',
#                      'Essex County': 'Essex',
#                      'Franklin County': 'Franklin',
#                      'Grand Isle County': 'Grand Isle',
#                      'Lamoille County': 'Lamoille',
#                      'Rutland County': 'Rutland',
#                      'Orange County': 'Orange',
#                      'Orleans County': 'Orleans',
#                      'Washington County': 'Washington',
#                      'Windham County': 'Windham',
#                      'Windsor County': 'Windsor'}, inplace=True)
#
# final_layer.rename({'County': 'COUNTY', 'Jurisdiction': 'JXTN'}, axis = 'columns', inplace=True)
#
# final_layer = final_layer[['COUNTY', 'JXTN', 'geometry']]
#
# final_layer.to_file('final_consolidated_layers/VTZA_unzoned_jxtns_07182024.geojson', driver = 'GeoJSON')

'''STEP ONE: Consolidate attribute tables with geoJSON layers for non-Editor jurisdictions'''

# print('Completely cleaning all geoJSON files prior to merge')

# for file_name in os.listdir(gis_dir):
#     if file_name != '.DS_Store' and file_name != '.DS_Store.xlsx':
#         try:
#             geo_name = ''
#             for word in file_name.split('.')[0:-1]:
#                 geo_name += word
#             gdf = gpd.read_file(os.path.join(gis_dir,file_name))
#             gdf['Does It Have Zoning?'] = 'No'
#             gdf['LAST_UPDATED'] = '7/19/2024'
#             gdf.rename({'County': 'COUNTY', 'Jurisdiction': 'JXTN', 'Abbreviated District Name': 'ABB_DIST_NAME'}, axis = 'columns',
#                        inplace = True)
#             gdf = gdf[['COUNTY', 'JXTN', 'ABB_DIST_NAME', 'geometry']]
#             gdf.to_file(os.path.join(output_gis_dir, geo_name+'_rev.geoJSON'), driver = 'GeoJSON')
#         except:
#             print(file_name)
#
# ''' STEP ONE: Convert .csv's to DataFrames '''
#

update_list = [
    'Bennington_Sandgate',
    'Chittenden_EssexJunction',
    'Chittenden_Richmond',
    'Chittenden_SouthBurlington',
    'Franklin_Fairfax',
    'Rutland_Killington',
    'Washington_Waterbury'
]
# print("Converting all .csv's in the Excel csvs directory")
#
# for file_name in os.listdir(excel_csvs):
#     if file_name != '.DS_Store' and file_name != '.DS_Store.xlsx':
#         county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
#
#         if county_jxtn in update_list:
#
#             df = pd.read_csv(os.path.join(excel_csvs, file_name),
#                                skiprows=[19, 32, 49, 69, 90, 111, 121, 132, 137, 142],
#                                header=None)
#
#             df_copy = df.copy()
#
#             # Disambiguate treatments
#             df_copy = disambiguate_treatments(df_copy)
#
#             # Transpose the DataFrame
#             df_copy = df_copy.transpose()
#             df_copy = df_copy.rename(df_copy.iloc[0][::], axis = 1)
#             df_copy = df_copy.drop(0)
#             df_copy.rename(column_mapper, axis = 'columns', inplace=True)
#             df_copy.rename(editor_column_mapper, axis = 'columns', inplace = True)
#
#             df_final = units_assignment(df_copy)
#
#             df_final = fix_values(df_final, excel_mapper, False)
#             df_final.to_csv('00_preprocessed_CSVs/' + county_jxtn + '_featuresExcel.csv')
#
# for file in os.listdir(preprocessed):
#     if file != '.DS_Store':
#         county_jxtn = file.split('_')[0] + '_' + file.split('_')[1]
#
#         if county_jxtn in update_list:
#
#             df = pd.read_csv(os.path.join(preprocessed, file))
#             df.rename(editor_column_mapper, axis='columns', inplace=True)
#             fix_units = {x: x.replace('_UNITS', '_COND_ALT') for x in df.columns}
#             df.rename(fix_units, axis = 'columns', inplace=True)
#
#             df = fix_conditionals(df)
#
#             df.to_csv('03_conditionals_fixed/' + county_jxtn + '_features_rev080724.csv')

''' STEP TWO: Standardize column labels, fix conditional columns and mismatched values for Editor files'''

# print('Fixing column labels, mismatched values, and conditional values in Editor-joined geoJSONs')
#
# for file_name in os.listdir(joined):
#     if file_name != '.DS_Store':
#         county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
#
#         # Standardize column names
#         gdf = gpd.read_file(os.path.join(os.getcwd(), joined + file_name), low_memory=False, header=0)
#         gdf.rename(editor_column_mapper, axis = 'columns', inplace=True)
#         gdf.rename(column_mapper, axis = 'columns', inplace=True)
#         gdf = fix_conditionals(gdf)
#
#         gdf = fix_values(gdf, {}, True)
#         try:
#             gdf = drop_annoying_cols(gdf, annoying_editor_columns)
#         except:
#             pass
#
#         gdf.to_file('02_joined/' + file_name, driver = 'GeoJSON')

# ''' STEP THREE: Move conditional/alternative values to _COND columns for Excel-originated files '''
#
# print('Now for Excel-originated files')
#
# for file_name in os.listdir(preprocessed):
#     if file_name != '.DS_Store' and file_name != '.DS_Store.xlsx':
#
#         df = pd.read_csv(os.path.join(preprocessed, file_name))
#         fix_units = {x: x.replace('_UNITS', '_COND_ALT') for x in df.columns}
#         df.rename(fix_units, axis = 'columns', inplace=True)
#         df_copy.rename(column_mapper, axis='columns', inplace=True)
#         df_copy.rename(editor_column_mapper, axis='columns', inplace=True)
#
#         df = fix_conditionals(df)
#
#         df.to_csv('03_conditionals_fixed/' + file_name)
#
# print('Finding and joining matching geoJSONs for jurisdictions not pre-joined inside Editor')
#
for file_name in os.listdir(conds_fixed):
    if file_name != '.DS_Store' and file_name != '.DS_Store.xlsx':

        try:
            county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
            if county_jxtn in update_list and '080724' in file_name:

                df = pd.read_csv(os.path.join(conds_fixed, file_name))
                try:
                    # df.rename(editor_column_mapper, axis='columns', inplace=True)
                    df.rename(column_mapper, axis='columns', inplace=True)
                except:
                    print('WTF ' + file_name)

                if '1F_MIN_LOT_COND_ALT' not in df.columns:
                    try:
                        fix_units = {x: x.replace('_UNITS', '_COND_ALT') for x in df.columns}
                        df.rename(fix_units, axis = 'columns', inplace=True)
                    except:
                        break
                    df = fix_conditionals(df)
                    df = fix_values(df, excel_mapper, False)

                try:
                    main_gdf = gpd.read_file('geoJSONs_ZONED_nonEditor/' + county_jxtn + '_rev.geojson')
                except:
                    try:
                        gis_filename = os.path.join(output_gis_dir, county_jxtn + '_rev.geojson')
                        main_gdf = gpd.read_file(gis_filename)
                    except:
                        main_gdf = gpd.read_file('geoJSONs_ZONED_nonEditor/' + county_jxtn + '_rev08072024.geojson')

                gis_files = [main_gdf]
                for gis_file in os.listdir(output_gis_dir):
                    try:
                        mainfilename = county_jxtn + '_rev.geoJSON'
                    except:
                        mainfilename = county_jxtn + '_rev08072024.geoJSON'
                    if county_jxtn in gis_file and gis_file.lower() != mainfilename.lower():
                        gis_files.append(gpd.read_file(os.path.join(output_gis_dir, gis_file)))

                # Concatenate all GIS files together into a single GeoDataFrame
                gdf = gpd.GeoDataFrame(pd.concat(gis_files, ignore_index=True))

                try:
                    df.drop('Unnamed: 0', axis = 'columns', inplace = True)
                except:
                    pass

                if 'JXTN' in df.columns and 'JXTN' in gdf.columns:
                    df.drop('JXTN', axis = 'columns', inplace = True)

                if 'COUNTY' in df.columns and 'COUNTY' in gdf.columns:
                    df.drop('COUNTY', axis = 'columns', inplace = True)

                # Merge the district attribute table with the GIS file
                gdf_joined = gdf.merge(df, on='ABB_DIST_NAME', how='left')

                gdf_joined.replace({'Addison County': 'Addison',
                         'Bennington County': 'Bennington',
                         'Caledonia County': 'Caledonia',
                         'Chittenden County': 'Chittenden',
                         'Essex County': 'Essex',
                         'Franklin County': 'Franklin',
                         'Grand Isle County': 'Grand Isle',
                         'Lamoille County': 'Lamoille',
                         'Rutland County': 'Rutland',
                         'Orleans County': 'Orleans',
                         'Orange County': 'Orange',
                         'Washington County': 'Washington',
                         'Windham County': 'Windham',
                         'Windsor County': 'Windsor'}, inplace = True)

                # Save the joined geoDataFrame as a .geoJSON file
                output_geojson = os.path.join(joined, f'{county_jxtn}_joinednonEditor.geojson')
                pd.set_option('display.max_columns', None)
                gdf_joined.to_file(output_geojson, driver='GeoJSON')
        except:
            unjoined.append(file_name)

for x in unjoined:
    print(x)
print(len(unjoined))

'''STEP FOUR: Save all individual jurisdiction final joined geoJSONs'''

# print('Saving individual jurisdiction files')

# for dir in dirs:
#     for file_name in os.listdir(dir):
#         if file_name != '.DS_Store' and file_name != '.DS_Store.xlsx':
#             county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
#             gdf = gpd.read_file(os.path.join(dir, file_name))
#             gdf.rename(column_mapper, axis='columns', inplace=True)
#             gdf.rename(editor_column_mapper, axis='columns', inplace=True)
#
#             gdf = units_assignment(gdf)
#
#             gdf = fix_values(gdf, excel_mapper, False)
#             rev_filename = 'geoJSONs_ZONED_complete/' + county_jxtn + '.geojson'
#             gdf.to_file(rev_filename, driver='GeoJSON')

'''STEP FIVE: Merge all single jurisdiction layers into a single statewide zoned-jxtn layer'''

# print('Merging all jurisdiction layers into a single statewide layer with full dataset')
#
# for dir in dirs:
#     for file_name in os.listdir(dir):
#             county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
#             try:
#                 df = gpd.read_file(os.path.join(dir, file_name), low_memory=False, header=0)
#                 df.rename(column_mapper, axis='columns', inplace=True)
#                 df.rename(editor_column_mapper, axis='columns', inplace=True)
#                 df.rename(editor_column_mapper_supp, axis = 'columns', inplace = True)
#                 # df = fix_conditionals(df)
#                 try:
#                     df = fix_values(df, excel_mapper, False)
#                 except:
#                     df = fix_values(df, excel_mapper, True)
#                 all_zoned_jxtns.append(df)
#             except:
#                 print(file_name)
#             counter += 1
#
# final_layer = gpd.GeoDataFrame(pd.concat(all_zoned_jxtns, ignore_index=True))
#
# final_layer.replace({'Addison County': 'Addison',
#                      'Bennington County': 'Bennington',
#                      'Caledonia County': 'Caledonia',
#                      'Chittenden County': 'Chittenden',
#                      'Essex County': 'Essex',
#                      'Franklin County': 'Franklin',
#                      'Grand Isle County': 'Grand Isle',
#                      'Lamoille County': 'Lamoille',
#                      'Rutland County': 'Rutland',
#                      'Orleans County': 'Orleans',
#                      'Orange County': 'Orange',
#                      'Washington County': 'Washington',
#                      'Windham County': 'Windham',
#                      'Windsor County': 'Windsor'}, inplace  = True)
#
# for x in final_layer.columns:
#     print(x)
#
# final_layer = fix_values(final_layer, excel_mapper, False)
#
# final_layer.to_file('final_consolidated_layers/VTZA_zoned_jxtns_07182024.geoJSON', driver = 'GeoJSON')
#
# ''' STEP SIX: Subset jxtn files for VT Planning Atlas visualization'''
#
# print('Subsetting full dataset for Vermont Planning Atlas')
#
# final_layer = gpd.read_file('final_consolidated_layers/VTZA_zoned_jxtns_08012024_final.geojson')
#
# for x in final_layer.columns:
#     if x not in vtplanning_cols:
#         final_layer.drop(x, axis = 'columns', inplace = True)
#
# vt_planning_layer = final_layer
# vt_planning_layer.to_file('final_consolidated_layers/VTPlanningAtlas_zoned_jxtns_08022024.geoJSON', driver = 'GeoJSON')