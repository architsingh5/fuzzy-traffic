import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

queue_length_curr = ctrl.Antecedent(np.arange(0, 61, 1), "queue_length_curr")
queue_length_other = ctrl.Antecedent(np.arange(0, 183, 1), "queue_length_other")
max_waiting_time = ctrl.Antecedent(np.arange(0, 91, 1), "max_waiting_time")

green_signal_time = ctrl.Consequent(np.arange(0, 61, 1), "green_signal_time")

level = ["low", "med", "high"]

queue_length_curr.automf(3, names=level)
queue_length_other.automf(3, names=level)
max_waiting_time.automf(3, names=level)

# queue_length_curr.view()
# queue_length_other.view()
# max_waiting_time.view()

green_signal_time.automf(3, names=level)

# green_signal_time.view()

rule1 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["low"] & max_waiting_time["low"],
    green_signal_time["low"],
)
rule2 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["low"] & max_waiting_time["med"],
    green_signal_time["low"],
)
rule3 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["low"] & max_waiting_time["high"],
    green_signal_time["low"],
)
rule4 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["med"] & max_waiting_time["low"],
    green_signal_time["low"],
)
rule5 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["med"] & max_waiting_time["med"],
    green_signal_time["low"],
)
rule6 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["med"] & max_waiting_time["high"],
    green_signal_time["low"],
)
rule7 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["high"] & max_waiting_time["low"],
    green_signal_time["low"],
)
rule8 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["high"] & max_waiting_time["med"],
    green_signal_time["low"],
)
rule9 = ctrl.Rule(
    queue_length_curr["low"] & queue_length_other["high"] & max_waiting_time["high"],
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
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8,
        rule9,
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

