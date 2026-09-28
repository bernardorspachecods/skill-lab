from efficiency_validator.process_tree import (
    descendant_pids,
    parse_process_names,
    parse_process_table,
)


def test_process_table_finds_all_descendants_without_host_noise() -> None:
    table = parse_process_table(
        [
            "100 1",
            "101 100",
            "102 101",
            "103 100",
            "200 1",
        ]
    )

    assert descendant_pids(table, 100) == {100, 101, 102, 103}


def test_process_table_ignores_malformed_rows() -> None:
    table = parse_process_table(["100 1", "not-a-row", "101 nope", "102 100"])

    assert descendant_pids(table, 100) == {100, 102}


def test_process_table_preserves_names_for_fs_usage_correlation() -> None:
    lines = ["100 1 zsh", "101 100 codex", "102 101 python3"]

    assert parse_process_names(lines) == {100: "zsh", 101: "codex", 102: "python3"}
