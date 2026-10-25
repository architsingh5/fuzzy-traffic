import numpy as np
from skfuzzy import control as ctrl

LEVELS = ["low", "med", "high"]

queue_length_curr = ctrl.Antecedent(np.arange(0, 26, 1), "queue_length_curr")
queue_length_other = ctrl.Antecedent(np.arange(0, 76, 1), "queue_length_other")
max_waiting_time = ctrl.Antecedent(np.arange(0, 91, 1), "max_waiting_time")

green_signal_time = ctrl.Consequent(np.arange(0, 61, 1), "green_signal_time")

for variable in (queue_length_curr, queue_length_other, max_waiting_time, green_signal_time):
    variable.automf(3, names=LEVELS)

# green signal time for each (queue_length_curr, queue_length_other) pair,
# given for a low, med and high max_waiting_time
RULE_TABLE = {
    ("low", "low"): ("low", "low", "low"),
    ("low", "med"): ("low", "low", "low"),
    ("low", "high"): ("low", "low", "low"),
    ("med", "low"): ("med", "med", "med"),
    ("med", "med"): ("med", "med", "med"),
    ("med", "high"): ("low", "low", "med"),
    ("high", "low"): ("high", "high", "high"),
    ("high", "med"): ("high", "high", "high"),
    ("high", "high"): ("high", "high", "high"),
}

rules = [
    ctrl.Rule(
        queue_length_curr[curr] & queue_length_other[other] & max_waiting_time[waiting],
        green_signal_time[green],
    )
    for (curr, other), greens in RULE_TABLE.items()
    for waiting, green in zip(LEVELS, greens)
]

gst_control_sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))


def fuzzy_controller_function(queue_length_curr, queue_length_other, max_waiting_time):

    gst_control_sim.input["queue_length_curr"] = queue_length_curr
    gst_control_sim.input["queue_length_other"] = queue_length_other
    gst_control_sim.input["max_waiting_time"] = max_waiting_time

    gst_control_sim.compute()

    # to plot the result (needs matplotlib): green_signal_time.view(sim=gst_control_sim)
    return round(gst_control_sim.output["green_signal_time"])
