file = open( r"D:/OneDrive - Universidade da Beira Interior/PrunusBOT/PathPlanningOptimizationAlgorithm/WaypointsFiles/test.txt", "w")

def WriteFile (WaypointsMatrix, TotalWaypoints):
    file.write("QGC WPL 110\n")
    for i in range(TotalWaypoints+1):
        if i == 0:
            file.write('%s       1       0       0       0       0       0       0       0       0       0       1\n'%(i))
        else:
            file.write('%s       0       3       16       0.00000000       0.00000000       0.00000000       0.00000000       %s       %s       100       1\n'%(i,WaypointsMatrix[i-1,0],WaypointsMatrix[i-1,1]))
    file.close()
