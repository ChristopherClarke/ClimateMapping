# This script converts called ACIS json into GeoJSON for mapping

import requests
from geojson import Feature, Point, FeatureCollection, Polygon
import geojson

params = '{"state":"la","grid":"21","meta":"ll","elems":' \
         '[{"name":"mint","interval":"mly","duration":"mly","reduce":"mean"}],' \
         '"date":"201702"}'

url = 'http://data.rcc-acis.org/GridData'

req = requests.post(url, data=params, headers={
    'content-type': 'application/json'})

json = req.json()

lat = json['meta']['lat']
lon = json['meta']['lon']
month = json['data'][0][0]  # May need to be changed if looking at multiple months
data = json['data'][0][1]  # " "

lat = [val for sublist in lat for val in sublist]  # List of lists converted to single list
lon = [val for sublist in lon for val in sublist]  # " "
data = [val for sublist in data for val in sublist]  # " "

# Create geoJSON string of points

featureLISTpoint = []
i = 0
for dataPoint in data:
    if dataPoint != -999:
        point = Point((lon[i], lat[i]))
        feature = Feature(geometry=point, properties={"value": "{}".format(data[i])})
        featureLISTpoint.append(feature)
        i = i + 1
    else:
        i = i + 1

outputJSONpoint = FeatureCollection(featureLISTpoint)

with open('GeoJSONpoint.json', 'w') as f:
    geojson.dump(outputJSONpoint, f)

# Create geoJSON file of Polygons for grid

gridSize = abs(lat[0]-lat[1])
d = gridSize / 2  # ACIS points are center of grid panel, therefore we must create 4 points for the corners
                # of the square with lat/lon + or - 'd' away from lat/lon of center

featureLISTpoly = []
j = 0
for dataPoint in data:
    if dataPoint != -999:
        polygon = Polygon(((lon[j]-d, lat[j]+d), (lon[j]+d, lat[j]+d), (lon[j]+d, lat[j]-d), (lon[j]-d, lat[j]-d)))
        feature = Feature(geometry=polygon, properties={"value": "{}".format(data[j])})
        featureLISTpoly.append(feature)
        j = j + 1
    else:
        j = j + 1

outputJSONpoly = FeatureCollection(featureLISTpoly)

with open('GeoJSONpoly.json', 'w') as f:
    geojson.dump(outputJSONpoly, f)
