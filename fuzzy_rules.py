import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

no_vehicle_current_lane = ctrl.Antecedent(np.arange(0, 23, 1), 'no_vehicle_current_lane')
no_vehicle_other_lane = ctrl.Antecedent(np.arange(0, 23, 1), 'no_vehicle_other_lane')

waiting_time_current_lane = ctrl.Antecedent(np.arange(0, 100, 1), 'waiting_time_current_lane')

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

traffic_light_signal['need-switching'] = fuzz.smf(traffic_light_signal.universe, 0, 1)
traffic_light_signal['okay'] = fuzz.zmf(traffic_light_signal.universe, 0, 1)
# traffic_light_signal.view()


##### FUNCTIONS THAT PASSS IN THE INPUT ####
### no_vehicle_current_lane too-small small much  too-much

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

traffic_light_ctrl = ctrl.ControlSystem([rule1a, rule1b, rule1c, rule1d, rule2a, rule2b])
traffic_status = ctrl.ControlSystemSimulation(traffic_light_ctrl)

def fuzzy_controller_function(no_vehicles_in_red_lanes,
                              no_vehicles_in_green_lanes,
                              max_waiting_time_in_red_lanes):

    traffic_status.input['no_vehicle_current_lane'] = int(no_vehicles_in_red_lanes)
    traffic_status.input['no_vehicle_other_lane'] = int(no_vehicles_in_green_lanes)
    traffic_status.input['waiting_time_current_lane'] = int(max_waiting_time_in_red_lanes)

    print('no_vehicles_in_red_lane ' + str(no_vehicles_in_red_lanes))
    print('no_vehicles_in_green_lane ' + str(no_vehicles_in_green_lanes))
    print('max_waiting_time_in_red_lane ' + str(max_waiting_time_in_red_lanes))

    traffic_status.compute()
    output = traffic_status.output['traffic_light_signal']
    print('output ' + str(output))
    return output