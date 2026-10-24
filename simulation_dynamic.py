import os
import sys
import traci
from fuzzyRules import fuzzy_controller_function as getGST
from simulation_static import edges, print_results, run_steps, simulation_time, yellow_time

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

tripinfo_file = "tripinfo_dynamic.xml"

sumo_binary = "sumo"
sumo_cmd = [
    sumo_binary, "-c", "junction.sumocfg", "--start",
    # per-vehicle results (incl. vehicles still driving at the end) used for the metrics
    "--tripinfo-output", tripinfo_file,
    "--tripinfo-output.write-unfinished",
    "--device.emissions.probability", "1",
]


def set_lane_time(edge, green_phase):

    no_of_vehicles = traci.edge.getLastStepVehicleNumber(edge)
    no_of_vehicles_other = 0

    for other_edge in edges:
        if other_edge != edge:
            no_of_vehicles_other += traci.edge.getLastStepVehicleNumber(other_edge)

    maximum_waiting_time = 0
    for vehicle in traci.edge.getLastStepVehicleIDs(edge):
        maximum_waiting_time = max(
            maximum_waiting_time, traci.vehicle.getWaitingTime(vehicle)
        )

    gst = getGST(no_of_vehicles, no_of_vehicles_other, maximum_waiting_time)
    if(no_of_vehicles==0):
        gst=3

    traci.trafficlight.setPhase("J2", green_phase)
    traci.trafficlight.setPhaseDuration("J2", gst)
    run_steps(gst)

    traci.trafficlight.setPhase("J2", green_phase + 1)
    traci.trafficlight.setPhaseDuration("J2", yellow_time)
    run_steps(yellow_time)


def dynamic_tls():
    traci.start(sumo_cmd)
    lane = 0

    while traci.simulation.getTime() < simulation_time:
        set_lane_time(edges[lane], 2 * lane)
        lane = (lane + 1) % len(edges)

    traci.close()
    print_results(tripinfo_file)

if __name__ == "__main__":
    dynamic_tls()
