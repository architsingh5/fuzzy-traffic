"""Black-box measurements of the project's behaviour, shared by the tests and generate_golden.py.

Only the entry points are used (`fuzzy_controller_function` and `python simulation.py`), so the
same golden values check any refactor of the code behind them.
"""
import itertools
import json
import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLDEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden")
FUZZY_GOLDEN = os.path.join(GOLDEN_DIR, "fuzzy_controller.json")
SIMULATION_GOLDEN = os.path.join(GOLDEN_DIR, "simulation.json")

# (queue_length_curr, queue_length_other, max_waiting_time) inputs, including values above the
# fuzzy universes (25 vehicles, 75 vehicles, 90 s) that the simulation does produce
FUZZY_QUEUE_LENGTHS_CURR = range(0, 31)
FUZZY_QUEUE_LENGTHS_OTHER = range(0, 81, 10)
FUZZY_MAX_WAITING_TIMES = range(0, 121, 15)

METRIC_PATTERN = re.compile(
    r"^(Total vehicles crossed|Average waiting time|total CO2 emission|total fuel consumption)"
    r"\s*:\s*(\S+)"
)


def fuzzy_outputs():
    """Green times as one row per queue_length_curr, ordered by queue_length_other, then max_waiting_time."""
    sys.path.insert(0, REPO_ROOT)
    from fuzzyRules import fuzzy_controller_function

    return [
        [
            fuzzy_controller_function(curr, other, waiting)
            for other, waiting in itertools.product(FUZZY_QUEUE_LENGTHS_OTHER, FUZZY_MAX_WAITING_TIMES)
        ]
        for curr in FUZZY_QUEUE_LENGTHS_CURR
    ]


def fuzzy_inputs_description():
    return {
        name: [values[0], values[-1], values.step]
        for name, values in [
            ("queue_length_curr", FUZZY_QUEUE_LENGTHS_CURR),
            ("queue_length_other", FUZZY_QUEUE_LENGTHS_OTHER),
            ("max_waiting_time", FUZZY_MAX_WAITING_TIMES),
        ]
    }


def sumo_home():
    """SUMO_HOME from the environment, else from the eclipse-sumo package, else None."""
    if os.environ.get("SUMO_HOME"):
        return os.environ["SUMO_HOME"]
    try:
        import sumo
    except ImportError:
        return None
    return sumo.SUMO_HOME


def sumo_available():
    home = sumo_home()
    return bool(home and os.path.exists(os.path.join(home, "bin", "sumo"))) or shutil.which("sumo") is not None


def simulation_metrics():
    """Run `python simulation.py` and return {controller: {metric: value}} from its output."""
    env = dict(os.environ)
    if sumo_home():
        env["SUMO_HOME"] = sumo_home()
        env["PATH"] = os.path.join(sumo_home(), "bin") + os.pathsep + env.get("PATH", "")
    output = subprocess.run(
        [sys.executable, "simulation.py"], cwd=REPO_ROOT, env=env,
        capture_output=True, text=True, check=True,
    ).stdout

    metrics = {}
    controller = None
    for line in output.splitlines():
        header = re.match(r"^===(\w+)===$", line.strip())
        if header:
            controller = header.group(1).lower()
            metrics[controller] = {}
            continue
        metric = METRIC_PATTERN.match(line.strip())
        if metric and controller:
            metrics[controller][metric.group(1)] = metric.group(2)
    return metrics


def load(path):
    with open(path) as golden:
        return json.load(golden)
