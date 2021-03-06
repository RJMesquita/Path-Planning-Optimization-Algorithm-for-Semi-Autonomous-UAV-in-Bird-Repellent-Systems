# A Novel Path Planning Optimization Algorithm for Semi-Autonomous UAV in Bird Repellent Systems Based in Particle Swarm Optimization

## Abstract
Bird damage to fruit crops causes significant monetary losses to farmers annually. The
application of traditional bird repelling methods such as bird cannons and tree netting become
inefficient in the long run, requiring high maintenance and reducing mobility. Due to their versatility,
Unmanned Aerial Vehicles (UAVs) can be beneficial to solve this problem. However, due to their low
battery capacity that equals low flight duration, it is necessary to evolve path planning optimization.
A novel path planning optimization algorithm of UAVs based on Particle Swarm Optimization
(PSO) is presented in this paper. This path planning optimization algorithm aims to manage the
drone’s distance and flight time, applying optimization and randomness techniques to overcome
the disadvantages of the traditional systems. The proposed algorithm’s performance was tested in
three study cases: two of them in simulation to test the variation of each parameter and one in the
field to test the influence on battery management and height influence. All cases were tested in the
three possible situations: same incidence rate, different rates, and different rates with no bird damage
to fruit crops. The field tests were also essential to understand the algorithm’s behavior of the path
planning algorithm in the UAV, showing that there is less efficiency with fewer points of interest, but
this does not correlate with the flight time. In addition, there is no association between the maximum
horizontal speed and the flight time, which means that the function to calculate the total distance for
path planning needs to be adjusted. Thus, the proposed algorithm presents promising results with
an outstanding reduced average error in the total distance for the path planning obtained and low
execution time, being suited for this and other applications.

## Keywords
* Bird damage to fruit crops; 
* Unmanned Aerial Vehicles; 
* Path Planning; 
* Meta-Heuristic; 
* Path Planning Optimization Algorithm;

## Global Architecture
Before developing the proposed optimization algorithm, studying the general problem and the tools needed to solve it was necessary. Birds damage trees and eat fruits of producers around the world, causing quantity and quality to decrease. Traditional repelling systems work in the short term but become ineffective because they maintain low mobility, and birds can easily detect patterns. UAVs have already proven to be essential tools to solve this problem, bridging traditional systems disadvantages. However, optimizing the path according to the bird’s pattern is necessary because drones have limited flight time.
After analyzing the problem, the algorithm was developed in Python programming language, in version 3.8, due to its versatility and pre-existing libraries in all areas of the algorithm, such as Graphical User Interface (GUI), math functions, and file manipulation. The fields were divided into plots assigned by the producer. These segments will be mentioned as points of interest (PoI) and have different damage proportions. In this way, and since the problem needs consistent application of the repelling systems, the optimization algorithm needs to minimize the flight distance between sections and maximize it according to the percentage of damage in each plot. However, birds can detect patterns and learn how to avoid them, so different numbers of random waypoints are required according to the area. As already mentioned, Mission Planner was chosen as pre-planning software, so it is essential to generate a compatible file of waypoints with various parameters. So, the proposed algorithm can be divided into four main steps: parameter setting, minimization between PoIs, maximization of Random Waypoints and creation of pre-planned mission file.
