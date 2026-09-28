from efficiency_validator.reproducibility import stable_json_digest


def test_stable_json_digest_ignores_mapping_order_but_not_values() -> None:
    first = stable_json_digest({"b": 2, "a": [1, 2]})
    reordered = stable_json_digest({"a": [1, 2], "b": 2})
    changed = stable_json_digest({"a": [1, 3], "b": 2})

    assert first == reordered
    assert first != changed
