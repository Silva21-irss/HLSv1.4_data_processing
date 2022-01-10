import os
import arcpy
from arcpy import env
folderSpace = r"d:\HLS\Acadia\Mosaics16bitsigned" # Composites input location
env.workspace = folderSpace
folderMosaic = r"d:\HLS\Acadia\Mosaics16bitsigned" # Mosaic output location
folderSave = 'D:\\HLS\\Acadia\\Mosaics16bitsigned\\' # Input location for mosaicked TIFFs
shapefileFolder = "D:\\Shapefiles\\Acadia_Boundary.shp" # Change based on boundary shapefile location
myrastersL = arcpy.ListRasters("extracted*L30*")
myrastersS = arcpy.ListRasters("extracted*S30*")
projection = "NAD 1983 UTM Zone 19N" # Adjust for : 17N Romeo Malette/Haliburton, 18N Petawawa/Estrie, 19N New Brundwick/Eastern QC/Nova Scotia, 20N Newfoundland, 10N BC

print('Removing small files from list')
for a in myrastersL:
    if os.stat(folderSave + a).st_size < 6870690:
        myrastersL.remove(a) # Remove tiles with little to no data from list

print('Joining same day Landsat tiles and sentinel tiles within 3 days')
for a in myrastersL:
    fileList = []
    Adate = a[35:42] # Get date from file name
    fileList.append(a)
    myrastersL.remove(a)
    for b in myrastersL: # Merge other landsat tiles taken on the same day
        if b[35:42] == Adate:
            fileList.append(b)
            myrastersL.remove(b)

    date = int(Adate)
    daterange = [*range(date - 3, date + 4,1)]
    for i in myrastersS: # Merge all sentinel tiles within 3 days from Landast day of acquisition
        day = int(i[35:42])
        if day in daterange:
            fileList.append(i)
    if len(fileList) > 0:
        #arcpy.MosaicToNewRaster_management(fileList, folderMosaic, "Mo" + a[35:42] + '.tif', arcpy.SpatialReference(projection), "32_BIT_FLOAT", "30", "16", "MEAN", "MATCH")
        arcpy.management.Mosaic(fileList,folderSave +a,"MEAN","MATCH","-3200","-3200","","","")
        print(fileList)


# RASTER CLIP
print('Performing Raster Clip')
# Clip out area not included in the site boundary based on the boundary shapefile

arcpy.env.workspace = folderMosaic
myrasters = arcpy.ListRasters("Mo*")

for i in myrasters:
    print(i)
    arcpy.Clip_management(i,"#",folderSave + "Clip"+i,shapefileFolder,'#','ClippingGeometry','MAINTAIN_EXTENT')

print('Landsat tiles that could not be mosaicked : ')
for i in myrastersL:
    print(i)
    arcpy.Clip_management(i,"#",folderSave + "ClipNO"+i[35:42]+".tif",shapefileFolder,'#','ClippingGeometry','MAINTAIN_EXTENT')






