import arcpy
def main():
    district = input("Enter the name of your town district: ")
    #For confirmation of correct district input
    print(district)
    #calling the geoProccesses for district
    geoProcesses(district)

#Zack's workflow to be turned into script:

def geoProcesses(town):

    #project shapefile
    arcpy.management.Project(town, town+'_32145', '32145')


    #project TIGER
    arcpy.management.Project('TIGER', 'TIGER_32145', '32145')
    #arcpy command to repair geometry for both the TIGER and 32145
    arcpy.management.RepairGeometry(town+'.gdb/'+town+'_32145')
    arcpy.management.RepairGeometry(town+'.gdb/TIGER_32145')
    #arcpy command to enable snaping and set snap tolerance to like 100
    #maybe just do this manually

    #arcpy command to snap vertex for like 50 meters
    #arcpy command to snap edge for like 50 meters
    arcpy.edit.Snap(town+'.gdb/'+town+'_32145',
            [[town+'.gdb/TIGER_32145', 'VERTEX', '50 Meters'],
            [town+'.gdb/TIGER_32145', 'EDGE', '50 Meters']])

    #Topology must be last step before manual edits. Datasets LOCK FEATURE CLASSES IN.
    #create dataset
    arcpy.management.CreateFeatureDataset(town+'.gdb', town)

    #move files into dataset
    arcpy.management.TransferFiles(town+'.gdb/'+town+'_32145', town+'.gdb/'+town,)
    arcpy.management.TransferFiles(town+'.gdb/TIGER_32145', town+'.gdb/'+town,)

    #create overlap/gap topology
    arcpy.management.CreateTopology(town+'.gdb/'+town, town+'_Zoning_Topology', '1')

    #add 32145 to overlap/gap topology
    arcpy.management.AddFeatureClassToTopology(town+'.gdb/'+town+'/'+town+'_Zoning_Topology', town+'.gdb/'+town+'/'+town+'_32145', '1', '1')

    #add rules to overlap/gap
    arcpy.management.AddRuleToTopology(town+'.gdb/'+town+'/'+town+'_Zoning_Topology', 'Must Not Have Gaps (Area)', town+'.gdb/'+town+'/'+town+'_32145')
    arcpy.management.AddRuleToTopology(town+'.gdb/'+town+'/'+town+'_Zoning_Topology', 'Must Not Overlap (Area)', town+'.gdb/'+town+'/'+town+'_32145')
    
main()
