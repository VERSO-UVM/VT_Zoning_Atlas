import arcpy
import os.path
def main():
    jurisdiction = input("Enter the name of your town jurisdiction: ")
    
    #needed global variables
    filePath = arcpy.mp.ArcGISProject("CURRENT").filePath 
    dirName = os.path.dirname(filePath)
    downloaded = dirName+'/Downloaded'

    #file management, projection, and TIGER
    geoFileManagement(jurisdiction, downloaded)

    next = input("Ready for geo proccesses?(t/f):").lower()
    while next not in ["t", "f"]:
        next = input("Check for valid input \n Ready for geo proccesses?(t/f):").lower()

    if next == "t":
        Topology(dirName, jurisdiction)

    
#Zack's workflow to be turned into script:

def geoFileManagement(town, downloaded):
   
    # Part 1: Files geodatabase and snapping

    # .shp files to file geodatabase 
    arcpy.conversion.FeatureClassToGeodatabase(downloaded+'/VT_Data_-_'+town+'_Zoning-shp/VT_Data_-_'+town+'_Zoning.shp', town+'.gdb')
    
    #project shapefile
    arcpy.management.Project(town+'.gdb/VT_Data___'+town+'_Zoning', town+'_32145', '32145')
   
    # geojson file to features to file geodatabase (rename json file to "TIGER.geojson")
    arcpy.conversion.JSONToFeatures(downloaded+'/TIGER2.geojson', 'TIGER2')
    
    #project TIGER
    arcpy.management.Project(town+'.gdb/TIGER2', 'TIGER_32145', '32145')
    
    #arcpy command to repair geometry for both the TIGER and 32145
    arcpy.management.RepairGeometry(town+'.gdb/'+town+'_32145')
    arcpy.management.RepairGeometry(town+'.gdb/TIGER_32145')

    print("Finished geoFileManagemet\n")
    #break

def Topology(dirName, town):
    #Part 2 : create mobile geodatabase and topology
    
    #create mobile geodatabase to avoid issues with locks
    arcpy.management.CreateMobileGDB(dirName, town+'Mobile.gdb')
   
    # Copy shapefile and TIGER into mobile
    arcpy.management.CopyFeatures(town+'.gdb/'+town+'_32145', town+'Mobile.geodatabase/'+town+'_32145')

    arcpy.management.CopyFeatures(town+'.gdb/TIGER_32145', town+'Mobile.geodatabase/TIGER_32145')

    #create dataset
    sr = arcpy.SpatialReference(32145)
    arcpy.management.CreateFeatureDataset(town+'Mobile.geodatabase', town, sr)

    #Move main.town_32145 into dataset
    arcpy.conversion.FeatureClassToGeodatabase(town+'Mobile.geodatabase/main.'+town+'_32145', town+'Mobile.geodatabase/main.'+town,)

    #create overlap/gap topology
    arcpy.management.CreateTopology(town+'Mobile.geodatabase/'+town, town+'_Zoning_Topology', '1')

    #add town_32145 to overlap/gap topology
    arcpy.management.AddFeatureClassToTopology(town+'Mobile.geodatabase/main.'+town+'/main.'+town+'_Zoning_Topology', town+'Mobile.geodatabase/main.'+town+'/main.main_'+town+'_32145', '1', '1')

    #add rules to overlap/gap
    arcpy.management.AddRuleToTopology(town+'Mobile.geodatabase/main.'+town+'/main.'+town+'_Zoning_Topology', 'Must Not Have Gaps (Area)', town+'Mobile.geodatabase/main.'+town+'/main.main_'+town+'_32145')
    arcpy.management.AddRuleToTopology(town+'Mobile.geodatabase/main.'+town+'/main.'+town+'_Zoning_Topology', 'Must Not Overlap (Area)', town+'Mobile.geodatabase/main.'+town+'/main.main_'+town+'_32145')
    
main()
