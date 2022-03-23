import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

no_vehicle_current_lane = ctrl.Antecedent(np.arange(0, 23, 1), 'no_vehicle_current_lane')
no_vehicle_other_lane = ctrl.Antecedent(np.arange(0, 23, 1), 'no_vehicle_other_lane')

waiting_time_current_lane = ctrl.Antecedent(np.arange(0, 100, 1), 'waiting_time_current_lane')

# emergency_vehicles_in_other_lane = ctrl.Antecedent(np.arange(0, 3, 1), 'emergency_vehicles_in_other_lane')
# emergency_vehicles_in_current_lane = ctrl.Antecedent(np.arange(0, 3, 1), 'emergency_vehicles_in_current_lane')

# emv_waiting_time_green_lane = ctrl.Antecedent(np.arange(0, 50, 1), 'emv_waiting_time_green_lane')
# emv_waiting_time_red_lane = ctrl.Antecedent(np.arange(0, 50, 1), 'emv_waiting_time_red_lane')

traffic_light_signal = ctrl.Consequent(np.arange(0, 2, 1), 'traffic_light_signal')

no_vehicle_current_lane['too-small'] = fuzz.trimf(no_vehicle_current_lane.universe, [0, 0, 10])
no_vehicle_current_lane['small'] = fuzz.trimf(no_vehicle_current_lane.universe, [5, 10, 15])
no_vehicle_current_lane['much'] = fuzz.trimf(no_vehicle_current_lane.universe, [10, 15, 20])
no_vehicle_current_lane['too-much'] = fuzz.smf(no_vehicle_current_lane.universe, 15, 20)
# no_vehicle_current_lane.view()

no_vehicle_other_lane['too-small'] = fuzz.trimf(no_vehicle_other_lane.universe, [0, 0, 10])
no_vehicle_other_lane['small'] = fuzz.trimf(no_vehicle_other_lane.universe, [5, 10, 15])
no_vehicle_other_lane['much'] = fuzz.trimf(no_vehicle_other_lane.universe, [10, 15, 20])
no_vehicle_other_lane['too-much'] = fuzz.smf(no_vehicle_other_lane.universe, 15, 20)
# no_vehicle_other_lane.view()

waiting_time_current_lane['negligible'] = fuzz.trimf(waiting_time_current_lane.universe, [0, 0, 36])
waiting_time_current_lane['okay'] = fuzz.trimf(waiting_time_current_lane.universe, [16, 36, 56])
waiting_time_current_lane['much'] = fuzz.trimf(waiting_time_current_lane.universe, [36, 56, 76])
waiting_time_current_lane['too-much'] = fuzz.smf(waiting_time_current_lane.universe, 56, 80)
# waiting_time_current_lane.view()

# emv_waiting_time_green_lane['negligible'] = fuzz.trimf(emv_waiting_time_green_lane.universe, [0, 0, 20])
# emv_waiting_time_green_lane['okay'] = fuzz.trimf(emv_waiting_time_green_lane.universe, [10, 20, 30])
# emv_waiting_time_green_lane['much'] = fuzz.trimf(emv_waiting_time_green_lane.universe, [20, 30, 40])
# emv_waiting_time_green_lane['too-much'] = fuzz.smf(emv_waiting_time_green_lane.universe, 30, 40)
# # emv_waiting_time_green_lane.view()

# emv_waiting_time_red_lane['negligible'] = fuzz.trimf(emv_waiting_time_red_lane.universe, [0, 0, 20])
# emv_waiting_time_red_lane['okay'] = fuzz.trimf(emv_waiting_time_red_lane.universe, [10, 20, 30])
# emv_waiting_time_red_lane['much'] = fuzz.trimf(emv_waiting_time_red_lane.universe, [20, 30, 40])
# emv_waiting_time_red_lane['too-much'] = fuzz.smf(emv_waiting_time_red_lane.universe, 30, 40)
# # emv_waiting_time_red_lane.view()

# emergency_vehicles_in_current_lane['absent'] = fuzz.zmf(emergency_vehicles_in_current_lane.universe, 0, 1)
# emergency_vehicles_in_current_lane['present'] = fuzz.smf(emergency_vehicles_in_current_lane.universe, 0, 1)
# emergency_vehicles_in_current_lane['much'] = fuzz.smf(emergency_vehicles_in_current_lane.universe, 1, 2)
# # emergency_vehicles_in_current_lane.view()

# emergency_vehicles_in_other_lane['absent'] = fuzz.zmf(emergency_vehicles_in_other_lane.universe, 0, 1)
# emergency_vehicles_in_other_lane['present'] = fuzz.smf(emergency_vehicles_in_other_lane.universe, 0, 1)
# emergency_vehicles_in_other_lane['much'] = fuzz.smf(emergency_vehicles_in_other_lane.universe, 1, 2)
# # emergency_vehicles_in_other_lane.view()

traffic_light_signal['need-switching'] = fuzz.smf(traffic_light_signal.universe, 0, 1)
traffic_light_signal['okay'] = fuzz.zmf(traffic_light_signal.universe, 0, 1)
# traffic_light_signal.view()

##### FUNCTIONS THAT PASSS IN THE INPUT ####
### no_vehicle_current_lane too-small small much  too-much

# rule0a = ctrl.Rule(emergency_vehicles_in_current_lane['much'] & emergency_vehicles_in_other_lane['absent']
#                    | emergency_vehicles_in_current_lane['present'] & emergency_vehicles_in_other_lane['absent']
#                    | emergency_vehicles_in_current_lane['much'] & emergency_vehicles_in_other_lane['present'],
#                    traffic_light_signal['okay'])

# rule0b = ctrl.Rule(emergency_vehicles_in_current_lane['absent'] & emergency_vehicles_in_other_lane['present']
#                    | emergency_vehicles_in_current_lane['present'] & emergency_vehicles_in_other_lane['much']
#                    | emergency_vehicles_in_current_lane['absent'] & emergency_vehicles_in_other_lane['much'],
#                    traffic_light_signal['need-switching'])

rule1a = ctrl.Rule(no_vehicle_current_lane['small'] & no_vehicle_other_lane['too-small']
                   | no_vehicle_current_lane['much'] & no_vehicle_other_lane['too-small']
                   | no_vehicle_current_lane['too-much'] & no_vehicle_other_lane['too-small'],
                   traffic_light_signal['okay'])

rule1b = ctrl.Rule(no_vehicle_current_lane['much'] & no_vehicle_other_lane['small']
                   | no_vehicle_current_lane['too-much'] & no_vehicle_other_lane['small']
                   | no_vehicle_current_lane['too-much'] & no_vehicle_other_lane['much'],
                   traffic_light_signal['okay'])

rule1c = ctrl.Rule(no_vehicle_current_lane['too-small'] & no_vehicle_other_lane['small']
                   | no_vehicle_current_lane['too-small'] & no_vehicle_other_lane['much']
                   | no_vehicle_current_lane['small'] & no_vehicle_other_lane['much'],
                   traffic_light_signal['need-switching'])

rule1d = ctrl.Rule(no_vehicle_current_lane['too-small'] & no_vehicle_other_lane['too-much']
                   | no_vehicle_current_lane['small'] & no_vehicle_other_lane['too-much']
                   | no_vehicle_current_lane['much'] & no_vehicle_other_lane['too-much'],
                   traffic_light_signal['need-switching'])

rule2a = ctrl.Rule(waiting_time_current_lane['negligible'] | waiting_time_current_lane['okay']
                   , traffic_light_signal['okay'])

rule2b = ctrl.Rule(waiting_time_current_lane['much'] | waiting_time_current_lane['too-much']
                   , traffic_light_signal['need-switching'])

# rule3a = ctrl.Rule(emv_waiting_time_green_lane['okay'] & emv_waiting_time_red_lane['negligible']
#                    | emv_waiting_time_green_lane['much'] & emv_waiting_time_red_lane['negligible']
#                    | emv_waiting_time_green_lane['too-much'] & emv_waiting_time_red_lane['negligible'],
#                    traffic_light_signal['okay'])

# rule3b = ctrl.Rule(emv_waiting_time_green_lane['much'] & emv_waiting_time_red_lane['okay']
#                    | emv_waiting_time_green_lane['too-much'] & emv_waiting_time_red_lane['okay']
#                    | emv_waiting_time_green_lane['too-much'] & emv_waiting_time_red_lane['much'],
#                    traffic_light_signal['okay'])

# rule3c = ctrl.Rule(emv_waiting_time_green_lane['negligible'] & emv_waiting_time_red_lane['okay']
#                    | emv_waiting_time_green_lane['negligible'] & emv_waiting_time_red_lane['much']
#                    | emv_waiting_time_green_lane['okay'] & emv_waiting_time_red_lane['much'],
#                    traffic_light_signal['need-switching'])

# rule3d = ctrl.Rule(emv_waiting_time_green_lane['negligible'] & emv_waiting_time_red_lane['too-much']
#                    | emv_waiting_time_green_lane['okay'] & emv_waiting_time_red_lane['too-much']
#                    | emv_waiting_time_green_lane['much'] & emv_waiting_time_red_lane['too-much'],
#                    traffic_light_signal['need-switching'])

# without emv
traffic_light_ctrl = ctrl.ControlSystem([rule1a, rule1b, rule1c, rule1d, rule2a, rule2b])
# with emv
# traffic_light_ctrl = ctrl.ControlSystem([rule0a, rule0b, rule1a, rule1b, rule1c, rule1d, rule2a, rule2b, rule3a, rule3b, rule3c, rule3d])
traffic_status = ctrl.ControlSystemSimulation(traffic_light_ctrl)

def fuzzy_controller_function(no_vehicles_in_red_lanes,
                              no_vehicles_in_green_lanes,
                              max_waiting_time_in_red_lanes,
                              emv_waiting_time_red_lanes, emv_waiting_time_green_lanes,
                              emv_current_lane, emv_other_lane):


    traffic_status.input['no_vehicle_current_lane'] = int(no_vehicles_in_red_lanes)
    traffic_status.input['no_vehicle_other_lane'] = int(no_vehicles_in_green_lanes)
    # traffic_status.input['emergency_vehicles_in_current_lane'] = int(emv_current_lane)
    # traffic_status.input['emergency_vehicles_in_other_lane'] = int(emv_other_lane)
    # traffic_status.input['emv_waiting_time_red_lane'] = int(emv_waiting_time_red_lanes)
    # traffic_status.input['emv_waiting_time_green_lane'] = int(emv_waiting_time_green_lanes)
    traffic_status.input['waiting_time_current_lane'] = int(max_waiting_time_in_red_lanes)



    print('no_vehicles_in_red_lane ' + str(no_vehicles_in_red_lanes))
    print('no_vehicles_in_green_lane ' + str(no_vehicles_in_green_lanes))
    print('max_waiting_time_in_red_lane ' + str(max_waiting_time_in_red_lanes))
    # print('emv_current_lane ' + str(emv_current_lane))
    # print('emv_waiting_time_red_lane ' + str(emv_waiting_time_red_lanes))
    # print('emv_waiting_time_green_lane ' + str(emv_waiting_time_green_lanes))
    # print('emv_other_lane ' + str(emv_other_lane))


    traffic_status.compute()
    output = traffic_status.output['traffic_light_signal']
    print('output ' + str(output))
    return output