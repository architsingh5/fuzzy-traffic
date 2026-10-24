"""Compare a fixed-time and a fuzzy-logic controller for the traffic light J2 in SUMO.

Usage: python simulation.py [static] [dynamic]   (runs both when no controller is given)
"""
import argparse
import os
import xml.etree.ElementTree as ET

import sumolib
import traci

from fuzzyRules import fuzzy_controller_function

SUMO_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "junction.sumocfg")

TLS_ID = "J2"
# incoming edges in the order of their green phases (0, 2, 4, 6) in junction.net.xml
EDGES = ["E2", "-E1", "-E3", "E0"]

STATIC_GREEN_TIME = 40
EMPTY_LANE_GREEN_TIME = 3
YELLOW_TIME = 3
SIMULATION_TIME = 1000


def static_green_time(edge):
    return STATIC_GREEN_TIME


def fuzzy_green_time(edge):
    queue_length = traci.edge.getLastStepVehicleNumber(edge)
    if queue_length == 0:
        return EMPTY_LANE_GREEN_TIME

    queue_length_other = sum(
        traci.edge.getLastStepVehicleNumber(other_edge) for other_edge in EDGES if other_edge != edge
    )
    max_waiting_time = max(
        traci.vehicle.getWaitingTime(vehicle) for vehicle in traci.edge.getLastStepVehicleIDs(edge)
    )
    return fuzzy_controller_function(queue_length, queue_length_other, max_waiting_time)


# controller name -> (green time function, SUMO trip output file)
CONTROLLERS = {
    "static": (static_green_time, "tripinfo_static.xml"),
    "dynamic": (fuzzy_green_time, "tripinfo_dynamic.xml"),
}


def run_steps(no_of_steps):
    for _ in range(no_of_steps):
        # end every controller at exactly the same time so their results are comparable
        if traci.simulation.getTime() >= SIMULATION_TIME:
            return
        traci.simulationStep()


def print_results(tripinfo_file):
    # vehicles that never got into the network have depart="-1"
    vehicles = [
        trip for trip in ET.parse(tripinfo_file).getroot().iter("tripinfo")
        if float(trip.get("depart")) >= 0
    ]
    no_of_vehicles_crossed = sum(1 for trip in vehicles if float(trip.get("arrival")) >= 0)
    total_waiting_time = sum(float(trip.get("waitingTime")) for trip in vehicles)
    # emission values are in mg
    total_CO2_emission = sum(float(trip.find("emissions").get("CO2_abs")) for trip in vehicles)
    total_fuel_consumption = sum(float(trip.find("emissions").get("fuel_abs")) for trip in vehicles)

    print("Total vehicles crossed:", no_of_vehicles_crossed)
    print("Average waiting time:", round(total_waiting_time / len(vehicles), 2))
    print("total CO2 emission : ", round(total_CO2_emission / 1000, 2), " grams ")
    print("total fuel consumption : ", round(total_fuel_consumption / 1000, 2), " grams")


def run(green_time, tripinfo_file):
    traci.start([
        sumolib.checkBinary("sumo"), "-c", SUMO_CONFIG, "--start",
        # per-vehicle results (incl. vehicles still driving at the end) used for the metrics
        "--tripinfo-output", tripinfo_file,
        "--tripinfo-output.write-unfinished",
        "--device.emissions.probability", "1",
    ])
    lane = 0

    while traci.simulation.getTime() < SIMULATION_TIME:
        gst = green_time(EDGES[lane])

        traci.trafficlight.setPhase(TLS_ID, 2 * lane)
        traci.trafficlight.setPhaseDuration(TLS_ID, gst)
        run_steps(gst)

        traci.trafficlight.setPhase(TLS_ID, 2 * lane + 1)
        traci.trafficlight.setPhaseDuration(TLS_ID, YELLOW_TIME)
        run_steps(YELLOW_TIME)

        lane = (lane + 1) % len(EDGES)

    traci.close()
    print_results(tripinfo_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("controllers", nargs="*", choices=list(CONTROLLERS), default=list(CONTROLLERS))
    for name in parser.parse_args().controllers:
        print(f"==={name.upper()}===")
        run(*CONTROLLERS[name])
        print()
