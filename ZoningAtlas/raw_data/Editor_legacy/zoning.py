import os
import pandas as pd
import geopandas as gpd
import numpy as np


# In[7]:

def units_assignment(df):
    df_copy = df.copy()
    thisdistrict = ''
    thesecolvals = []
    columns = [str(x) + '_UNITS' for x in df_copy.columns[19::]]
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

geopkg_mapper = {
                'county': 'COUNTY',
                'jurisdiction': 'JXTN',
                # : 'PARENT_JXTN'
                'abbrvname': 'ABB_DIST_NAME',
                'name': 'DIST_NAME',
                'extinct': 'EXT_DIST',
                'overlay': 'OVER',
                'mapped': 'DIST_MAP',
                'type': 'DIST_TYPE',
                'affordable_district': 'AFF_DIST',
                'elderly_district': 'ELD_DIST',
                # 'NOTES',
                'family1_treatment': '1FDP',
                'family2_treatment': '2FDP',
                'family3_treatment': '3FDP',
                'family4_treatment': '4FDP',
                '5+-Family Allowed?' : '5FDP',
                'family1_minlotacres':'1F_MIN_LOT',
                'family1_frontsetbackft': '1F_FSET',
                 # '1F_FSET_UNITS',
                'family1_sidesetbackft': '1F_SSET',
                # : '1F_SSET_UNITS',
                'family1_rearsetbackft': '1F_RSET',
                # : '1F_RSET_UNITS',
                'family1_maxlotcoverage_building': '1F_MAX_LOT_BLDG',
                # : '1F_MAX_LOT_BLDG_UNITS'
                'family1_maxlotcoverage_buildingimpervious': '1F_MAX_LOT_IMP',
                # : '1F_MAX_LOT_IMP_UNITS'
                'family1_minparking': '1F_PARK',
                # : '1F_PARK_UNITS',
                'family1_maxstories': '1F_STORIES',
                # : '1F_STORIES_UNITS',
                'family1_maxheightft': '1F_HEIGHT',
                # : '1F_HEIGHT_UNITS',
                'family1_floorarearatio':'1F_FTA',
                # : '1F_FTA_UNITS',
                'family1_minunitsqft': '1F_MIN_UNIT',
                # : '1F_MIN_UNIT_UNITS',
                'family2_affordable_only': '2F_AFF',
                'family2_elderly_only': '2F_ELD',
                'family2_minlotacres': '2F_MIN_LOT',
                # : '2F_MIN_LOT_UNITS',
                'family2_maxunitsperacre': '2F_MAX_DENS',
                # : '2F_MAX_DENS_UNITS',
                'family2_frontsetbackft': '2F_FSET',
                # : '2F_FSET_UNITS',
                'family2_sidesetbackft': '2F_SSET',
                # : '2F_SSET_UNITS',
                'family2_rearsetbackft': '2F_RSET',
                # : '2F_RSET_UNITS',
                'family2_maxlotcoverage_building': '2F_MAX_LOT_BLDG',
                # : '2F_MAX_LOT_BLDG_UNITS',
                'family2_maxlotcoverage_buildingimpervious': '2F_MAX_LOT_IMP',
                # : '2F_MAX_LOT_IMP_UNITS',
                'family2_minparking_1br': '2F_PARK_1BR',
                # : '2F_PARK_1BR_UNITS',
                'family2_minparking_2br': '2F_PARK_2BR',
                # : '2F_PARK_2BR_UNITS',
                'family2_maxstories': '2F_STORIES',
                # : '2F_STORIES_UNITS',
                'family2_maxheightft': '2F_HEIGHT',
                # : '2F_HEIGHT_UNITS',
                'family2_floorarearatio': '2F_FTA',
                # : '2F_FTA_UNITS',
                'family2_minunitsqft': '2F_MIN_UNIT',
                # : '2F_MIN_UNIT_UNITS',
                'family3_affordable_only': '3F_AFF',
                'family3_elderly_only': '3F_ELD',
                'family3_minlotacres': '3F_MIN_LOT',
                # : '3F_MIN_LOT_UNITS',
                'family3_maxunitsperacre': '3F_MAX_DENS',
                # : '3F_MAX_DENS_UNITS',
                'family3_frontsetbackft': '3F_FSET',
                # : '3F_FSET_UNITS',
                'family3_sidesetbackft': '3F_SSET',
                # : '3F_SSET_UNITS',
                'family3_rearsetbackft': '3F_RSET',
                # : '3F_RSET_UNITS',
                'family3_maxlotcoverage_building': '3F_MAX_LOT_BLDG',
                # : '3F_MAX_LOT_BLDG_UNITS',
                'family3_maxlotcoverage_buildingimpervious': '3F_MAX_LOT_IMP',
                # : '3F_MAX_LOT_IMP_UNITS',
                'family3_minparking_1br': '3F_PARK_1BR',
                # : '3F_PARK_1BR_UNITS',
                'family3_minparking_2br': '3F_PARK_2BR',
                # : '3F_PARK_2BR_UNITS',
                'family3_water_required': '3F_CNXN_H2O',
                'family3_transit_required': '3F_CNXN_TRANSIT',
                'family3_maxstories': '3F_STORIES',
                # : '3F_STORIES_UNITS',
                'family3_maxheightft': '3F_HEIGHT',
                # : '3F_HEIGHT_UNITS',
                'family3_floorarearatio': '3F_FTA',
                # : '3F_FTA_UNITS',
                'family3_minunitsqft': '3F_MIN_UNIT',
                # : '3F_MIN_UNIT_UNITS',
                'family3_maxbedrooms': '3F_BEDROOMS',
                # : '3F_BEDROOMS_UNITS',
                'family4_affordable_only':'4F_AFF',
                'family4_elderly_only': '4F_ELD',
                'family4_minlotacres': '4F_MIN_LOT',
                # : '4F_MIN_LOT_UNITS',
                'family4_maxunitsperacre': '4F_MAX_DENS',
                # : '4F_MAX_DENS_UNITS',
                'family4_frontsetbackft':'4F_FSET',
                # : '4F_FSET_UNITS',
                'family4_sidesetbackft': '4F_SSET',
                # : '4F_SSET_UNITS',
                'family4_rearsetbackft':'4F_RSET',
                # : '4F_RSET_UNITS',
                'family4_maxlotcoverage_building': '4F_MAX_LOT_BLDG',
                # : '4F_MAX_LOT_BLDG_UNITS',
                'family4_maxlotcoverage_buildingimpervious': '4F_MAX_LOT_IMP',
                # : '4F_MAX_LOT_IMP_UNITS',
                'family4_minparking_1br':'4F_PARK_1BR',
                # : '4F_PARK_1BR_UNITS',
                'family4_minparking_2br': '4F_PARK_2BR',
                # : '4F_PARK_2BR_UNITS',
                'family4_water_required': '4F_CNXN_H2O',
                'family4_transit_required': '4F_CNXN_TRANSIT',
                'family4_maxstories': '4F_STORIES',
                # : '4F_STORIES_UNITS',
                'family4_maxheightft': '4F_HEIGHT',
                # : '4F_HEIGHT_UNITS',
                'family4_floorarearatio': '4F_FTA',
                # : '4F_FTA_UNITS',
                'family4_minunitsqft': '4F_MIN_UNIT',
                # : '4F_MIN_UNIT_UNITS',
                'family4_maxbedrooms': '4F_BEDROOMS',
                # : '4F_BEDROOMS_UNITS',
                'family4_maxunitsperbldg': '4F_MAX_UNITS',
                # : '4F_MAX_UNITS_UNITS',
                'affordable_treatment': 'AFFDP',
                'affordable_definition': 'AFF_DEF',
                'affordable_elderly_only':'AFF_ELD_ONLY',
                'affordable_minlotacres': 'AFF_MIN_LOT',
                # : 'AFF_MIN_LOT_UNITS',
                'affordable_maxunitsperacre': 'AFF_MAX_DENS',
                # : 'AFF_MAX_DENS_UNITS',
                'affordable_minparking_1br': 'AFF_PARK_1BR',
                # : 'AFF_PARK_1BR_UNITS',
                'affordable_minparking_2br': 'AFF_PARK_2BR',
                # : 'AFF_PARK_2BR_UNITS',
                'affordable_water_required': 'AFF_CNXN_H2O',
                'affordable_transit_required': 'AFF_CNXN_TRANSIT',
                'affordable_minunitsqft': 'AFF_MIN_UNIT',
                # : 'AFF_MIN_UNIT_UNITS',
                'affordable_maxbedrooms': 'AFF_BEDROOMS',
                # : 'AFF_BEDROOMS_UNITS',
                'affordable_maxunitsperbldg': 'AFF_MAX_UNITS',
                # : 'AFF_MAX_UNIT_UNITS',
                'accessory_treatment': 'ADUDP',
                'accessory_family_required': 'ADU_EMP_REQD',
                'accessory_renter_prohibited': 'ADU_RENTER_PROH',
                'accessory_owner_required': 'ADU_OWNER_REQD',
                'accessory_elderly_only': 'ADU_ELD',
                'accessory_minlotacres': 'ADU_MIN_LOT',
                # : 'ADU_MIN_LOT_UNITS',
                'accessory_minparking': 'ADU_PARK',
                # : 'ADU_PARK_UNITS',
                'accessory_primarystructure_only':'ADU_PRIM_STRUC',
                'accessory_maxpercent': 'ADU_MAX_PCT',
                # : 'ADU_MAX_PCT_UNITS',
                'accessory_maxsqft': 'ADU_MAX_SIZE',
                # : 'ADU_MAX_SIZE_UNITS',
                'accessory_maxbedrooms': 'ADU_BEDROOMS',
                # : 'ADU_BEDROOMS_UNITS',
                'plannedresidential_treatment': 'PRDDP',
                'plannedresidential_mobilehome': 'PRD_MHP',
                'plannedresidential_minlotacres': 'PRD_MIN_LOT',
                # : 'PRD_MIN_LOT_UNITS',
                'plannedresidential_maxunitsperacre': 'PRD_MAX_DENS',
                # : 'PRD_MAX_DENS_UNITS',
                'plannedresidential_maxunits': 'PRD_MAX_UNITS',
                # : 'PRD_MAX_UNITS_UNITS',
                'specialnotes': 'SPNOTES',
                'tooltipnotes': 'TTIPNOTES',
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
                '5F Max. Units Per Building' : '5F_MAX_UNITS',
                'Base residential density (units/acre)' : 'BASE_DENS',
                '1F Frontage (ft)' : '1F_FRONT',
                '2F Frontage (ft)' : '2F_FRONT',
                '3F Frontage (ft)' : '3F_FRONT',
                '4F Frontage (ft)' : '4F_FRONT',
                '5F Frontage (ft)' : '5F_FRONT',
                'PUD PUD required with Subdivision' : 'PUD_SUBDV',
                'PUD PUD Threshold #' : 'PUD_THRESH',
                'PUD PUD Allowed' : 'PUD_ALLOW',
                'PUD PUD requiring land conservation' : 'PUD_CONSERVE',
#                 # : 'GIS_ID'
}
# }

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
                '4F Max. Units Per Building' : '4F_MAX_UNITS',
                # : '4F_MAX_UNITS_UNITS',
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
                'AFF Max. Units Per Building' : 'AFF_MAX_UNITS',
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
                'PRD Max. Units' : 'PRD_MAX_UNITS',
                # : 'PRD_MAX_UNITS_UNITS',
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
                '5F Max. Units Per Building' : '5F_MAX_UNITS',
                'Base residential density (units/acre)' : 'BASE_DENS',
                '1F Frontage (ft)' : '1F_FRONT',
                '2F Frontage (ft)' : '2F_FRONT',
                '3F Frontage (ft)' : '3F_FRONT',
                '4F Frontage (ft)' : '4F_FRONT',
                '5F Frontage (ft)' : '5F_FRONT',
                'PUD PUD required with Subdivision' : 'PUD_SUBDV',
                'PUD PUD Threshold #' : 'PUD_THRESH',
                'PUD PUD Allowed' : 'PUD_ALLOW',
                'PUD PUD requiring land conservation' : 'PUD_CONSERVE',
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
                 '1-Family Min. Lot Units': '1F_MIN_LOT_UNITS',
                 '1-Family Front Setback': '1F_FSET',
                 '1-Family Front Setback Units': '1F_FSET_UNITS',
                 '1-Family Side Setback': '1F_SSET',
                 '1-Family Side Setback Units': '1F_SSET_UNITS',
                 '1-Family Rear Setback': '1F_RSET',
                 '1-Family Rear Setback Units': '1F_RSET_UNITS',
                 '1-Family Max. Lot Coverage - Buildings': '1F_MAX_LOT_BLDG',
                 '1-Family Max. Lot Coverage - Buildings Units': '1F_MAX_LOT_BLDG_UNITS',
                 '1-Family Max. Lot Coverage - Buildings & Impervious Surface': '1F_MAX_LOT_IMP',
                 '1-Family Max. Lot Coverage - Buildings & Impervious Surface Units': '1F_MAX_LOT_IMP_UNITS',
                 '1-Family Min. # Parking Spaces': '1F_PARK',
                 '1-Family Min. # Parking Spaces Units': '1F_PARK_UNITS',
                 '1-Family Max. Stories': '1F_STORIES',
                 '1-Family Max. Stories Units': '1F_STORIES_UNITS',
                 '1-Family Max. Height': '1F_HEIGHT',
                 '1-Family Max. Height Units': '1F_HEIGHT_UNITS',
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
                 '4+-Family Min. Parking Spaces Per 2+ BR Units': '4F_PARK_2BR_UNITS',
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
                 '4+-Family Max. Units': '4F_MAX_UNITS',
                 '4+-Family Max. Units Units': '4F_MAX_UNITS_UNITS',
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
                 'AH Max. Units': 'AFF_MAX_UNITS',
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
                 'ADU Max. Size Units': 'ADU_MAX_SIZE_UNITS',
                 'ADU Max. Bedrooms': 'ADU_BEDROOMS',
                 'ADU Max. Bedrooms Units': 'ADU_BEDROOMS_UNITS',
                 'Planned Residential Development (PRD) Treatment': 'PRDDP',
                 'Mobile or Manufactured Home Park': 'PRD_MHP',
                 'PRD Min. Lot': 'PRD_MIN_LOT',
                 'PRD Min. Development Size': 'PRD_MIN_LOT',
                 'PRD Min. Lot Units': 'PRD_MIN_LOT_UNITS',
                 'PRD Max. Density': 'PRD_MAX_DENS',
                 'PRD Max. Density Units': 'PRD_MAX_DENS_UNITS',
                 'PRD Max. Units': 'PRD_MAX_UNITS',
                 'PRD Max. Units Per Development Units': 'PRD_MAX_UNITS_UNITS',
                 'PRD Max. Units Units': 'PRD_MAX_UNITS_UNITS',
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
                 '5+Family Max. # Units Per Building': '5F_MAX_UNITS',
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
                 'Unique GIS schema identifier': 'GIS_ID'}

# In[9]:


# Function to disambiguate treatments
def disambiguate_treatments(df):
    for index, row in df.iterrows():
        if index > 18 and index <= 30:
            df.at[index, 0] = '1F ' + df.loc[index, 0]
        if index > 30 and index <= 47:
            df.at[index, 0] = '2F ' + df.loc[index, 0]
        if index > 47 and index <= 67:
            df.at[index, 0] = '3F ' + df.loc[index, 0]
        if index > 67 and index <= 88:
            df.at[index, 0] = '4F ' + df.loc[index, 0]
        if index > 88 and index <= 109:
            df.at[index, 0] = '5F ' + df.loc[index, 0]
        if index > 109 and index <= 114:
            df.at[index, 0] = 'AFF ' + df.loc[index, 0]
        if index > 114 and index <= 124:
            df.at[index, 0] = 'ADU ' + df.loc[index, 0]
        if index > 124 and index <= 128:
            df.at[index, 0] = 'PRD ' + df.loc[index, 0]
        if index > 128 and index < len(df.columns):
            df.at[index, 0] = 'PUD ' + df.loc[index, 0]
    return(df)


# In[ ]:

# atlas_list = []
#
# for filename in os.listdir('../ATLAS_READY/Editor_cleaned_district_boundaries_geoJSON'):
#     try:
#         atlas_list.append(gpd.read_file('../ATLAS_READY/Editor_cleaned_district_boundaries_geoJSON/' + filename))
#     except:
#         print(filename)
#
# for filename in os.listdir('../ATLAS_READY/Excel_cleaned_district_boundaries_geoJSON'):
#     try:
#         atlas_list.append(gpd.read_file('../ATLAS_READY/Excel_cleaned_district_boundaries_geoJSON/' + filename))
#     except:
#         print(filename)
#
# Atlas_layer = gpd.GeoDataFrame(pd.concat(atlas_list, ignore_index=True))
#
# Atlas_layer.to_file('atlas_layer.geoJSON', driver = 'GeoJSON')

atlas_layer = gpd.read_file('../ATLAS_READY/atlas_layer.geoJSON')
# columns_to_drop = []
# fix_these_cols = {'COUNTY_left': 'COUNTY', 'JXTN_left': 'JXTN', 'JXTN_right': 'JXTN',
#                   'COUNTY_right': 'COUNTY', 'PUD required with Subdivision_left': 'PUD_SUBDV',
#                   'PUD Threshold #_left': 'PUD_THRESH', 'PUD requiring land conservation_left': 'PUD_CONSERVE',
#                   'PUD required with Subdivision_right': 'PUD_SUBDV', 'PUD Threshold #_right': 'PUD_THRESH',
#                   'PUD requiring land conservation_right': 'PUD_CONSERVE'}
#
# for key, val in editor_column_mapper.items():
#     print(key)
#     for index, row in atlas_layer.iterrows():
#         try:
#             if row[key] != np.NaN:
#                 atlas_layer.at[index, val] == row[key]
#                 columns_to_drop.append(key)
#         except:
#             print('This key isn\'t in column labels')
#
# for key, val in fix_these_cols.items():
#     print(key)
#     for index, row in atlas_layer.iterrows():
#         try:
#             if row[key] != np.NaN:
#                 atlas_layer.at[index, val] == row[key]
#                 columns_to_drop.append(key)
#         except:
#             print('This key isn\'t in column labels')
#
# atlas_layer.replace({'Addison County': 'Addison',
#                      'Bennington County': 'Bennington',
#                      'Chittenden County': 'Chittenden',
#                      'Franklin County': 'Franklin',
#                      'Grand Isle County': 'Grand Isle',
#                      'Lamoille County': 'Lamoille',
#                      'Rutland County': 'Rutland',
#                      'Orange County': 'Orange',
#                      'Washington County': 'Washington',
#                      'Windham County': 'Windham',
#                      'Windsor County': 'Windsor'}, inplace  = True)
#
# columns_to_drop = set(columns_to_drop)
# columns_to_drop = list(columns_to_drop)
#
# atlas_layer.drop(columns_to_drop, axis='columns', inplace = True)
# atlas_layer.drop(['Shape_Length', 'Shape_Area', 'FID_1', 'Shape__Are', 'Shape__Len', 'st_area(Shape)',
#                   'st_perimeter(Shape)', '.'],
#                   axis = 'columns', inplace = True)
#
# print('\n\n\nREMAINING COLUMNS LABELS\n')
for x in atlas_layer.columns:
    print(x)

# atlas_layer.to_file('atlas_layer_cols_fixed.geoJSON', driver = 'GeoJSON')


# print(atlas_layer['4FDP'].unique())

# atlas_layer.to_file('atlas_layer.geoJSON', driver = 'GeoJSON')

# Read the "Districts" worksheet into a DataFrame
# input_dir = '../districts_needs_to_join_csv'
# gis_dir = '../ATLAS_READY/gis_needs_to_join'
#
# unjoined = []
#
#
# # Windsor_Pomfret
# # Orleans_NewportCity
# # Windsor_Weston
#
# for file_name in os.listdir(input_dir):
#     if file_name != '.DS_Store' and file_name != '.DS_Store.xlsx':
#         county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
#
#         df = pd.read_csv(os.path.join(input_dir, file_name),
#                            skiprows=[19, 32, 49, 69, 90, 111, 121, 132, 137, 142],
#                            header=None)
#
#         df_copy = df.copy()
#
#         # Disambiguate treatments
#         df_copy = disambiguate_treatments(df_copy)
#
#         # Transpose the DataFrame
#         df_copy = df_copy.transpose()
#         df_copy = df_copy.rename(df_copy.iloc[0][::], axis = 1)
#         df_copy = df_copy.drop(0)
#         df_copy.rename(column_mapper, axis = 'columns', inplace=True)
#
#         df_final = units_assignment(df_copy)
#         df_final.to_csv('../ATLAS_READY/Excel_cleaned/' + county_jxtn + '.csv')
#
#         # try:
#
#         # Find and join matching geoJSONs for jurisdiction
#         gis_filename = os.path.join(gis_dir, county_jxtn + '.geojson')
#         try:
#             try:
#                 main_gdf = gpd.read_file(gis_filename)
#             except:
#                 main_gdf = gpd.read_file('../Editor_legacy/district_boundaries/' + county_jxtn + '.geojson')
#                 main_gdf = main_gdf[['Jurisdiction', 'County', 'Abbreviated District Name', 'geometry']]
#
#             gis_files = [main_gdf]
#             for gis_file in os.listdir(gis_dir):
#                 # gis_stub = os.path.join(gis_dir, county_jxtn)
#                 if county_jxtn in gis_file and gis_file != (county_jxtn + '.geojson'):
#                     gis_files.append(gpd.read_file(os.path.join(gis_dir, gis_file)))
#
#             # Concatenate all GIS files together into a single GeoDataFrame
#             gdf = gpd.GeoDataFrame(pd.concat(gis_files, ignore_index=True))
#
#             # Merge the district attribute table with the GIS file
#             gdf_joined = gdf.merge(df_final, left_on = 'Abbreviated District Name', right_on = 'ABB_DIST_NAME', how='left', suffixes = ('_left', '_right'))
#             # gdf_joined = gdf_joined.drop(['OBJECTID', 'COUNTY'], axis = 'columns')
#
#             gdf_joined = check_dupe_columns(gdf_joined)
#
#             # Save the joined geoDataFrame as a .geoJSON file
#             output_geojson = os.path.join('../ATLAS_READY/Excel_cleaned_district_boundaries_geoJSON', f'{county_jxtn}_joined.geojson')
#             gdf_joined.to_file(output_geojson, driver='GeoJSON')
#         except:
#             unjoined.append(file_name)
#
# for x in sorted(unjoined):
#     print(x)
# print(len(unjoined))

        # except:
        #     with open('unjoined_jxtns.txt', 'w') as f:
        #         missing_jxtn = county_jxtn
        #         f.write(missing_jxtn)
        #     f.close()
        #     print(missing_jxtn)

# geopackage_dir = 'Editor_formatted/geodatabase_complete_state_052324'
# gdf = gpd.read_file(os.path.join(geopackage_dir, 'vermont_districts.gpkg'))
# gdf.rename(geopkg_mapper, axis = 'columns', inplace = True)
# filename = geopackage_dir + '_rev.gpkg'
# gdf.to_file(filename, driver = 'GPKG')

# editor_dir = 'Editor_legacy/district_boundaries/'

# for file_name in os.listdir(editor_dir):
#     county_jxtn = file_name.split('_')[0] + '_' + file_name.split('_')[1]
#
#     # Standardize column names
#     df = pd.read_csv(editor_dir + file_name, sep = ',', low_memory=False, header=0)
#     df.rename(editor_column_mapper, axis = 'columns', inplace=True)
#     df.set_index('ABB_DIST_NAME', inplace=True)
#
#     df.to_csv('Editor_cleaned/district_boundaries_preclean/' + county_jxtn + '.csv')

# gis_dir = 'temp'
# temp_dir = '../ATLAS_READY/Editor_cleaned_district_boundaries_geoJSON'
#
# for gis_file in os.listdir(os.path.join(os.getcwd(), gis_dir)):
#     if gis_file != 'S__joined.geojson_Store_D_joined.geojson' and gis_file != '.DS_Store':
#         try:
#             filename = os.path.join(gis_dir, gis_file)
#             filename_no_extension = gis_file.split('.')[0]
#             thisgdf = gpd.read_file(filename)
#             thisgdf = thisgdf.rename(editor_column_mapper, axis = 'columns', copy = True)
#             revfilename = f'{filename_no_extension}_rev.geojson'
#             revfilename = os.path.join(temp_dir, revfilename)
#             # thisgdf = check_dupe_columns(thisgdf)
#             thisgdf.to_file(revfilename, driver = 'GeoJSON')
#         except:
#             print(gis_file)