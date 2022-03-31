import os, sys
import traci
from fuzzy_rules import fuzzy_controller_function
from helper_functions import *

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

sumo_binary = "sumo-gui"
sumo_cmd = [sumo_binary, "-c", "junction.sumocfg", "--start"]

traci.start(sumo_cmd)

west_east_lanes = ["E0_0", "-E1_0"]
north_south_lanes = ["E2_0", "-E3_0"]

trafficLightID = traci.trafficlight.getIDList()[0]
no_stopped = []
no_moving = []

step = 0
total_vehicle_waiting_time = 0

while step < 5000:
    lanes_currently_moving, lanes_stopped_by_light = get_lane_lists(
        west_east_lanes, north_south_lanes, trafficLightID
    )

    vehicles_in_red_lanes = get_vehicles_in_lane(lanes_stopped_by_light)
    vehicles_in_green_lanes = get_vehicles_in_lane(lanes_currently_moving)

    no_vehicles_in_red_lanes = len(vehicles_in_red_lanes)
    no_vehicles_in_green_lanes = len(vehicles_in_green_lanes)

    vehicles_waiting_time = vehicle_waiting_time_in_lane(vehicles_in_red_lanes)

    if vehicles_waiting_time != 0:
        vehicles_waiting_time.sort()
        max_waiting_time_in_red_lanes = vehicles_waiting_time[-1]
        sum_wt_time = sum(vehicles_waiting_time)
        total_vehicle_waiting_time += sum_wt_time

    if (step > 0) and (step % 7) == 0:
        traffic_command = fuzzy_controller_function(no_vehicles_in_red_lanes,
                                                    no_vehicles_in_green_lanes,
                                                    max_waiting_time_in_red_lanes)

        if traffic_command >= 0.5:
            current_phase = traci.trafficlight.getPhase("J2")
            if current_phase < 5:
                traci.trafficlight.setPhase("J2", 4)
            else:
                traci.trafficlight.setPhase("J2", 9)
        print('done')

    traci.simulationStep()
    step += 1

print(total_vehicle_waiting_time)

traci.close()