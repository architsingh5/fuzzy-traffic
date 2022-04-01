import os
import sys
import traci
import random
from fuzzyRules import fuzzy_controller_function as getGST

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

sumo_binary = "sumo-gui"
sumo_cmd = [sumo_binary, "-c", "junction.sumocfg", "--start"]


edges = ["E2", "-E1", "-E3", "E0"]

def set_lane_time(edge,step):
    no_of_vehicles = len(traci.edge.getLastStepVehicleIDs(edge))
    no_of_vehicles_other = 0

    for i in range(0,len(edges)):
        if(edges[i]!=edge):
            no_of_vehicles_other+=len(traci.edge.getLastStepVehicleIDs(edges[i]))

    vehicles_on_lane = traci.edge.getLastStepVehicleIDs(edge)
    maximum_waiting_time = 0

    for vehicle in vehicles_on_lane:
        maximum_waiting_time = max(maximum_waiting_time, traci.vehicle.getAccumulatedWaitingTime(vehicle))

    # if(len(vehicles_on_lane)>0):
    #     first_vehicle_waiting_time = traci.vehicle.getWaitingTime(vehicles_on_lane[0])

    gst = getGST(no_of_vehicles, no_of_vehicles_other, maximum_waiting_time)
    print(gst)

    # traci.trafficlight.setPhase("J2",0)
    traci.trafficlight.setPhaseDuration("J2", gst)

    current_lane_steps = 0
    while(current_lane_steps < gst+1):
        step += 1
        current_lane_steps+=1
        traci.simulationStep()

    print(traci.trafficlight.getRedYellowGreenState("J2"))
    traci.trafficlight.setPhaseDuration("J2",2)
    j=0
    while(j<2):
        step += 1
        j+=1
        traci.simulationStep()

    return step


def dynamic_tls():
    traci.start(sumo_cmd)
    step = 0
    total_vehicle_waiting_time = 0  
    total_no_of_vehicles_crossed = 0
    lane = 0

    while step < 1000:

        if(lane==0):
            lane = 1
            step=set_lane_time("E2",step)
            
        elif(lane==1):
            lane = 2
            step=set_lane_time("-E1",step)
        
        elif(lane==2):
            lane = 3
            step=set_lane_time("-E3",step)

        elif(lane==3):
            lane = 0
            step=set_lane_time("E0",step)
    
    traci.close()

# def dynamic_tls():
#     pass

if __name__ == "__main__":
    dynamic_tls()
    # dynamic_tls()
        # traci.simulationStep()
        # step += 1

# print(traci.trafficlight.getRedYellowGreenState(trafficLightID))
# print(traci.trafficlight.getPhaseDuration(trafficLightID))
# vechile_id = "vehicle_" + str(step)
# traci.vehicle.add(vechile_id, random.choice(routes))

# def get_vehicles_in_lane(array_of_lane_id):
#     vehicles = []
#     for laneIDs in array_of_lane_id:
#         vehicles = vehicles + list(traci.lane.getLastStepVehicleIDs(laneIDs))
#     return vehicles


# def vehicle_waiting_time_in_lane(vehicle_list):
#     waiting_times = []
#     for vehicle in vehicle_list:
#         waiting_times.append(traci.vehicle.getAccumulatedWaitingTime(vehicle))
#     if len(waiting_times) == 0:
#         return 0
#     else:
#         return waiting_times




# routes = ["route01","route02","route03","route04","route05","route06","route07","route08","route09","route10","route11","route12"]
# lanes = ["E0", "E1", "E2", "E3"]
# trafficLightID = traci.trafficlight.getIDList()[0]
# traci.
# route.add("route01", ["E0", "E3"])




# def current_moving_lane(trafficLightID):
#     if traci.trafficlight.getRedYellowGreenState(trafficLightID).startswith("rrrr"):
#         return "WE"
#     else:
#         return "NS"


# def get_lane_lists(traffic_lanes, trafficLightID):
#     """
#     :param traffic_lanes_in_x_axis:  list
#         lanes controlled by traffic light in the x-axis
#     :param traffic_lanes_in_y_axis: list
#         lanes controlled by traffic light in the y-axis
#     :return: green_light_lanes: array
#         list of lanes currently moving.
#     ::return: red_light_lanes: array
#         list of lanes blocked by traffic
#     """

# print(traci.trafficlight.getRedYellowGreenState(trafficLightID))
# print(traci.trafficlight.getPhaseDuration(trafficLightID))

# if current_moving_lane(trafficLightID) == "WE":
#     return traffic_lanes_in_x_axis, traffic_lanes_in_y_axis
# else:
#     return traffic_lanes_in_y_axis, traffic_lanes_in_x_axis


# def get_vehicles_in_lanes(lane_ids):
#     """

#     :param array_of_lane_id: list
#         a list containing the IDs of the lanes to get vehicles from
#     :return: vehicles: list
#         a list of all vehicles in the lanes

#     """
#     vehicles = []
#     for lane_id in lane_ids:
#         vehicles = vehicles + list(traci.lane.getLastStepVehicleIDs(lane_id))
#     return vehicles


# def vehicle_waiting_time_in_lane(vehicle_list):
#     waiting_times = []
#     for vehicle in vehicle_list:
#         waiting_times.append(traci.vehicle.getAccumulatedWaitingTime(vehicle))
#     if len(waiting_times) == 0:
#         return 0
#     else:
#         return waiting_times

# while step < 1000:
# print(traci.trafficlight.getRedYellowGreenState(trafficLightID))
# print(traci.trafficlight.getPhaseDuration(trafficLightID))

# lanes_currently_moving, lanes_stopped_by_light = get_lane_lists(
#     lanes, trafficLightID
# )

# get_lane_lists(lanes, trafficLightID)

# vehicles_in_red_lanes = get_vehicles_in_lanes(lanes_stopped_by_light)
# vehicles_in_green_lanes = get_vehicles_in_lanes(lanes_currently_moving)

# no_vehicles_in_red_lanes = len(vehicles_in_red_lanes)
# no_vehicles_in_green_lanes = len(vehicles_in_green_lanes)

# vehicles_waiting_time = vehicle_waiting_time_in_lane(vehicles_in_red_lanes)

# if vehicles_waiting_time != 0:
#     vehicles_waiting_time.sort()
#     max_waiting_time_in_red_lanes = vehicles_waiting_time[-1]
#     sum_wt_time = sum(vehicles_waiting_time)
#     total_vehicle_waiting_time += sum_wt_time

# traci.simulationStep()
# step += 1

# print(total_vehicle_waiting_time)

# traci.close()
