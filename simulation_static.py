import os
import sys
import xml.etree.ElementTree as ET
import traci


if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

tripinfo_file = "tripinfo_static.xml"

sumo_binary = "sumo"
sumo_cmd = [
    sumo_binary, "-c", "junction.sumocfg", "--start",
    # per-vehicle results (incl. vehicles still driving at the end) used for the metrics
    "--tripinfo-output", tripinfo_file,
    "--tripinfo-output.write-unfinished",
    "--device.emissions.probability", "1",
]

# incoming edges in the order of their green phases (0, 2, 4, 6) in junction.net.xml
edges = ["E2", "-E1", "-E3", "E0"]

yellow_time = 3
simulation_time = 1000


def run_steps(no_of_steps):
    for _ in range(no_of_steps):
        # end both controllers at exactly the same time so their results are comparable
        if traci.simulation.getTime() >= simulation_time:
            return
        traci.simulationStep()


def set_lane_time(edge, green_phase):

    gst = 40

    traci.trafficlight.setPhase("J2", green_phase)
    traci.trafficlight.setPhaseDuration("J2", gst)
    run_steps(gst)

    traci.trafficlight.setPhase("J2", green_phase + 1)
    traci.trafficlight.setPhaseDuration("J2", yellow_time)
    run_steps(yellow_time)


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


def static_tls():
    traci.start(sumo_cmd)
    lane = 0

    while traci.simulation.getTime() < simulation_time:
        set_lane_time(edges[lane], 2 * lane)
        lane = (lane + 1) % len(edges)

    traci.close()
    print_results(tripinfo_file)

if __name__ == "__main__":
    static_tls()
