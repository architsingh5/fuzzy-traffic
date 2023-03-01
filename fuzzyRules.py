import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

max_queue_length_curr = 60
max_green_signal_time = 60
max_queue_length_other = max_queue_length_curr * 3
max_waiting_time = max_green_signal_time * 3
a = max_queue_length_curr/5
b = max_queue_length_other/5
c = max_waiting_time/5
d = max_green_signal_time/5

queue_length_curr = ctrl.Antecedent(np.arange(0, max_queue_length_curr+1, 1), "queue_length_curr")
queue_length_other = ctrl.Antecedent(np.arange(0, max_queue_length_other+1, 1), "queue_length_other")
max_waiting_time = ctrl.Antecedent(np.arange(0, max_waiting_time+1, 1), "max_waiting_time")

green_signal_time = ctrl.Consequent(np.arange(0, max_green_signal_time+1, 1), "green_signal_time")

level = ["low", "med", "high"]

queue_length_curr.automf(3, names=level)
queue_length_other.automf(3, names=level)
max_waiting_time.automf(3, names=level)

# queue_length_curr['low'] = fuzz.trapmf(queue_length_curr.universe ,  [0, 0, 0, a*2] )
# queue_length_curr['med'] = fuzz.trapmf(queue_length_curr.universe ,  [a, a*2, a*3, a*4] )
# queue_length_curr['high'] = fuzz.trapmf(queue_length_curr.universe ,  [a*3, a*4, a*5, a*5] )

# queue_length_other['low'] = fuzz.trapmf(queue_length_other.universe ,  [0, 0, 0, b*2] )
# queue_length_other['med'] = fuzz.trapmf(queue_length_other.universe ,  [b, b*2, b*3, b*4] )
# queue_length_other['high'] = fuzz.trapmf(queue_length_other.universe ,  [b*3, b*4, b*5, b*5] )

# max_waiting_time['low'] = fuzz.trapmf(max_waiting_time.universe ,  [0, 0, 0, c*2] )
# max_waiting_time['med'] = fuzz.trapmf(max_waiting_time.universe ,  [c, c*2, c*3, c*4] )
# max_waiting_time['high'] = fuzz.trapmf(max_waiting_time.universe ,  [c*3, c*4, c*5, c*5] )

# queue_length_curr.view()
# queue_length_other.view()
# max_waiting_time.view()

green_signal_time.automf(3, names=level)

# green_signal_time['low'] = fuzz.trapmf(green_signal_time.universe ,  [0, 0, 0, d*2] )
# green_signal_time['med'] = fuzz.trapmf(green_signal_time.universe ,  [d, d*2, d*3, d*4] )
# green_signal_time['high'] = fuzz.trapmf(green_signal_time.universe ,  [d*3, d*4, d*5, d*5] )

# green_signal_time.view()

rule1 = ctrl.Rule(
    queue_length_curr["low"],
    green_signal_time["low"],
)
rule10 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["low"] & max_waiting_time["low"],
    green_signal_time["med"],
)
rule11 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["low"] & max_waiting_time["med"],
    green_signal_time["med"],
)
rule12 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["low"] & max_waiting_time["high"],
    green_signal_time["med"],
)
rule13 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["med"] & max_waiting_time["low"],
    green_signal_time["med"],
)
rule14 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["med"] & max_waiting_time["med"],
    green_signal_time["low"],
)
rule15 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["med"] & max_waiting_time["high"],
    green_signal_time["med"],
)
rule16 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["high"] & max_waiting_time["low"],
    green_signal_time["low"],
)
rule17 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["high"] & max_waiting_time["med"],
    green_signal_time["low"],
)
rule18 = ctrl.Rule(
    queue_length_curr["med"] & queue_length_other["high"] & max_waiting_time["high"],
    green_signal_time["med"],
)
rule19 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["low"] & max_waiting_time["low"],
    green_signal_time["high"],
)
rule20 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["low"] & max_waiting_time["med"],
    green_signal_time["high"],
)
rule21 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["low"] & max_waiting_time["high"],
    green_signal_time["high"],
)
rule22 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["med"] & max_waiting_time["low"],
    green_signal_time["high"],
)
rule23 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["med"] & max_waiting_time["med"],
    green_signal_time["high"],
)
rule24 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["med"] & max_waiting_time["high"],
    green_signal_time["high"],
)
rule25 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["high"] & max_waiting_time["low"],
    green_signal_time["med"],
)
rule26 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["high"] & max_waiting_time["med"],
    green_signal_time["med"],
)
rule27 = ctrl.Rule(
    queue_length_curr["high"] & queue_length_other["high"] & max_waiting_time["high"],
    green_signal_time["med"],
)


GST_control = ctrl.ControlSystem(
    [
        rule1,
        rule10,
        rule11,
        rule12,
        rule13,
        rule14,
        rule15,
        rule16,
        rule17,
        rule18,
        rule19,
        rule20,
        rule21,
        rule22,
        rule23,
        rule24,
        rule25,
        rule26,
        rule27,
    ]
)

gst_control_sim = ctrl.ControlSystemSimulation(GST_control)


def fuzzy_controller_function(queue_length_curr, queue_length_other, max_waiting_time):

    gst_control_sim.input["queue_length_curr"] = queue_length_curr
    gst_control_sim.input["queue_length_other"] = queue_length_other
    gst_control_sim.input["max_waiting_time"] = max_waiting_time

    gst_control_sim.compute()

    output = gst_control_sim.output["green_signal_time"]
    # green_signal_time.view(sim=gst_control_sim)
    # plt.show()
    return round(output)

if __name__ == "__main__":
    queue_length_curr.view()
    queue_length_other.view()
    max_waiting_time.view()
    green_signal_time.view()
    plt.show()
    # print(fuzzy_controller_function(0, 0, 0))