import numpy as np
import time
import PSO
import interface

# Constants
EarthRadius = 6371000  # m
OneDegree = EarthRadius * 2 * np.pi / 360  # 1° latitude in meters in the equator
FinalDistance = 0


def random_points(cord,NumberOfPoints):
    RandomWaypoints = np.zeros([NumberOfPoints,2])
    for i in range(NumberOfPoints):
        r = max_radius * np.sqrt(np.random.random(1))
        theta = 2 * np.pi * np.random.random(1)
        dx = r * np.cos(theta)
        dy = r * np.sin(theta)
        RandomWaypoints[i,0] = SensorsCoordinates[cord,0] + dy / OneDegree
        RandomWaypoints[i,1] = SensorsCoordinates[cord,1] + dx / (OneDegree * np.cos(SensorsCoordinates[cord,0] * np.pi / 180))
    return RandomWaypoints


def Sortarrays (Matrix,Order):
    OldMatrix = Matrix
    MatrixLen = np.shape(Matrix)
    Matrix = np.zeros([MatrixLen[0],MatrixLen.__len__()])
    for i in range(MatrixLen[0]):
        Matrix[i] = OldMatrix[int(Order[i])]
    return Matrix


def main(FinalDistance, NumberOfWaypoints):
    it = 0
    pointspersensor = np.zeros(NumberOfSensors)
    while FinalDistance < MaxDistance - DistanceError or FinalDistance > MaxDistance + DistanceError:
        FinalDistance = BestPathBetweenSensors
        RealNumberOfWaypoints = 0

        for i in range(NumberOfSensors):
            pointspersensor[i] = int(NumberOfWaypoints * NonZeroPercentage[i])
            RealNumberOfWaypoints = RealNumberOfWaypoints+ int(pointspersensor[i])
        TotalWaypoints = 2+2*NumberOfSensors+RealNumberOfWaypoints
        WaypointsMatrix = np.zeros([TotalWaypoints, 2])
        WaypointsMatrix[0,:] = TakeOff
        WaypointsMatrix[TotalWaypoints-1, :] = Landing

        ex = 1
        for i in range(NumberOfSensors):
            aux = 0
            waypoints = random_points(i, int(pointspersensor[i]))
            [max_path_dist, cord_order] = PSO.Maximization(i, int(pointspersensor[i]), waypoints, SensorsCoordinates)
            waypoints = Sortarrays(waypoints,cord_order)
            FinalDistance = FinalDistance + max_path_dist
            WaypointsMatrix[ex] = SensorsCoordinates[i]
            ex = ex+1
            while aux != int(pointspersensor[i]):
                for j in range(int(pointspersensor[i])):
                    WaypointsMatrix[j+ex] = waypoints[j]
                    aux = aux+1
            ex = ex+int(pointspersensor[i])
            WaypointsMatrix[ex] = SensorsCoordinates[i]
            ex = ex+1

        # Control the number of waypoints according to the difference between the final distance and the maximum
        final_diff = int(FinalDistance - MaxDistance)
        if final_diff > DistanceError:
            RealNumberOfWaypoints = RealNumberOfWaypoints - NumberOfSensors
        elif final_diff < - DistanceError:
            RealNumberOfWaypoints = RealNumberOfWaypoints + NumberOfSensors

        NumberOfWaypoints = RealNumberOfWaypoints
        it = it + 1

    print('Distance: ', FinalDistance)
    print('Total Waypoints: ', TotalWaypoints)
    print('Iterations: ', it)
    print('Time: ', (time.time() - st))
    print('---------------------------------')

    return WaypointsMatrix, TotalWaypoints


if __name__ == '__main__':

    TakeOff, Landing, Sensors, Percentage, MaxDistance, max_radius, DistanceError, path, height = interface.GraficInterface()

    st = time.time()

    # Removal Of Sensors Without Detection
    NonZeroPercentage = []
    for i in range(len(Percentage)):
        if Percentage[i] != 0:
            NonZeroPercentage.append(Percentage[i])
    aux = 0
    SensorsCoordinates = np.zeros([len(NonZeroPercentage), 2])
    for i in range(len(Percentage)):
        if Percentage[i] != 0:
            SensorsCoordinates[aux] = Sensors[i]
            aux = aux + 1
    NumberOfSensors = len(SensorsCoordinates)

    # Path Between Sensors (PSO Minimization)
    [BestPathBetweenSensors, OrderOfSensors] = PSO.Minimization(TakeOff, Landing, SensorsCoordinates, NumberOfSensors)
    SensorsCoordinates = Sortarrays (SensorsCoordinates,OrderOfSensors)
    NonZeroPercentage = Sortarrays(NonZeroPercentage,OrderOfSensors)

    # Calculation Of The Number Of Waypoints To The Sensors
    cont = 1  # One meter per each sensor
    dif_dist = int((MaxDistance - BestPathBetweenSensors) / NumberOfSensors)
    distperway = 0
    NumberOfWaypoints = 1
    while distperway != cont:  # distancia por ponto
        distperway = int(dif_dist / NumberOfWaypoints)
        NumberOfWaypoints = NumberOfWaypoints + 1

    [WaypointsMatrix, TotalWaypoints] = main(FinalDistance, NumberOfWaypoints)

    file = open(path,"w")
    file.write("QGC WPL 110\n")
    for i in range(TotalWaypoints + 1):
        if i == 0:
            file.write('%s       1       0       0       0       0       0       0       0       0       0       1\n' % (i))
        if i == 0:
            file.write('%s       0       3       22       0.00000000       0.00000000       0.00000000       0.00000000       %s       %s       %s       1\n' % (i, WaypointsMatrix[i - 1, 0], WaypointsMatrix[i - 1, 1], height))
        if i == TotalWaypoints:
            file.write('%s       0       3       21       0.00000000       0.00000000       0.00000000       0.00000000       %s       %s       %s       1\n' % (i, WaypointsMatrix[i - 1, 0], WaypointsMatrix[i - 1, 1], height))
        else:
            file.write('%s       0       3       16       0.00000000       0.00000000       0.00000000       0.00000000       %s       %s       %s       1\n' % (i, WaypointsMatrix[i - 1, 0], WaypointsMatrix[i - 1, 1],height))
    file.close()
