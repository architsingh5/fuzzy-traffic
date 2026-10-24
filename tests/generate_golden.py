"""Record the current behaviour as the golden values the tests compare against.

Run this only when a behaviour change is intended (e.g. new fuzzy rules or a SUMO upgrade),
and commit the updated files in tests/golden/ together with that change:

    pipenv run python tests/generate_golden.py
"""
import json
import os
import re
import subprocess

import behaviour


def write(path, text):
    os.makedirs(behaviour.GOLDEN_DIR, exist_ok=True)
    with open(path, "w") as golden:
        golden.write(text)
    print("wrote", os.path.relpath(path, behaviour.REPO_ROOT))


if __name__ == "__main__":
    # one line per queue_length_curr so a diff shows which inputs changed
    rows = ",\n".join("  " + json.dumps(row) for row in behaviour.fuzzy_outputs())
    write(behaviour.FUZZY_GOLDEN, (
        "{\n"
        f' "inputs": {json.dumps(behaviour.fuzzy_inputs_description())},\n'
        f' "green_times": [\n{rows}\n ]\n'
        "}\n"
    ))

    sumo = os.path.join(behaviour.sumo_home(), "bin", "sumo") if behaviour.sumo_home() else "sumo"
    version_output = subprocess.run([sumo, "--version"], capture_output=True, text=True).stdout
    write(behaviour.SIMULATION_GOLDEN, json.dumps({
        "sumo_version": re.search(r"^Eclipse SUMO sumo (?:Version )?(\S+)", version_output).group(1),
        "metrics": behaviour.simulation_metrics(),
    }, indent=1) + "\n")
