import os
import sys
from xml.etree.ElementTree import tostring
import traci
import random

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

sumo_binary = "sumo-gui"
sumo_cmd = [sumo_binary, "-c", "junction.sumocfg", "--start"]

# routes = ["route01","route02","route03","route04","route05","route06","route07","route08","route09","route10","route11","route12"]
# lanes = ["E0", "E1", "E2", "E3"]
# trafficLightID = traci.trafficlight.getIDList()[0]
# traci.route.add("route01", ["E0", "E3"])

def static_tls():
    traci.start(sumo_cmd)
    step = 0
    total_vehicle_waiting_time = 0  
    total_no_of_vehicles_crossed = 0

    while step < 1000:
        # print(traci.trafficlight.getRedYellowGreenState(trafficLightID))
        # print(traci.trafficlight.getPhaseDuration(trafficLightID))
        # vechile_id = "vehicle_" + str(step)
        # traci.vehicle.add(vechile_id, random.choice(routes))
        traci.simulationStep()
        step += 1

    traci.close()


def dynamic_tls():
    pass


if __name__ == "__main__":
    static_tls()
    # dynamic_tls()






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
