# fuzzy-traffic

Fuzzy-logic traffic light control for a four-way junction, simulated with [SUMO](https://eclipse.dev/sumo/).

At the start of each green phase, the fuzzy controller picks a green time from:

- the queue length on the approach that is about to get green,
- the total queue length on the other approaches,
- the longest waiting time of a vehicle on that approach.

The simulation compares it with a fixed-time controller that gives every approach 40 s of green.

## Requirements

- Python 3.15 and [pipenv](https://pipenv.pypa.io/)
- SUMO. Either install it from the [SUMO downloads](https://sumo.dlr.de/docs/Downloads.php) and put `sumo` on your `PATH` (or set `SUMO_HOME`), or run `pipenv run pip install eclipse-sumo`.

## Running

```sh
pipenv install
pipenv run python simulation.py            # both controllers
pipenv run python simulation.py dynamic    # only the fuzzy controller
```

Each run simulates the first 1000 s of the traffic in `junction.rou.xml` and prints the number of vehicles that completed their trip, the average waiting time per vehicle, and the total CO2 emission and fuel consumption. SUMO's per-vehicle results are written to `tripinfo_static.xml` and `tripinfo_dynamic.xml`.

## Files

| File | Contents |
|---|---|
| `simulation.py` | Runs the fixed-time and fuzzy controllers in SUMO and prints the results |
| `fuzzyRules.py` | Fuzzy membership functions and the rule table for the green time |
| `junction.*.xml`, `junction.sumocfg` | SUMO network, traffic demand, GUI settings and configuration |

To plot the membership functions or a controller output, install matplotlib (`pipenv run pip install matplotlib`) and call `.view()` on the variables in `fuzzyRules.py`.

## License

[MIT](LICENSE)
