#importing arcpy tools
import arcpy


# before further work: https://learn.arcgis.com/en/projects/automate-a-geoprocessing-workflow-with-python/





#Zack's workflow to be turned into script:

# #project shapefile
# arcpy.managment.Project(‘.shp file’, ‘Town_32145’, ‘32145’)
# #project TIGER
# arcpy.managment.Project(‘TIGER file’, ‘TIGER_32145’, ‘32145’)
# #arcpy command to repair geometry for both the TIGER and 32145
# arcpy.management.RepairGeometry(‘Town.gdb/Town_32145’)
# arcpy.management.RepairGeometry(‘Town.gdb/TIGER_32145’)
# #arcpy command to enable snaping and set snap tolerance to like 100
# #maybe just do this manually

# #arcpy command to snap vertex for like 50 meters
# #arcpy command to snap edge for like 50 meters
# arcpy.edit.Snap(‘Town.gdb/Town_32145’,
#         [[‘Town.gdb/TIGER_32145’, ‘VERTEX’, ’50 Meters’],
#          [‘Town.gdb/TIGER_32145’, ‘EDGE’, ’50 Meters’]])

# #Topology must be last step before manual edits. Datasets LOCK FEATURE CLASSES IN, because administration hates the working man! Idk its stupid. //
# #create dataset
# arcpy.managment.CreateFeatureDataset(‘Town.gdb’, ‘Town’)

# #move files into dataset
# arcpy.management.TransferFiles(‘Town.gdb/Town_32145’, ‘Town.gdb/Town’,)
# arcpy.management.TransferFiles(‘Town.gdb/TIGER_32145’, ‘Town.gdb/Town’,)

# #create overlap/gap topology
# arcpy.managment.CreateTopology(‘Town.gdb/Town’, ‘Town_Zoning_Topology’, ‘1’)

# #add 32145 to overlap/gap topology
# arcpy.managment.AddFeatureClassToTopology(‘Town.gdb/Town/Town_Zoning_Topology’, ‘Town.gdb/Town/Town_32145’, ‘1’, ‘1’)

# #add rules to overlap/gap
# arcpy.managment.AddRuleToTopology(‘Town.gdb/Town/Town_Zoning_Topology’, ‘Must Not Have Gaps (Area)’, ‘Town.gdb/Town/Town_32145’)
# arcpy.managment.AddRuleToTopology(‘Town.gdb/Town/Town_Zoning_Topology’, ‘Must Not Overlap (Area)’, ‘Town.gdb/Town/Town_32145’)