# GEOG682-Final
# DC Crime Mapping Analysis
# Nina Smith
# 08/04/19

***Introduction***
This is a project analyzing the effectiveness of Washington, DC's gunshot detection network.  This is done by examining the 
reported gun crime incidents in DC per ward with the number of gun shots spotted per ward. 

***Analysis***
The data for this report was gathered from opendata.dc.gov.  The first dataset: Crime Incidents in 2017, has locations a descriptions of various
crimes that occurred throughout the district in 2017.  The second dataset: Shot Spotter Gun Shots, shows the locations of gunfire in DC
as detected by ShotSpotter which uses sensors to detect the sound of gunfire and report it to the police. Finally, the last dataset: Ward from 
2012, is a polygon dataset with the boundaries of the wards of the city. Links are provided to the datasets and further descriptions.
  Crime Incidents in 2017: https://opendata.dc.gov/datasets/crime-incidents-in-2017 
  Shot Spotter Gun Shots: https://opendata.dc.gov/datasets/shot-spotter-gun-shots?geometry=-139.043%2C-52.268%2C139.043%2C52.268
  Ward from 2012: https://opendata.dc.gov/datasets/ward-from-2012
The two maps for this analysis were created by using data management tools within QGIS.  First, the gun incidents from 'Crime Incidents in 2017'
were selected and made into a new vector layer.  Next, this new layer was joined by location with the 'Ward from 2012' polygon layer with 
the number of points from 'Crime Incidents' that fall within each ward being added to the ward dataset. 
For the Shot Spotter layer, the points from the year 2017 were selected and made into a new layer.  This point layer was then joined by
location with the polygon layer of "Ward from 2012."  
Once these spatial joins were completed, the same expression was used on each.  The count value (number of points that fell in each ward)
was divided by the 2010 population for each ward then multiplied by 10,000 to get the number of incidents per 10,000 people per ward. 

![Fig. 1 - Crime Incidents per 10000 People](https://github.com/nfs26/GEOG682-Final/blob/master/GunIncidentsMap.png)
# Fig. 1 - Crime Incidents per 10,000 People
![Fig. 2 - ShotSpotter Incidents per 10000 People](https://github.com/nfs26/GEOG682-Final/blob/master/ShotSpotterMap2017.png)
# Fig. 2 - ShotSpotter Incidents per 10,000 People

 - Number of Gun Crimes Committed per 10,000 People in 2017 in Each Ward - 
 Ward 1: 15
 Ward 2: 7
 Ward 3: 3
 Ward 4: 17
 Ward 5: 36
 Ward 6: 21
 Ward 7: 58
 Ward 8: 58
 
  - Number of Shooting Incidents Detected by ShotSpotter per 10,000 People in 2017 in Each Ward - 
  Ward 1: 17
  Ward 2: 0
  Ward 3: 0 
  Ward 4: 21
  Ward 5: 57
  Ward 6: 37
  Ward 7: 232
  Ward 8: 289
  
***Automation***
My Python code works by conducting the 'Select by Attributes' and 'Spatial Join' necessary for this analysis.  After those have been performed, it uses the values of each joined layer to calculate the values for each district by iterating through a for loop. 
The select by attribute function is used by creating an SQL expression and using it to select by that expression, as can be seen in this except of code creating the selection expression for the 'Crime Incidents in 2017' layer.
~~~
#create SQL expression
expression = '"METHOD"  =  \'GUN\''

#select active layer (gun incidents) and select using defined expression
layer = iface.activeLayer()
layer.selectByExpression(expression, QgsVectorLayer.SetSelection)
~~~
This selection is then made into a new vector layer:
~~~
#make new selection into a vector layer
QgsVectorFileWriter.writeAsVectorFormat(layer, 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\GunIncidents.shp','utf-8',layer.crs(),'ESRI Shapefile',1)
~~~
Then the newly created vector layers were joined with the polygon ward layer, getting the sum total of points that fall within each ward. 
~~~
#join gun incidents layer with the ward layer
processing.runalg("qgis:joinattributesbylocation",
    {'TARGET': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Ward_from_2012.shp',
    'JOIN': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\GunIncidents.shp',
    'PREDICATE':u'contains',
    'SUMMARY':1,
    'KEEP':0,
    'OUTPUT': 'C:\Users\ninaf\OneDrive\Documents\UMD GEOINT\GEOG682\Final\Wards_Incidents_Join.shp'})
~~~
The for loop works by iterating through each feature in the selected layer, so for each feature, I got the value of the count (number of incidents per ward), population in 2010, and name.  Then, using the count and population values, I calculated the value per 10,000 people.  Then I combined the name value and the calculated value into a dictionary and printed it as can be seen in the for loop for the newly-created joined layer. 
~~~
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
~~~
  
  ***Results***
After reviewing my results, I would suggest that Wards 7 and 8 be covered by an expanded gunshot detection network.  It appears that there are many more gunshots fired in those wards than crimes involving guns are reported.  This means either that the spot shotters are faulty in these areas, or crimes are not being reported in those wards.  As the spot shotter and reported crime incident numbers seem fairly closely matched in city's other districts, it appears that there is more to be learned about criminal activity in Wards 7 and 8, and an expanded gunshot detection network could help with that by providing more data, and potentially helping police arrive at the scene of the crime more quickly to also obtain more information. 

Two limitatations of the data are the limiatations of the ShotSpotters themselves: their inability to locate the precise source of the sound and their inability to locate the precise location of the sounds.  Some of the incidents included in the dataset and analysis could be duplicates heard by multiple ShotSpotters in high density areas, or one incident with multiple gunshots.  Additionally, some of the incidents included in the dataset could have occurred outside the boundaries of the city or even have occurred in one ward yet recorded as occurring in another.  This could lead to more incidents being coded for the wards that contain more ShotSpotters, or to some wards not having as many incidents recorded as truly happened because they have fewer ShotSpotters. 
