#import requests
import math
from math import sin, cos, atan2, acos

home = '40.280146, -7.512566'
work = '40.280441, -7.507916'

lat1 = 41.28068701521618
lon1 = -8.29118112538366
lat2 = 41.28074597277624
lon2 = -8.291092612493838

lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

dlon = lon2 - lon1
dlat = lat2 - lat1

# Distance Matrix API
api_key = 'AIzaSyAqB4GGXdwCc-60kGj1Cadgx1XyJ-EV2pw'

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metrics"

r = requests.get(url + '&origins=' + home + '&destinations=' + work + '&mode=walking' + '&key=' + api_key )

dist = r.json()['rows'][0]['elements'][0]['distance']['value']
print('Google Maps:',dist)

# Site do Cálculo das Distâncias: https://www.movable-type.co.uk/scripts/latlong.html
# Formula de Haversine
a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
c = 2 * atan2(math.sqrt(a), math.sqrt(1-a))
r = 6371*1000
distance = c*r
print('Formula de Haversine:', distance)

# Spherical Law of Cosines
d = acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(dlon))*r
print('Spherical Law of Cosines', d)

# Equirectangular Approximation
x = dlon*cos((lat1+lat2)/2)
distancia = math.sqrt(x**2+dlat**2)*r
print('Equirectangular Approximation:', distancia)
