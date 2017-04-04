# This script converts called ACIS json into GeoJSON for mapping

import pandas as pd
import requests
import numpy as np

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

df = pd.DataFrame({
    'lat': lat,
    'lon': lon,
    'month': month,
    'dataPoints': data})

df.replace(-999, np.nan, inplace=True)

df = df.dropna()

lat = df.lat.tolist()
lon = df.lon.tolist()
data = df.dataPoints.tolist()

geoJSON = '{ "type": "FeatureCollection", "features": ['

# Create geoJSON string of points

i = 0
for dataPoint in df.dataPoints.tolist():
    print(df.lon.tolist()[i])
    geoJSON = geoJSON + '{ "type": "Feature", "geometry": {"type": "Point", "coordinates": [{}, {}]}, "properties": {"prop0": "{}"}}, '\
        .format(lon[i], lat[i], data[i])
    i = i + 1

geoJSON = geoJSON[:-2] + ']}'

print(geoJSON)




# { "type": "Polygon",
#     "coordinates": [
#         [[30, 10], [40, 40], [20, 40], [10, 20], [30, 10]]
#     ]
# }

# Create square for grid

# for dataPoint in df.data:
#     if dataPoint.isnull():
#         continue
#     else:
#         geoJSON = geoJSON + '{ "type": "Polygon", "coordinates": [[[30, 10], [40, 40], [20, 40], [10, 20], [30, 10]]]}'
