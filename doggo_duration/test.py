import pytest
from parse import parse

def test_parse():
    test_strs = [
        "3h15m",
        "1 hours and 1 minutes",
        "100:100",
        "12hours5min",
        "53:4m",
    ]

    expected = [
        195,
        61,
        6100,
        725,
        3184
    ]

    for t, e in zip(test_strs, expected):
        assert parse(t) == e

