import pytest

import behaviour


@pytest.mark.skipif(not behaviour.sumo_available(), reason="SUMO is not installed")
def test_simulation_results_match_golden_values():
    golden = behaviour.load(behaviour.SIMULATION_GOLDEN)

    assert behaviour.simulation_metrics() == golden["metrics"], (
        f"results differ from the values recorded with SUMO {golden['sumo_version']}"
    )
