"""
Catch‑up planner: rebuild safe schedule for children with missing immunisations.
Implements WHO catch‑up algorithm for routine vaccines.
"""

from __future__ import annotations
import datetime as _dt
from typing import Dict, List, Optional, Sequence

from .schedule import ANTIGENS, _doses, _nominal_due, _earliest_allowed


def plan(
    dob: _dt.date,
    taken: Dict[str, _dt.date | Sequence[_dt.date] | None],
    *,
    as_of: Optional[_dt.date] = None,
) -> Dict[str, List[_dt.date]]:
    """
    For each antigen, return the full list of scheduled dates (catch-up)
    following WHO rules, ignoring any doses already recorded in *taken*.
    """
    as_of = as_of or _dt.date.today()
    result: Dict[str, List[_dt.date]] = {}

    for antigen in ANTIGENS:
        doses_defs = _doses(antigen)
        # flatten taken dates
        recorded = sorted(
            (d if isinstance(d, _dt.date) else list(d))
            if taken.get(antigen) is not None
            else []
        )
        rec_iter = iter(recorded)
        prev_date: Optional[_dt.date] = None
        this_plan: List[_dt.date] = []

        for dose_def in doses_defs:
            # skip any recorded dose
            next_recorded = None
            try:
                next_recorded = next(rec_iter)
            except StopIteration:
                pass

            if next_recorded:
                # consume recorded and set prev_date
                prev_date = next_recorded
                continue

            # compute nominal and earliest
            nominal = _nominal_due(dob, dose_def)
            earliest = _earliest_allowed(dob, dose_def, prev_date)
            due = max(nominal, earliest)
            if due > as_of:
                # still include future doses in the plan
                this_plan.append(due)
                prev_date = due
            else:
                this_plan.append(due)
                prev_date = due

        result[antigen] = this_plan

    return result
