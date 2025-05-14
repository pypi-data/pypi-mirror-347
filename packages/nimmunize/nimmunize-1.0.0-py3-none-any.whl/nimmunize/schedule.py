"""nimmunize.schedule
=====================
Schedule‑calculation engine for Nigeria’s routine immunisation calendar.
Reads the canonical JSON spec (``data/nphcda_schedule.json``) and exposes
three key helpers:

* ``next_due(dob, taken, *, as_of=None, include_details=False)`` – next dose
  per antigen; if *include_details* is **True** returns dosage, route, and
  diseases prevented alongside the due date.
* ``overdue(dob, taken, *, as_of=None)`` – flags missed series and computes
  delay in days.
* ``reference()`` – poster metadata (title, date, URLs, image).

Pure‑Python, no external deps, so it runs happily on low‑spec Android field
apps.
"""

from __future__ import annotations
import datetime as _dt, json, importlib.resources as pkg
from functools import lru_cache
from typing import Dict, List, Optional, Sequence, Any

# -------------------------------------------------------------------------
# JSON SPEC LOADING
# -------------------------------------------------------------------------
with pkg.files(__package__).joinpath("data/nphcda_schedule.json").open(
    "r", encoding="utf-8"
) as _f:
    _SPEC = json.load(_f)
ANTIGENS: List[str] = [a["name"].lower() for a in _SPEC.get("antigens", [])]


# -------------------------------------------------------------------------
# INTERNAL HELPERS
# -------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _doses(antigen: str) -> List[dict]:
    rec = next(a for a in _SPEC["antigens"] if a["name"].lower() == antigen.lower())
    return sorted(rec["doses"], key=lambda d: d.get("sequence", 0))


def _nominal_due(dob: _dt.date, dose: dict) -> _dt.date:
    return dob + _dt.timedelta(weeks=dose.get("age_weeks", 0))


def _earliest_allowed(dob: _dt.date, dose: dict, prev: Optional[_dt.date]):
    by_age = dob + _dt.timedelta(days=dose.get("min_age_days", 0))
    if prev is None:
        return by_age
    return max(by_age, prev + _dt.timedelta(days=dose.get("min_interval_days", 0)))


def _parse_taken(v: Any) -> Sequence[_dt.date]:
    if v is None:
        return []
    if isinstance(v, _dt.date):
        return [v]
    return list(v)


# -------------------------------------------------------------------------
# PUBLIC API
# -------------------------------------------------------------------------


def next_due(
    dob: _dt.date,
    taken: Dict[str, Any],
    *,
    as_of: Optional[_dt.date] = None,
    include_details: bool = False,
):
    """Return next dose per antigen.

    *Default* – ``{ag: date|None}``.
    With *include_details=True* – ``{ag: {due, sequence, dosage, route, diseases}}``.
    """
    as_of = as_of or _dt.date.today()
    out: Dict[str, Any] = {}
    for ag in ANTIGENS:
        doses = _doses(ag)
        shots = sorted(_parse_taken(taken.get(ag)), key=lambda d: d)
        given = {i + 1: d for i, d in enumerate(shots)}
        nxt = next((d for d in doses if d["sequence"] not in given), None)
        if nxt is None:
            out[ag] = None
            continue
        prev = given.get(nxt["sequence"] - 1)
        due = max(_nominal_due(dob, nxt), _earliest_allowed(dob, nxt, prev))
        if include_details:
            out[ag] = {
                "due": due,
                "sequence": nxt["sequence"],
                "dosage": nxt.get("dosage"),
                "route": nxt.get("route"),
                "diseases": nxt.get("diseases_prevented", []),
            }
        else:
            out[ag] = due
    return out


def overdue(dob: _dt.date, taken: Dict[str, Any], *, as_of: Optional[_dt.date] = None):
    as_of = as_of or _dt.date.today()
    res: Dict[str, Optional[int]] = {}
    for ag, val in next_due(dob, taken, as_of=as_of).items():
        if val is None:
            res[f"missed_{ag}"] = False
            res[f"delay_{ag}"] = None
            continue
        due: _dt.date = val
        res[f"missed_{ag}"] = as_of >= due
        res[f"delay_{ag}"] = (as_of - due).days if as_of >= due else None
    return res


def reference():
    return _SPEC.get("source", {})


if __name__ == "__main__":  # pragma: no cover
    dob = _dt.date(2024, 7, 15)
    print(next_due(dob, {"bcg": dob}, include_details=True))
