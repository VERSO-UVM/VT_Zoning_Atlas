""" IMPORTS """

import pandas as pd

""" FUNCTION DECLARATIONS """

def disambiguate_treatments(df):
    for index, row in df.iterrows():
        if index > 19 and index < 32:
            df.at[index, 0] = '1F ' + df.loc[index, 0]
        if index > 32 and index < 49:
            df.at[index, 0] = '2F ' + df.loc[index, 0]
        if index > 49 and index < 69:
            df.at[index, 0] = '3F ' + df.loc[index, 0]
        if index > 69 and index < 90:
            df.at[index, 0] = '4F ' + df.loc[index, 0]
        if index > 90 and index < 111:
            df.at[index, 0] = '5F ' + df.loc[index, 0]
        if index > 111 and index < 121:
            df.at[index, 0] = 'AFF ' + df.loc[index, 0]
        if index > 121 and index < 132:
            df.at[index, 0] = 'ADU ' + df.loc[index, 0]
        if index > 132 and index < 137:
            df.at[index, 0] = 'PRD ' + df.loc[index, 0]
        if index > 137 and index < 142:
            df.at[index, 0] = 'PUD ' + df.loc[index, 0]
    return(df)

def standardize_df_column_names(columns):

    column_mapper ={'County' : 'COUNTY',
                    'Jurisdiction': 'JXTN',
                    # : 'PARENT_JXTN'
                    'Abbreviated District Name' : 'ABB_DIST_NAME',
                    'Full District Name' : 'DIST_NAME',
                    # : 'BYLAW_EFF'
                    # : 'CHANGE_EXP'
                    'Mapped But Extinct?' : 'EXT_DIST',
                    'Overlay District?' : 'OVER',
                    'Type of Residential District?' : 'DIST_TYPE',
                    'Affordable Housing District?' : 'AFF_DIST',
                    'Elderly Housing District?' : 'ELD_DIST',
                    '1-Family Allowed?' : '1FDP',
                    '2-Family Allowed?' : '2FDP',
                    '3-Family Allowed?' : '3FDP',
                    '4+-Family Allowed?' : '4FDP',
                    '5+-Family Allowed?' : '5FDP',
                    '1F Minimum Lot Size (acres)' : '1F_MIN_LOT',
                    '1F Minimum Lot Size (acres)' : '1F_MIN_LOT_UNITS',
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
    return [column_mapper.get(col, col) for col in columns]

""" MAIN CODE """

df = pd.read_excel('Orange_Brookfield_features.xlsx', header = None,
                   skiprows=[20, 33, 50, 70, 91, 112, 122, 133, 138, 143]) # might need to adjust skiprows if 0-indexed

df_copy = df.copy()

for i in range(0, len(df.columns), 2):
    df_copy.drop(i, axis = 'columns', inplace=True)

disambiguate_treatments(df_copy)

## Figure out how to handle the Units columns!
## Transpose the table

standardize_df_column_names(df_copy)
