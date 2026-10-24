import itertools

import behaviour


def test_green_times_match_golden_values():
    golden = behaviour.load(behaviour.FUZZY_GOLDEN)
    assert golden["inputs"] == behaviour.fuzzy_inputs_description()

    inputs = list(itertools.product(
        behaviour.FUZZY_QUEUE_LENGTHS_CURR, behaviour.FUZZY_QUEUE_LENGTHS_OTHER, behaviour.FUZZY_MAX_WAITING_TIMES
    ))
    expected = itertools.chain.from_iterable(golden["green_times"])
    actual = itertools.chain.from_iterable(behaviour.fuzzy_outputs())
    changed = [(i, e, a) for i, e, a in zip(inputs, expected, actual) if e != a]

    assert not changed, (
        f"{len(changed)} of {len(inputs)} green times changed, first ones "
        f"((queue_length_curr, queue_length_other, max_waiting_time), expected, actual): {changed[:10]}"
    )
