import os
import sys
import traci
from fuzzyRules import fuzzy_controller_function as getGST
import matplotlib.pyplot as plt
iteration = 0
x=[]
y=[]

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

sumo_binary = "sumo"
sumo_cmd = [sumo_binary, "-c", "junction.sumocfg", "--start", "--duration-log.disable", "true", "--no-step-log", "true", "--no-warnings", "true"]

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

def update_vehicle_on_lane(vechicles_on_lane,edge):
    vehicles_at_opening = traci.edge.getLastStepVehicleIDs(edge)
    for vehicle in vehicles_at_opening:
        vechicles_on_lane.add(vehicle)

def set_lane_time(edge, step, total_steps):

    global total_no_of_vehicles_crossed, total_waiting_time, total_fuel_consumption, total_CO2_emission

    no_of_vehicles = traci.edge.getLastStepVehicleNumber(edge)
    no_of_vehicles_other = 0

    for i in range(0, len(edges)):
        if edges[i] != edge:
            no_of_vehicles_other += traci.edge.getLastStepVehicleNumber(edges[i])

    vehicles_at_opening = traci.edge.getLastStepVehicleIDs(edge)
    maximum_waiting_time = 0

    vehicles_on_lane = set()
    for vehicle in vehicles_at_opening:
        vehicles_on_lane.add(vehicle)

    vehicle_with_waiting_time = []

    for vehicle in vehicles_on_lane:
        vehicle_with_waiting_time.append((vehicle, traci.vehicle.getWaitingTime(vehicle)))
        maximum_waiting_time = max(maximum_waiting_time, traci.vehicle.getWaitingTime(vehicle))

    traci.simulationStep()

    gst = getGST(no_of_vehicles, no_of_vehicles_other, maximum_waiting_time)
    # print("Edge", edge,end=" ")
    # print("No of Vehicles", no_of_vehicles,"No of Vehicles Other", no_of_vehicles_other,"Maximum Waiting Time", maximum_waiting_time,end=" ")
    
    # print("GST", gst)

    global x,y,iteration
    iteration+=1
    x.append(iteration)
    y.append(gst)
    
    traci.trafficlight.setPhaseDuration("J2", gst-1)

    current_lane_steps = 0
    vehicles_crossed = set()
    while current_lane_steps < gst:
        step += 1
        current_lane_steps += 1
        update_vehicle_on_lane(vehicles_on_lane,edge)
        calculcate_vehicles_crossed(vehicles_crossed, vehicles_on_lane, edge)
        for edge2 in edges:
            # total_CO2_emission += traci.edge.getCO2Emission(edge2)
            total_fuel_consumption += traci.edge.getFuelConsumption(edge2)
        for edge2 in return_edges:
            # total_CO2_emission += traci.edge.getCO2Emission(edge2)
            total_fuel_consumption += traci.edge.getFuelConsumption(edge2)
        traci.simulationStep()
        if(step==total_steps):
            break

    # curr_waiting_time = 0
    for vehicle in vehicles_crossed:
        for that_vehicle in vehicle_with_waiting_time:
            if vehicle == that_vehicle[0]:
                # curr_waiting_time += that_vehicle[1]
                total_waiting_time = total_waiting_time + that_vehicle[1]
    
    yellow_light_time = 5
    yellow_light_time = yellow_light_time-1

    # traci.trafficlight.setPhase("J2", (traci.trafficlight.getPhase("J2") + 1) % 8)
    traci.trafficlight.setPhaseDuration("J2", yellow_light_time)

    j = 0
    while j < yellow_light_time+1 and step<total_steps:
        step += 1
        j += 1
        for edge2 in edges:
            # total_CO2_emission += traci.edge.getCO2Emission(edge2)
            total_fuel_consumption += traci.edge.getFuelConsumption(edge2)
        for edge2 in return_edges:
            # total_CO2_emission += traci.edge.getCO2Emission(edge2)
            total_fuel_consumption += traci.edge.getFuelConsumption(edge2)
        if(j!=yellow_light_time):
            traci.simulationStep()
        if(step==total_steps):
            break

    calculcate_vehicles_crossed(vehicles_crossed, vehicles_on_lane, edge)

    no_of_vehicle_crossed = len(vehicles_crossed)

    total_no_of_vehicles_crossed += no_of_vehicle_crossed

    # print("No of Vehicles Crossed", no_of_vehicle_crossed)

    return step



def dynamic_tls():
    traci.start(sumo_cmd)
    step = 0
    lane = 0

    total_steps = 3600
    while step < total_steps:

        if lane == 0:
            step = set_lane_time("E2", step, total_steps)
            lane = 1

        elif lane == 1:
            step = set_lane_time("-E1", step, total_steps)
            lane = 2

        elif lane == 2:
            step = set_lane_time("-E3", step, total_steps)
            lane = 3

        elif lane == 3:
            step = set_lane_time("E0", step, total_steps)
            lane = 0

        # print(step)

    traci.close()

    average_waiting_time = round(total_waiting_time / total_no_of_vehicles_crossed, 2)

    print("Total vehicles crossed:", total_no_of_vehicles_crossed)
    print("Average waiting time:", average_waiting_time, "seconds")
    # print("total CO2 emission : ", round(total_CO2_emission / 1000, 2), " grams ")
    print("total fuel consumption : ", round(total_fuel_consumption / 1000, 2), " liters")

    return total_no_of_vehicles_crossed, average_waiting_time, total_CO2_emission, total_fuel_consumption

if __name__ == "__main__":
    dynamic_tls()
    plt.plot(x,y)
    plt.show()
