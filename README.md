# fuzzy_traffic_controller
A fuzzy logic based traffic light controller using scikit-fuzzy  sumo.
To reduce the waiting time of emergency vehicles at intersections, this fuzzy logic algorithm was designed to prioritize emergency vehicles simulated on sumo.

## Requirememts
- [python3](https://www.python.org/downloads/)
- [sumo](https://www.eclipse.org/sumo/)
- [sumo-gui](https://sumo.dlr.de/docs/sumo-gui.html)

## Running the program
run `python3 fuzzy_controlled_simulation.py` to run the fuzzy logic controlled traffic simulation 

run `python3 uncontrolled_simulation.py` to run the uncontrolled traffic simulation (The uncontrolled simulation is used as test to compare the efficiency of the fuzzy controlled simulation)

## Overview
A fuzzy logic-based traffic light control system was programmed with python using and [SciKit-fuzzy](https://scikit-fuzzy.github.io/scikit-fuzzy/overview.html), SciPys’ fuzzy logic toolbox. 
Microscopic Traffic Simulation was done using sumo and used to simulate a four junction, vehicles are added in proportions, and [Traffic Controller interface (Traci)](https://sumo.dlr.de/docs/TraCI.html) is used to connect the sumo simulation to the controlling python program.

## Starting SUMO
We do that by checking if the environment variable $SUMO_HOME is defined on the system. $SUMO_HOME points to the installation folder of SUMO. If sumo is installed, we then go ahead to start the sumo GUI and then load the already created road network. Then we continued by importing traci and starting the simulation.
From traci, we stored the names of lanes that can be affected by each traffic light turn and we got the ID of the traffic light in the intersection.


## PRE SIMULATION (Building the road netwrks)
The road network was built and connected using the sumo GUI. The junctions and the connection between lanes were defined and the generated XML was saved to file.
A route as used in this project is a well-defined journey that has a start position/state and an end position/state. Eight Routes were defined.

## THE SIMULATION
Using the sumo’s default one-second per simulation step,  The simulation takes approximately 16,000 steps run. For each step, we get the amount of vehicles moving, and the amount of vehicles currently stopped by the traffic light. We get the waiting time of vehicles stopped by the light. From among them, we get the vehicle with the maximum waiting time. We also check for the amount of emergency vehicles on the road. 

There are two main version of the main program. The first uses the default ninety-seconds fixed-time-controlled traffic light, each route is passed for ninety (90) steps no matter what is happening on the road. 

Data from this version of the program is used as control to compare with the others.  The second version of this program uses a fuzzy logic controller. After every seven steps, it send the information on amount of vehicles on road, the waiting time of vehicles in traffic, the presence, amount and location of emergency vehicles to the fuzzy logic controller to determine whether or not to switch the traffic light.

## THE FUZZY LOGIC CONTROLLER
The fuzzy logic controller was implemented using SciKit Fuzzy (skfuzzy).
The fuzzy logic controller accepts five inputs: number of vehicles on the red lanes, number of vehicle on green lanes, the maximum waiting time of vehicles on the red lane, number of emergency vehicles on the red lane and number of emergency vehicles on the green lane.

We defined the number of vehicles using an array of integers from 0 – 12. then we used three triangular membership functions and an s-function to define the memberships. Values from 0 – 4 were defined as "too-small", values from 2 to 8 were defined as "small", values from 5 to 10 were defined as "much" and values from 8 upwards were defined as "too-much".

<img width="499" alt="image" src="https://user-images.githubusercontent.com/39713155/145992825-45fec009-db91-44b0-8ce2-f1ba2d19becc.png">
*Number of vehicles membership graph*
Waiting time was defined using an array of integers from 0 to 50. From our network, we found that the waiting maximum waiting time of vehicles before the traffic light switch falls within the range of 45 and 55. We also used the triangular membership function and S-function to define the memberships. we defined waiting time from 0 to 12 as "negligible", from 8 to 25 as "okay", from 18 to 38 as "much" and from 28 and above as too "much"
<img width="508" alt="image" src="https://user-images.githubusercontent.com/39713155/145992878-20eaef8b-4f15-4397-8634-a3df1502fbfb.png">
*Maximum vehicle waiting time membership graph*
Amount of emergency vehicles on the lane was defined using an array of integers from 0 to 2.  we used the Z-function and S-function to define membership. If there is zero emergency vehicle in the lane, we defined that as "absent". If there is 1, "present" and if there is 2 or more, we defined that as "much".
<img width="398" alt="image" src="https://user-images.githubusercontent.com/39713155/145992918-7030c6bc-5bd6-45fd-bd08-5fa67ec5acd0.png">
*Number of emergency vehicles membership graph*
The output of the fuzzy logic is a value between 0 and 1. Which was implemented by passing an array containing 0 and 1 as the consequent. If the output is 0, then the traffic light is “okay” if it is 1, then it needs switching.
<img width="316" alt="image" src="https://user-images.githubusercontent.com/39713155/145992952-c43a5fd1-135d-47ec-a935-06774c547848.png">
*Traffic light output membership graph*
These set of antecedents and consequents were grouped into fuzzy rules that were used to create the control system. The control system was then simulated and used to compute outputs based on the five inputs. The output of the fuzzy logic controller is a decimal from 0 to 1. The output zero indicates that the traffic controller is okay and the value one means that the controller needs switching. When running the simulation, output usually falls between 0.3 and 0.7 so we set a bar at 0.5. If the output is below 0.5 the traffic light won’t be changed if not, it would be switched. 


## CONCLUSION

A performance evaluation was done on the created fuzzy logic controller and from the result obtained, it can be deduced that a smarter traffic light control system can improve throughput at intersections and reduce the overall time spent in traffic. Also, when prioritizing vehicles, there should be an additional waiting time on other (unprioritized) vehicles. In the case of this project, there is no such overhead. Other vehicles had their average waiting time reduced by 25%. emergency vehicles that were prioritized had their average waiting time reduced by 77%. The average number of moving vehicles in the intersection increased by 6% and the number of vehicles stopped by traffic reduced by 7%.
