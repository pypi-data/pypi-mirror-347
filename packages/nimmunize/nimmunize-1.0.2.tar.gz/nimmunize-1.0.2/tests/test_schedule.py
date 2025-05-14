import datetime as _dt
import pytest
from nimmunize.schedule import next_due, overdue, reference


def test_reference_contains_source():
    src = reference()
    assert "title" in src and "url" in src and "published" in src


@pytest.mark.parametrize(
    "dob, taken, expected_next",
    [
        (_dt.date(2024, 1, 1), {}, {"bcg": _dt.date(2024, 1, 1)}),
        (_dt.date(2024, 1, 1), {"bcg": _dt.date(2024, 1, 1)}, {"bcg": None}),
    ],
)
def test_next_due_simple(dob, taken, expected_next):
    result = next_due(dob, taken)
    assert result["bcg"] == expected_next["bcg"]


def test_overdue_flag_and_delay():
    dob = _dt.date(2024, 1, 1)
    # BCG due at birth, no shot, so overdue with delay = days since
    today = _dt.date(2024, 1, 10)
    od = overdue(dob, {}, as_of=today)
    assert od["missed_bcg"] is True
    assert od["delay_bcg"] == 9
