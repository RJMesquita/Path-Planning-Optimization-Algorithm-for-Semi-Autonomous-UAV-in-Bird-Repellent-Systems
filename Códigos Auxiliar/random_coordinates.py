import matplotlib.pyplot as plt
import numpy as np
import math

lat = 41.2910444
lon = -8.239538

max_radius = 12

def random_point_in_disk(max_radius):
    r = max_radius * np.sqrt(np.random.random(1))
    theta = 2 * np.pi * np.random.random(1)
    return [r * np.cos(theta), r * np.sin(theta)]

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * math.atan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371 * 1000
    distance = c * r
    return distance

EarthRadius = 6371 # km
OneDegree = EarthRadius * 2 * np.pi / 360 * 1000 # 1° latitude in meters

random_lat = np.zeros(9)
random_lon = np.zeros(9)
for i in range(9):
    dx, dy = random_point_in_disk(max_radius)
    random_lat[i] = lat + dy / OneDegree
    random_lon[i] = lon + dx / ( OneDegree * np.cos(lat * np.pi / 180) )
    print(random_lat[i], random_lon[i])
    print(haversine(lat,lon,random_lat[i],random_lon[i]))

'''
n = 100
max_radius_grau = max_radius/OneDegree
t = np.linspace(0,2*np.pi,n+1)
x = max_radius_grau*np.cos(t)+lat
y = max_radius_grau*np.sin(t)+lon
plt.axis('equal')
plt.grid()
plt.plot(x,y,'g',random_lat, random_lon,'b*',lat,lon,'r*')
plt.plot()
plt.show()
'''