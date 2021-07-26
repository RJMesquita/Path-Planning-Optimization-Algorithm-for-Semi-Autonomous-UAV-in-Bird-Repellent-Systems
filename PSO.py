import numpy as np
from math import radians, cos, sin, atan2, sqrt
from main import EarthRadius
#from matplotlib import pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = c * EarthRadius
    return distance

def Minimization (Departure,Landing,SensorsCoordinates,NumberOfSensors):
    NumberOfParticles = 5
    part = np.zeros([NumberOfParticles, NumberOfSensors])
    raw_part = np.zeros([NumberOfParticles, NumberOfSensors])

    BestPathBetweenSensors = float('inf')
    OrderOfSensors = np.zeros(NumberOfSensors)
    Pbest = np.array(np.ones((NumberOfParticles)) * np.inf)
    XPbest = np.zeros([NumberOfParticles, NumberOfSensors])
    fobj = np.zeros(NumberOfParticles)

    c1 = 2
    c2 = 2
    #W = 0.7
    W = 0.5 + (np.random.random_sample() / 2)
    v = np.random.random((NumberOfParticles, NumberOfSensors))

    for i in range(NumberOfParticles):
        simple_part = np.random.permutation(NumberOfSensors)
        for j in range(NumberOfSensors):
            part[i, j] = simple_part[j]

    it = 1
    itmax = 50
    #BestPathBetweenSensorsConv = np.zeros(itmax)
    #Time = np.zeros(itmax)
    while it <= itmax:
        for i in range(NumberOfParticles):
            fobj[i] = 0
            for j in range(NumberOfSensors):
                if j == 0:
                    distance = haversine(Departure[0], Departure[1], SensorsCoordinates[(int(part[i, j]), 0)],
                                         SensorsCoordinates[(int(part[i, j]), 1)])
                elif j > 0:
                    distance = haversine(SensorsCoordinates[(int(part[i, j - 1]), 0)],
                                         SensorsCoordinates[(int(part[i, j - 1]), 1)],
                                         SensorsCoordinates[(int(part[i, j]), 0)], SensorsCoordinates[(int(part[i, j]), 1)])
                fobj[i] = fobj[i] + distance
            fobj[i] = fobj[i] + haversine(Landing[0], Landing[1], SensorsCoordinates[(int(part[i, j]), 0)],
                                          SensorsCoordinates[(int(part[i, j]), 1)])
            if BestPathBetweenSensors>= fobj[i]:
                BestPathBetweenSensors = fobj[i]
                OrderOfSensors = part[i]
            if Pbest[i] >= fobj[i]:
                Pbest[i] = fobj[i]
                XPbest[i] = part[i]

        for i in range(NumberOfParticles):
            r1 = np.random.random(1)
            r2 = np.random.random(1)
            for j in range(NumberOfSensors):
                v[i, j] = W * v[i, j] + c1 * r1 * (XPbest[i, j] - part[i, j]) + c2 * r2 * (
                        OrderOfSensors[j] - part[i, j])
                raw_part[i, j] = part[i, j] + v[i, j]
                part[i, j] = round(raw_part[i, j], 0)
                if part[i, j] >= NumberOfSensors:
                    part[i, j] = NumberOfSensors - 1
                if part[i, j] < 0:
                    part[i, j] = 0

        for i in range(NumberOfParticles):
            for j in range(NumberOfSensors):
                for aux_j in range(NumberOfSensors):
                    if j != aux_j:
                        if part[i, j] == part[i, aux_j] and part[i, j] != -1:
                            if raw_part[i, j] < raw_part[i, aux_j]:
                                part[i, aux_j] = -1
                            else:
                                part[i, j] = -1

        for i in range(NumberOfParticles):
            for j in range(NumberOfSensors):
                if part[i, j] == -1:
                    out = True
                    while out == True:
                        value = int(NumberOfSensors * np.random.random(1))
                        if value in part[i]:
                            continue
                        else:
                            part[i, j] = value
                            out = False
        #BestPathBetweenSensorsConv[it-1] = BestPathBetweenSensors
        #Time[it-1] = it
        it = it + 1
    #plt.plot(Time,BestPathBetweenSensorsConv,'b-')
    #plt.show()
    return BestPathBetweenSensors,OrderOfSensors

def Maximization(cord, waypersensor, waypoints,cord_sensors):
    numb_part = 5
    part = np.zeros([numb_part, waypersensor])
    raw_part = np.zeros([numb_part, waypersensor])

    Gbest = float('-inf')
    XGbest = np.zeros(waypersensor)
    Pbest = np.array(np.ones((numb_part)) * -np.inf)
    XPbest = np.zeros([numb_part, waypersensor])
    fobj = 0

    c1 = 2
    c2 = 2
    #W = 0.7
    W = 0.5 + (np.random.random_sample() / 2)
    v = np.random.random((numb_part, waypersensor))

    for i in range(numb_part):
        simple_part = np.random.permutation(waypersensor)
        for j in range(waypersensor):
            part[i, j] = simple_part[j]

    it = 1
    itmax = 200
    #GbestConv = np.zeros(itmax)
    #Time = np.zeros(itmax)
    last = 0
    while it <= itmax:
        for i in range(numb_part):
            for j in range(waypersensor):
                if j == 0:
                    distance = haversine(cord_sensors[(cord, 0)], cord_sensors[(cord, 1)],
                                         waypoints[(int(part[i, j]), 0)], waypoints[(int(part[i, j]), 1)])
                elif j > 0:
                    distance = haversine(waypoints[(int(part[i, j - 1]), 0)], waypoints[(int(part[i, j - 1]), 1)],
                                         waypoints[(int(part[i, j]), 0)], waypoints[(int(part[i, j]), 1)])
                fobj = fobj + distance
                last = haversine(cord_sensors[(cord, 0)], cord_sensors[(cord, 1)],
                                     waypoints[(int(part[i, j]), 0)], waypoints[(int(part[i, j]), 1)])
            fobj = fobj + last
            if Gbest <= fobj:
                Gbest = fobj
                XGbest = part[i]
            if Pbest[i] <= fobj:
                Pbest[i] = fobj
                XPbest[i] = part[i]
            fobj = 0

        for i in range(numb_part):
            r1 = np.random.random(1)
            r2 = np.random.random(1)
            for j in range(waypersensor):
                v[i, j] = W * v[i, j] + c1 * r1 * (XPbest[i, j] - part[i, j]) + c2 * r2 * (
                        XGbest[j] - part[i, j])
                raw_part[i, j] = part[i, j] + v[i, j]
                part[i, j] = round(raw_part[i, j], 0)
                if part[i, j] >= waypersensor:
                    part[i, j] = waypersensor - 1
                if part[i, j] < 0:
                    part[i, j] = 0

        for i in range(numb_part):
            for j in range(waypersensor):
                for aux_j in range(waypersensor):
                    if j != aux_j:
                        if part[i, j] == part[i, aux_j] and part[i, j] != -1:
                            if raw_part[i, j] < raw_part[i, aux_j]:
                                part[i, aux_j] = -1
                            else:
                                part[i, j] = -1

        for i in range(numb_part):
            for j in range(waypersensor):
                if part[i, j] == -1:
                    out = True
                    while out == True:
                        value = int(waypersensor * np.random.random(1))
                        if value in part[i]:
                            continue
                        else:
                            part[i, j] = value
                            out = False
        #GbestConv[it-1] = Gbest
        #Time[it-1] = it
        it = it + 1
    #plt.plot(Time, GbestConv, 'b-')
    #plt.show()
    return Gbest, XGbest
