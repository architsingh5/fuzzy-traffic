import os
import sys
import traci
import random
from fuzzyRules import fuzzy_controller_function as getGST
from simulation_static import static_tls

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

sumo_binary = "sumo"
sumo_cmd = [sumo_binary, "-c", "junction.sumocfg", "--start", "--duration-log.disable", "true", "--no-step-log", "true",
"--no-warnings", "true"]

edges = ["E2", "-E1", "-E3", "E0"]
return_edges = ["-E2", "E1", "E3", "-E0"]

total_no_of_vehicles_crossed = 0
total_waiting_time = 0
total_fuel_consumption = 0
total_CO2_emission = 0

def calculcate_vehicles_crossed(vehicles_crossed, vehicles_on_current_lane, edge):
    if edge[0] == "-":
        edge = edge[1:]
    else:
        edge = "-" + edge

    for return_edge in return_edges:
        if return_edge == edge:
            continue
        vehicles_on_lane = traci.edge.getLastStepVehicleIDs(return_edge)
        for vehicle in vehicles_on_lane:
            if vehicle not in vehicles_crossed and vehicle in vehicles_on_current_lane:
                vehicles_crossed.add(vehicle)


def set_lane_time(edge, step):

    global total_no_of_vehicles_crossed, total_waiting_time, total_fuel_consumption, total_CO2_emission

    no_of_vehicles = traci.edge.getLastStepVehicleNumber(edge)
    no_of_vehicles_other = 0

    for i in range(0, len(edges)):
        if edges[i] != edge:
            no_of_vehicles_other += traci.edge.getLastStepVehicleNumber(edges[i])

    vehicles_on_lane = traci.edge.getLastStepVehicleIDs(edge)
    # print("step traffic: ", len(vehicles_on_lane))
    maximum_waiting_time = 0

    vehicle_with_waiting_time = []
    # print("Lane:", edge, "No of vehicles:", len(vehicles_on_lane), "No of vehicles:", no_of_vehicles)

    for vehicle in vehicles_on_lane:
        # print("Waiting time of vehicle " + vehicle + " is " + str(traci.vehicle.getWaitingTime(vehicle)))
        # print("fuel consumption for vehicle " + vehicle + " is : " + str(traci.vehicle.getFuelConsumption(vehicle)))
        # print(traci.vehicle.getFuelConsumption(vehicle))
        vehicle_with_waiting_time.append(
            (vehicle, traci.vehicle.getWaitingTime(vehicle))
        )
        maximum_waiting_time = max(
            maximum_waiting_time, traci.vehicle.getWaitingTime(vehicle)
        )
        #print("step wt:", traci.vehicle.getWaitingTime(vehicle))

    gst = getGST(no_of_vehicles, no_of_vehicles_other, maximum_waiting_time)
    # print("gst: ", gst)
    # print(maximum_waiting_time, sep="\t")
    # print(no_of_vehicles_other)
    if(no_of_vehicles==0):
        gst=3
    # traci.trafficlight.setPhase("J2",0)

    traci.trafficlight.setPhaseDuration("J2", gst)

    current_lane_steps = 0
    vehicles_crossed = set()
    while current_lane_steps < gst + 1:
        step += 1
        current_lane_steps += 1
        calculcate_vehicles_crossed(vehicles_crossed, vehicles_on_lane, edge)
        for edge2 in edges:
            total_CO2_emission += traci.edge.getCO2Emission(edge2)
            total_fuel_consumption += traci.edge.getFuelConsumption(edge2)
        for edge2 in return_edges:
            total_CO2_emission += traci.edge.getCO2Emission(edge2)
            total_fuel_consumption += traci.edge.getFuelConsumption(edge2)
        traci.simulationStep()

    # print("No of vehicles crossed:", len(vehicles_crossed)+1)
    total_no_of_vehicles_crossed += len(vehicles_crossed)

    curr_waiting_time = 0
    for vehicle in vehicles_crossed:
        for that_vehicle in vehicle_with_waiting_time:
            if vehicle == that_vehicle[0]:
                curr_waiting_time += that_vehicle[1]
                total_waiting_time = total_waiting_time + that_vehicle[1]
    if(len(vehicles_crossed) > 0):
        print("Avg WT: ", curr_waiting_time/len(vehicles_crossed))

    traci.trafficlight.setPhase("J2", (traci.trafficlight.getPhase("J2") + 1) % 8)
    traci.trafficlight.setPhaseDuration("J2", 4)
    print(edge, "gst - ", gst, " " , no_of_vehicles, " ", no_of_vehicles_other, " ", maximum_waiting_time, " ", len(vehicles_crossed))

    j = 0
    while j < 1:
        step += 1
        j += 1
    #     traci.simulationStep()
    return step



def dynamic_tls():
    traci.start(sumo_cmd)
    step = 0
    lane = 0

    while step < 1000:

        if lane == 0:
            step = set_lane_time("E2", step)
            lane = 1

        elif lane == 1:
            step = set_lane_time("-E1", step)
            lane = 2

        elif lane == 2:
            step = set_lane_time("-E3", step)
            lane = 3

        elif lane == 3:
            step = set_lane_time("E0", step)
            lane = 0

    traci.close()

    print("Total vehicles crossed:", total_no_of_vehicles_crossed)
    print("Average waiting time:",round(total_waiting_time / total_no_of_vehicles_crossed, 2),)
    print("total CO2 emission : ", round(total_CO2_emission / 1000, 2), " grams ")
    print("total fuel consumption : ", round(total_fuel_consumption / 1000, 2), " liters")

if __name__ == "__main__":
    dynamic_tls()
