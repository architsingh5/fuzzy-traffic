import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

queue_length = ctrl.Antecedent(np.arange(0,31,1), 'queue_length')
waiting_time = ctrl.Antecedent(np.arange(0,61,1), 'waiting_time')
greenSignalTime = ctrl.Consequent(np.arange(0,25,1), 'greenSignalTime')

level = ['low', 'medium', 'high']

queue_length.automf(3, names=level)
waiting_time.automf(3, names=level)
greenSignalTime.automf(3, names=level)

queue_length.view()
waiting_time.view()
greenSignalTime.view()


# queue_length['low'] = fuzz.trimf(queue_length.universe, [0, 0, 5])
# queue_length['medium'] = fuzz.trimf(queue_length.universe, [0, 5, 10])
# queue_length['high'] = fuzz.trimf(queue_length.universe, [5, 10, 20])

# waiting_time['low'] = fuzz.trimf(waiting_time.universe, [0, 0, 10])
# waiting_time['medium'] = fuzz.trimf(waiting_time.universe, [0, 10, 20])
# waiting_time['high'] = fuzz.trimf(waiting_time.universe, [10, 20, 30])

# greenSignalTime['low'] = fuzz.trimf(greenSignalTime.universe, [0, 0, 3])
# greenSignalTime['medium'] = fuzz.trimf(greenSignalTime.universe, [0, 3, 7])
# greenSignalTime['high'] = fuzz.trimf(greenSignalTime.universe, [7, 10, 10])


rule1 = ctrl.Rule(queue_length['low'] & waiting_time['low'], greenSignalTime['low'])
rule2 = ctrl.Rule(queue_length['low'] & waiting_time['medium'], greenSignalTime['medium'])
rule3 = ctrl.Rule(queue_length['low'] & waiting_time['high'], greenSignalTime['high'])
rule4 = ctrl.Rule(queue_length['medium'] & waiting_time['low'], greenSignalTime['low'])
rule5 = ctrl.Rule(queue_length['medium'] & waiting_time['medium'], greenSignalTime['medium'])
rule6 = ctrl.Rule(queue_length['medium'] & waiting_time['high'], greenSignalTime['high'])
rule7 = ctrl.Rule(queue_length['high'] & waiting_time['low'], greenSignalTime['low'])
rule8 = ctrl.Rule(queue_length['high'] & waiting_time['medium'], greenSignalTime['medium'])
rule9 = ctrl.Rule(queue_length['high'] & waiting_time['high'], greenSignalTime['high'])

GST_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

GST_control_sim = ctrl.ControlSystemSimulation(GST_control)

GST_control_sim.input['queue_length'] = 25
GST_control_sim.input['waiting_time'] = 20

GST_control_sim.compute()

print(GST_control_sim.output['greenSignalTime'])
greenSignalTime.view(sim=GST_control_sim)
plt.show()
