import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


def get_emv(vehicleIDList):
    emv_list = []
    for vehicleID in vehicleIDList:
        if vehicleID.startswith('emergency-route'):
            emv_list.append(vehicleID);
    return emv_list


def current_moving_lane(trafficLightID):
    if traci.trafficlight.getRedYellowGreenState(trafficLightID).startswith('rrrr'):
        return 'WE'
    else:
        return 'NS'


def get_lane_lists(traffic_lanes_in_x_axis, traffic_lanes_in_y_axis, trafficLightID):
    """

    :param traffic_lanes_in_x_axis:  list
        lanes controlled by traffic light in the x-axis
    :param traffic_lanes_in_y_axis: list
        lanes controlled by traffic light in the y-axis
    :return: green_light_lanes: array
        list of lanes currently moving.
    ::return: red_light_lanes: array
        list of lanes blocked by traffic

    """
    if current_moving_lane(trafficLightID) == 'WE':
        return traffic_lanes_in_x_axis, traffic_lanes_in_y_axis
    else:
        return traffic_lanes_in_y_axis, traffic_lanes_in_x_axis


def get_vehicles_in_lane(array_of_lane_id):
    """

    :param array_of_lane_id: list
        a list containing the IDs of the lanes to get vehicles from
    :return: vehicles: list
        a list of all vehicles in the lanes

    """
    vehicles = []
    for laneIDs in array_of_lane_id:
        vehicles = vehicles + list(traci.lane.getLastStepVehicleIDs(laneIDs))
    return vehicles


def vehicle_waiting_time_in_lane(vehicle_list):
    waiting_times = []
    for vehicle in vehicle_list:
        waiting_times.append(traci.vehicle.getAccumulatedWaitingTime(vehicle))
    if len(waiting_times) == 0:
        return 0
    else:
        return waiting_times


def get_emv_waiting_time(vehicle_list):
    emvs_on_the_lane = get_emv(vehicle_list)
    emv_waiting_time = vehicle_waiting_time_in_lane(emvs_on_the_lane)
    if emv_waiting_time != 0:
        return sum(emv_waiting_time)
    return 0
