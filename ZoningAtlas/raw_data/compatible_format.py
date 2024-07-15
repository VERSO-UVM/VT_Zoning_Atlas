import pandas as pd
import os
import re

for file in os.listdir('Editor_legacy/district_boundaries'):
    thisfile = file.split('CountyVT')[0]
    res_list = re.findall('[A-Z][^A-Z]*', thisfile)
    thiscounty = res_list[-1]
    jurisdiction = ''
    if len(res_list) > 2:
        for word in res_list[0:-1]:
            jurisdiction += word
    else:
        jurisdiction = res_list[0]
    filename = thiscounty + '_' + jurisdiction + '_joined.geojson'
    old_file = os.path.join("Editor_legacy/district_boundaries", file)
    new_file = os.path.join("Editor_legacy/temp", filename)
    os.rename(old_file, new_file)

