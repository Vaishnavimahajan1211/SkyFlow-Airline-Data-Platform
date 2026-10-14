
"""
Unit tests for SkyFlow data quality checks.
"""

import pandas as pd

from python.quality.data_quality_checks import check


def test_check_passes_for_true_condition(capsys):
    check(True, "Test condition")

    output = capsys.readouterr().out

    assert "PASS" in output
    assert "Test condition" in output


def test_check_fails_for_false_condition(capsys):
    check(False, "Test condition")

    output = capsys.readouterr().out

    assert "FAIL" in output
    assert "Test condition" in output


def test_check_tracks_passed_and_failed_counts():
    import python.quality.data_quality_checks as quality

    initial_passed = quality.passed_checks
    initial_failed = quality.failed_checks

    try:
        quality.check(True, "Passing test")
        quality.check(False, "Failing test")

        assert quality.passed_checks == initial_passed + 1
        assert quality.failed_checks == initial_failed + 1
    finally:
        # Restore module state so other tests remain independent.
        quality.passed_checks = initial_passed
        quality.failed_checks = initial_failed
        quality.total_checks -= 2
        quality.check_results = quality.check_results[:-2]


def test_check_records_result_details():
    import python.quality.data_quality_checks as quality

    initial_length = len(quality.check_results)
    initial_total = quality.total_checks
    initial_passed = quality.passed_checks

    try:
        quality.check(False, "Missing value detected")

        result = quality.check_results[-1]

        assert result["check_name"] == "Missing value detected"
        assert result["status"] == "FAIL"
        assert result["details"] == "Missing value detected"
        assert result["check_number"] == initial_total + 1
    finally:
        quality.check_results = quality.check_results[:initial_length]
        quality.total_checks = initial_total
        quality.passed_checks = initial_passed
        quality.failed_checks -= 1

