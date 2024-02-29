import arcpy
def main():
    jurisdiction = input("Enter the name of your town jurisdiction: ")
    #For confirmation of correct jurisdiction input
    print(jurisdiction)
    #calling the geoProccesses for jurisdiction
    geoProcesses(jurisdiction)

#Zack's workflow to be turned into script:

def geoProcesses(town):
    
    
    #create mobile geodatabase to avoid issues with locks
    arcpy.management.CreateMobileGDB(arcpy.mp.ArcGISProject("CURRENT").filePath, town+'_mobile.gdb')
    
    
    #BEFORE ANYTHING ELSE GETS CODED WE NEED A WAY TO ACCESS THE PATH TO THE PROJECT FOLDER
        #we need to also import the .shp file and 'json to features' tool that TIGER
    
    #project shapefile
 #   arcpy.management.Project(town, town+'_32145', '32145')


    #project TIGER
 #  arcpy.management.Project('TIGER', 'TIGER_32145', '32145')
    #arcpy command to repair geometry for both the TIGER and 32145
 #  arcpy.management.RepairGeometry(town+'.gdb/'+town+'_32145')
 #  arcpy.management.RepairGeometry(town+'.gdb/TIGER_32145')
    #arcpy command to enable snaping and set snap tolerance to like 100
    #maybe just do this manually

    #arcpy command to snap vertex for like 50 meters
    #arcpy command to snap edge for like 50 meters
 #   arcpy.edit.Snap(town+'.gdb/'+town+'_32145',
 #           [[town+'.gdb/TIGER_32145', 'VERTEX', '50 Meters'],
 #           [town+'.gdb/TIGER_32145', 'EDGE', '50 Meters']])

    #Topology must be last step before manual edits. Datasets LOCK FEATURE CLASSES IN.
    #create dataset
    sr = arcpy.SpatialReference(32145)
    arcpy.management.CreateFeatureDataset(town+'.gdb', town, sr)

    #move files into dataset
#    arcpy.management.Copy(town+'_mobile.gdb/'+town+'_32145', town+'_mobile.gdb/'+town,)
 #   arcpy.management.Copy(town+'_mobile.gdb/TIGER_32145', town+'_mobile.gdb/'+town,)

    #create overlap/gap topology
#    arcpy.management.CreateTopology(town+'_mobile.gdb/'+town, town+'_Zoning_Topology', '1')

    #add 32145 to overlap/gap topology
#    arcpy.management.AddFeatureClassToTopology(town+'_mobile.gdb/'+town+'1'+'/'+town+'_Zoning_Topology', town+'_mobile.gdb/'+town+'1'+'/'+town+'_32145', '1', '1')

    #add rules to overlap/gap
#    arcpy.management.AddRuleToTopology(town+'_mobile.gdb/'+town+'/'+town+'_Zoning_Topology', 'Must Not Have Gaps (Area)', town+'_mobile.gdb/'+town+'/'+town+'_32145')
#    arcpy.management.AddRuleToTopology(town+'_mobile.gdb/'+town+'/'+town+'_Zoning_Topology', 'Must Not Overlap (Area)', town+'_mobile.gdb/'+town+'/'+town+'_32145')
    
main()
