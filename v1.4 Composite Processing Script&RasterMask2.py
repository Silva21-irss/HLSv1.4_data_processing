import arcpy
from arcpy import env
import os
from arcpy.sa import *
folderSpace = r"d:\HLS\Quebec"
env.workspace = folderSpace
myrasters = arcpy.ListRasters("HLS.*")

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension('Spatial')

# Access only important bands
Lbands = ['01','02','03','04','05','06','07','08','11']
Sbands = ['01','02','03','04','09','12','13','11','14']
landsat = []
sentinel = []
for x in myrasters:
    if x[4] == 'S' and x[28:30] in Sbands:
        sentinel.append(x)
for x in myrasters:
    if x[4] == 'L' and x[28:30] in Lbands:
        landsat.append(x)
                    
# Determine missing data
print('Investigating Landsat tiles')
a = 0
tog = []
while a < len(landsat):
    tile = landsat[a]
    tog.append(tile)
    sen = tile[8:22]
    for s in landsat:
        if s[8:22] == sen and s != tile:
            tog.append(s)
    if len(tog) < 9:
        for i in tog:
            Lbands.remove(i[28:30])
        print(i[8:22])
        print(Lbands)
    Lbands = ['01','02','03','04','05','06','07','08','11']
    tog = []
    a = a+9

print('Investigating Sentinel tiles')
a = 0
tog = []
years = []
while a < len(sentinel):
    tile = sentinel[a]
    tog.append(tile)
    sen = tile[8:22]
    for s in sentinel:
        if s[8:22] == sen and s != tile:
            tog.append(s)
    if len(tog) < 9:
        for i in tog:
            Sbands.remove(i[28:30])
        print(i[8:22])
        years.append(i[17:22])
        print(Sbands)
    Sbands = ['01','02','03','04','09','12','13','11','14']
    tog = []
    a = a+9

# Produce Composites
print('Producing Composites for landsat HLS tiles')
composite = []
a = 0 # CHANGE BACK TO ZERO
while a < len(landsat):
    tile = landsat[a]
    sen = tile[8:22]
    for x in landsat:
        if x[8:22] == sen:
            composite.append(x)

    # Create indeces as bands in the composite
    ndvi_top = Minus(composite[4],composite[3])
    ndvi_bottom = Plus(composite[4],composite[3])
    ndvi = Divide(Float(ndvi_top),Float(ndvi_bottom))

    nbr_top = Minus(composite[6],composite[4])
    nbr_bottom = Plus(composite[6],composite[4])
    nbr = Divide(Float(nbr_top),Float(nbr_bottom))

    ndmi_top = Minus(composite[5],composite[4])
    ndmi_bottom = Plus(composite[5],composite[4])
    ndmi = Divide(Float(ndmi_top),Float(ndmi_bottom))

    evi_1st = Times(ndvi_top,2.5)
    evi_2nd1 = Times(composite[3],6)
    evi_2nd2 = Times(composite[1],7.5)
    evi_2nd3 = Plus(composite[4],evi_2nd1)
    evi_2nd4 = Plus(evi_2nd2,1)
    evi_bottom = Minus(evi_2nd3,evi_2nd4)
    evi = Divide(Float(evi_1st),Float(evi_bottom))

    tct_b1 = Times(Float(composite[1]),0.3029)
    tct_b2 = Times(Float(composite[2]),0.2786)
    tct_b3 = Times(Float(composite[3]),0.4733)
    tct_b4 = Times(Float(composite[4]),0.5599)
    tct_b5 = Times(Float(composite[5]),0.508)
    tct_b6 = Times(Float(composite[6]),0.1872)
    tct_b11 = Plus(Float(tct_b1),Float(tct_b2))
    tct_b12 = Plus(Float(tct_b3),Float(tct_b4))
    tct_b13 = Plus(Float(tct_b5),Float(tct_b6))
    tct_b14 = Plus(Float(tct_b12),Float(tct_b13))
    tct_brightness = Plus(Float(tct_b11),Float(tct_b14))

    tct_g1 = Times(Float(composite[1]),-0.2941)
    tct_g2 = Times(Float(composite[2]),-0.243)
    tct_g3 = Times(Float(composite[3]),-0.5424)
    tct_g4 = Times(Float(composite[4]),0.7276)
    tct_g5 = Times(Float(composite[5]),0.0713)
    tct_g6 = Times(Float(composite[6]),-0.1608)
    tct_g11 = Plus(Float(tct_g1),Float(tct_g2))
    tct_g12 = Plus(Float(tct_g3),Float(tct_g4))
    tct_g13 = Plus(Float(tct_g5),Float(tct_g6))
    tct_g14 = Plus(Float(tct_g12),Float(tct_g13))
    tct_greenness = Plus(Float(tct_g11),Float(tct_g14))

    tct_w1 = Times(Float(composite[1]),0.1511)
    tct_w2 = Times(Float(composite[2]),0.1973)
    tct_w3 = Times(Float(composite[3]),0.3283)
    tct_w4 = Times(Float(composite[4]),0.3407)
    tct_w5 = Times(Float(composite[5]),-0.7117)
    tct_w6 = Times(Float(composite[6]),-0.4559)
    tct_w11 = Plus(Float(tct_w1),Float(tct_w2))
    tct_w12 = Plus(Float(tct_w3),Float(tct_w4))
    tct_w13 = Plus(Float(tct_w5),Float(tct_w6))
    tct_w14 = Plus(Float(tct_w12),Float(tct_w13))
    tct_wetness = Plus(Float(tct_w11),Float(tct_w14))

    composite.append(ndvi)
    composite.append(nbr)
    composite.append(ndmi)
    composite.append(evi)
    composite.append(tct_brightness)
    composite.append(tct_greenness)
    composite.append(tct_wetness)
    
    arcpy.CompositeBands_management(composite,
                            "HLS_composite_L30_" + sen + ".tif")
    print(composite)
    b = 1
    composite = []
    a = a+9

sentinel = sentinel[4869:len(sentinel)] # REMOVE THIS LINE AFTER MALCOLM KNAPP!!!

print('Processing Sentinel composites')
composite = []
a = 0
while a < len(sentinel):
    tile = sentinel[a]
    sen = tile[8:22]
    for x in sentinel:
        if x[8:22] == sen:
            composite.append(x)
            
    # Create indeces as bands in the composite   
    composite = [composite[0],composite[1],composite[2],composite[3],composite[4],composite[6],composite[7],composite[5],composite[8]]

    ndvi_top = Minus(composite[4],composite[3])
    ndvi_bottom = Plus(composite[4],composite[3])
    ndvi = Divide(Float(ndvi_top),Float(ndvi_bottom))

    nbr_top = Minus(composite[6],composite[4])
    nbr_bottom = Plus(composite[6],composite[4])
    nbr = Divide(Float(nbr_top),Float(nbr_bottom))

    ndmi_top = Minus(composite[5],composite[4])
    ndmi_bottom = Plus(composite[5],composite[4])
    ndmi = Divide(Float(ndmi_top),Float(ndmi_bottom))

    evi_1st = Times(ndvi_top,2.5)
    evi_2nd1 = Times(composite[3],6)
    evi_2nd2 = Times(composite[1],7.5)
    evi_2nd3 = Plus(composite[4],evi_2nd1)
    evi_2nd4 = Plus(evi_2nd2,1)
    evi_bottom = Minus(evi_2nd3,evi_2nd4)
    evi = Divide(Float(evi_1st),Float(evi_bottom))

    tct_b1 = Times(Float(composite[1]),0.3029)
    tct_b2 = Times(Float(composite[2]),0.2786)
    tct_b3 = Times(Float(composite[3]),0.4733)
    tct_b4 = Times(Float(composite[4]),0.5599)
    tct_b5 = Times(Float(composite[5]),0.508)
    tct_b6 = Times(Float(composite[6]),0.1872)
    tct_b11 = Plus(Float(tct_b1),Float(tct_b2))
    tct_b12 = Plus(Float(tct_b3),Float(tct_b4))
    tct_b13 = Plus(Float(tct_b5),Float(tct_b6))
    tct_b14 = Plus(Float(tct_b12),Float(tct_b13))
    tct_brightness = Plus(Float(tct_b11),Float(tct_b14))

    tct_g1 = Times(Float(composite[1]),-0.2941)
    tct_g2 = Times(Float(composite[2]),-0.243)
    tct_g3 = Times(Float(composite[3]),-0.5424)
    tct_g4 = Times(Float(composite[4]),0.7276)
    tct_g5 = Times(Float(composite[5]),0.0713)
    tct_g6 = Times(Float(composite[6]),-0.1608)
    tct_g11 = Plus(Float(tct_g1),Float(tct_g2))
    tct_g12 = Plus(Float(tct_g3),Float(tct_g4))
    tct_g13 = Plus(Float(tct_g5),Float(tct_g6))
    tct_g14 = Plus(Float(tct_g12),Float(tct_g13))
    tct_greenness = Plus(Float(tct_g11),Float(tct_g14))

    tct_w1 = Times(Float(composite[1]),0.1511)
    tct_w2 = Times(Float(composite[2]),0.1973)
    tct_w3 = Times(Float(composite[3]),0.3283)
    tct_w4 = Times(Float(composite[4]),0.3407)
    tct_w5 = Times(Float(composite[5]),-0.7117)
    tct_w6 = Times(Float(composite[6]),-0.4559)
    tct_w11 = Plus(Float(tct_w1),Float(tct_w2))
    tct_w12 = Plus(Float(tct_w3),Float(tct_w4))
    tct_w13 = Plus(Float(tct_w5),Float(tct_w6))
    tct_w14 = Plus(Float(tct_w12),Float(tct_w13))
    tct_wetness = Plus(Float(tct_w11),Float(tct_w14))

    composite.append(ndvi)
    composite.append(nbr)
    composite.append(ndmi)
    composite.append(evi)
    composite.append(tct_brightness)
    composite.append(tct_greenness)
    composite.append(tct_wetness)
    
    arcpy.CompositeBands_management(composite,
                            "HLS_composite_S30_" + sen + ".tif")
    print(composite)
    composite = []
    a = a+9

print('Processing Masks')

# Process Mask
env.workspace = folderSpace
myrastersL = arcpy.ListRasters("*.L30*11.tif")
myrastersS = arcpy.ListRasters("*.S30*14.tif")
myrastersX = myrastersL + myrastersS

print("Now processing mask")
#All values indicating water/no water and low-no aerosol interference
for ras in myrastersX:
    #if ras[4] == 'L' and ras[28:30] == '11':
        print(ras)
        name = os.path.join(folderSpace, 'm_' + ras)
        ras = arcpy.Raster(ras)
        out_raster = Con((ras==0)|(ras==32)|(ras==64)|(ras==96)|(ras==128)|(ras==160),ras)
        out_raster.save(name) # Create binary raster mask


# Mask out pixels experiencing interference
comprastersL = arcpy.ListRasters("HLS_composite_L*")
for i in comprastersL:
    print(i)
    name = os.path.join(folderSpace,'extracted_' + i)
    outExtract = ExtractByMask(i,"m_HLS.L30." + i[18:32]+".v1.4_11.tif")
    outExtract.save(name)

comprastersS = arcpy.ListRasters("HLS_composite_S*")
for i in comprastersS:
    print(i)
    name = os.path.join(folderSpace,'extracted_' + i)
    outExtract = ExtractByMask(i,"m_HLS.S30." + i[18:32]+".v1.4_14.tif")
    outExtract.save(name)

