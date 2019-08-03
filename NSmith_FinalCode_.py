#Nina Smith
#08/04/2019
#GEOG 682 Final

import processing 

#load the file path into variable names
crimeInc = "C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Crime_Incidents_in_2017.shp"
spotShot = "C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Shot_Spotter_Gun_Shots.shp"
wards = "C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Ward_from_2012.shp"

#add each layer to the map
iface.addVectorLayer(wards,"DC Wards","ogr")
iface.addVectorLayer(crimeInc, "DC Crime Incidents","ogr")
iface.addVectorLayer(spotShot, "DC SpotShot Incidents","ogr")

#create SQL expression
expression = '"METHOD"  =  \'GUN\''

#select active layer (gun incidents) and select using defined expression
layer = iface.activeLayer()
layer.selectByExpression(expression, QgsVectorLayer.SetSelection)

#make new selection into a vector layer
QgsVectorFileWriter.writeAsVectorFormat(layer, 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\GunIncidents.shp','utf-8',layer.crs(),'ESRI Shapefile',1)

#join gun incidents layer with the ward layer
processing.runalg("qgis:joinattributesbylocation",
    {'TARGET': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Ward_from_2012.shp',
    'JOIN': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\GunIncidents.shp',
    'PREDICATE':u'contains',
    'SUMMARY':1,
    'KEEP':0,
    'OUTPUT': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Wards_Incidents_Join.shp'})

#select this new layer as the active layer    
gun_layer = iface.activeLayer()

#loop through the values in the layer (wards) and calculate the events per 10000 then print the ward name and value
features1 = gun_layer.getFeatures()
for feat in features1:
    count = feat["count"]
    pop = feat["POP_2010"]
    value = ((count/pop)*10000)
    name = feat["NAME"]
    print(dict(zip(name,value)))
    
#join shot spotter layer with the ward layer
processing.runalg("qgis:joinattributesbylocation",
    {'TARGET': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Ward_from_2012.shp',
    'JOIN': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Shot_Spotter_Gun_Shots.shp',
    'PREDICATE':u'contains',
    'SUMMARY':1,
    'KEEP':0,
    'OUTPUT': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\SpotShot_Incidents_Join.shp'})

#select this layer as the active layer
ss_layer = iface.activeLayer()
#loop through each value (ward) and calculate events per 10000 then print ward name and value
features2 = ss_layer.getFeatures()
for feat in features2:
    count = feat["count"]
    pop = feat["POP_2010"]
    value = ((count/pop)*10000)
    name = feat["NAME"]
    print(dict(zip(name, value)))
