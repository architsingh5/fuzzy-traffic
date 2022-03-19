import sys
import os
#checking is sumo is installed or not
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    # add tools to path
    # sys.path is a built-in variable within the sys module. 
    # It contains a list of directories that the interpreter will search 
    # in for the required module.
    sys.path.append(tools)
else:
    # SUMO_HOME is not setted or not installed
    sys.exit("please declare environment variable 'SUMO_HOME'")


sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "4-junction/4-junction.sumocfg", "--start"]

print(sumoBinary)
print(sumoCmd)

import traci
traci.start(sumoCmd)