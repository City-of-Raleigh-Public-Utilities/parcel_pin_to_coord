#Get PIN
#Set PIN as String
#Create X Y variables
#Loop through setting even and odd numbers
#Add zero to ends
#Create feature class
#Add fields to shp file
#put x y values in fc
#Add feature class to mxd
#pan to layer


#PIN = '1840484945'
#X = 'X' + '=' + '2' + PIN[0] + PIN[2] + PIN[4] + PIN[6] + PIN[8] + '0'
#Y = 'Y' + '=' + PIN[1] + PIN[3] + PIN[5] + PIN[7] + PIN[9] + '0'
#print X
#print Y



import arcpy
from arcpy import env
import arcpy.mapping
arcpy.env.workspace="c:\\temp"
arcpy.env.overwriteOutput=True

ParcelPin = arcpy.GetParameterAsText(0)
x = '2'
y = ''

for i, v in enumerate(ParcelPin):
    if i % 2 == 0:
    	x= (x+v)
    else:
   		y=y+v
X=int(x+'0')
Y=int(y+'0')
#Make Lat, Long variables from X and Y turn to strings to concatenate with X=, Y = coordinate for later labeling
Longitude=str(X)
Latitude=str(Y)
arcpy.AddMessage(' X = ' + Longitude)
arcpy.AddMessage(' Y = ' + Latitude)
#Create shape file
out_path="c:\\temp"
out_name="ParcelPoint.shp"
geometry_type="POINT"
#Create spatial reference
sr=arcpy.SpatialReference(2264)
arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, spatial_reference=sr)
#Add fields to shp file
inFeatures="ParcelPoint.shp"
fieldName1="Long"
fieldLength=20
fieldName2="Lat"
fieldLength=20
arcpy.AddField_management(inFeatures, fieldName1, "Text", fieldLength)
arcpy.AddField_management(inFeatures, fieldName2, "Text", fieldLength)
#Create cursor and rows
#if your feature class is a point feature class, use "SHAPE@XY"
#Add x y values in lat long fields
#Create point geometry in shp file
rowValue=[X,Y]
with arcpy.da.InsertCursor("ParcelPoint.shp", ["SHAPE@XY", "Long", "Lat"]) as cursor:
	cursor.insertRow([rowValue, X, Y])
#This produces the same result
#rowValue=(X,Y), X,Y
#with arcpy.da.InsertCursor("ParcelPoint.shp", ("SHAPE@XY", "Long", "Lat")) as cursor:
#	cursor.insertRow(rowValue)

#Add shape file to mxd
theShape=r"c:\\temp\\ParcelPoint.shp"
mxd=arcpy.mapping.MapDocument("CURRENT")
#get the data frame
df=arcpy.mapping.ListDataFrames(mxd)[0]
#create new layer
newLayer=arcpy.mapping.Layer(theShape)
#add layer to the map at the top of the TOC in data frame
arcpy.mapping.AddLayer(df, newLayer, "TOP")
#Select shape file ParcelPoint
arcpy.MakeFeatureLayer_management("c:\\temp\\ParcelPoint.shp")
arcpy.SelectLayerByAttribute_management("ParcelPoint", "NEW_SELECTION", ' "FID" < 1 ')
#Pan to selected feature
#Set extent of map
df.panToExtent(newLayer.getSelectedExtent())
df.scale = 1250
#Unselect feature class
arcpy.SelectLayerByAttribute_management("ParcelPoint", "CLEAR_SELECTION", ' "FID" < 1 ')
#Change symbology to existing layer file
arcpy.ApplySymbologyFromLayer_management("ParcelPoint", r"C:\\Users\\Mazanekm\\Documents\\Python\\Deconstruct_PIN\\ParcelPointSymbology.lyr")
#Apply Label
layer=arcpy.mapping.ListLayers(mxd) [0]  #Indexing list for 1st layer
layer.showLabels = True
#Change color and make text bold
layer.labelClasses[0].expression=  ' "%s" & "X = " & [Long] & "  " & "Y = " & [Lat] & "%s" ' % ("<BOL><CLR red='255' green='255' blue='0'>", "</CLR></BOL>")
#Turn bold tag on, turn color tag on, turn color tag off turn bold tag off. Just like placing a stack of plates and retrieving the plates.

#refresh things
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
#delete variables, mxd created
del mxd, df, newLayer, layer
