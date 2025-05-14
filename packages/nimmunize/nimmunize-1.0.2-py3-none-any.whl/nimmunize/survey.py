# nimmunize/survey.py

from __future__ import annotations
import pandas as pd
import datetime as _dt
from typing import Dict, List, Optional, Sequence, Any

from .schedule import ANTIGENS, next_due as _next_due, overdue as _overdue

# -----------------------------------------------------------------------------
# DATE PARSING
# -----------------------------------------------------------------------------
_DOB_FMT_HINTS = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m", "%m/%Y"]


def _parse_date(val: Any) -> Optional[_dt.date]:
    """Smart-parse full or partial dates; YYYY-MM becomes day=15."""
    if pd.isna(val) or val is None:
        return None
    if isinstance(val, (_dt.date, pd.Timestamp)):
        return val.date() if isinstance(val, pd.Timestamp) else val  # type: ignore
    s = str(val).strip()
    for fmt in _DOB_FMT_HINTS:
        try:
            dt = _dt.datetime.strptime(s, fmt)
            if fmt in ("%Y-%m", "%m/%Y"):
                dt = dt.replace(day=15)
            return dt.date()
        except ValueError:
            continue
    raise ValueError(f"Un-parsable date: {val}")


# -----------------------------------------------------------------------------
# LOAD & NORMALISE
# -----------------------------------------------------------------------------
def load(
    path_or_df: str | pd.DataFrame,
    *,
    dob_col: str = "dob",
    vacc_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Read a CSV / Excel / DataFrame and normalise:
      - Date of birth to datetime.date
      - Vaccination columns coerced to datetime.date or None
    Stores the final `vacc_cols` in df.attrs['vacc_cols'].
    """
    # load into DataFrame
    if isinstance(path_or_df, pd.DataFrame):
        df = path_or_df.copy()
    else:
        if str(path_or_df).lower().endswith((".xls", ".xlsx")):
            df = pd.read_excel(path_or_df)
        else:
            df = pd.read_csv(path_or_df)

    # parse DOB
    if dob_col not in df.columns:
        raise KeyError(f"Date-of-birth column '{dob_col}' not found")
    df[dob_col] = df[dob_col].apply(_parse_date)

    # infer vaccination columns
    cols = vacc_cols or [c for c in df.columns if c.lower() in ANTIGENS]
    df.attrs["vacc_cols"] = cols

    # parse each vaccination date column
    for col in cols:
        df[col] = df[col].apply(_parse_date)

    return df


# -----------------------------------------------------------------------------
# AUDIT ROWS
# -----------------------------------------------------------------------------
def audit(
    df: pd.DataFrame, *, dob_col: str = "dob", as_of: _dt.date | str | None = None
) -> pd.DataFrame:
    """
    Vectorised audit → adds:
      - missed_<antigen>: bool
      - delay_<antigen>: Optional[int]
      - next_due_<antigen>: Optional[date]
    Only for antigens in df.attrs['vacc_cols'].
    """
    # resolve as_of date
    if isinstance(as_of, str):
        as_of = _parse_date(as_of)
    as_of = as_of or _dt.date.today()

    cols: List[str] = df.attrs.get("vacc_cols", [])
    records: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        dob = row[dob_col]
        taken = {ag: row.get(ag) for ag in cols}

        od = _overdue(dob, taken, as_of=as_of)
        nd = _next_due(dob, taken, as_of=as_of)

        # filter to only loaded vaccines
        rec: Dict[str, Any] = {}
        for k, v in od.items():
            antigen = k.replace("missed_", "")
            if antigen in cols:
                rec[k] = v
        for ag, due in nd.items():
            if ag in cols:
                rec[f"next_due_{ag}"] = due

        records.append(rec)

    audited = pd.concat([df.reset_index(drop=True), pd.DataFrame(records)], axis=1)
    return audited


# -----------------------------------------------------------------------------
# SURVEY METRICS (updated)
# -----------------------------------------------------------------------------
def metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Standard national-survey-style indicators:
      - coverage_%: {antigen: % not missed}
      - FIC_%: % fully immunised on all loaded antigens
      - median_delay_days: {antigen: median delay (days) or None}
    """
    cols: List[str] = df.attrs.get("vacc_cols", [])
    # determine which missed columns actually exist
    miss_cols = [f"missed_{ag}" for ag in cols if f"missed_{ag}" in df.columns]

    # coverage per antigen
    coverage: Dict[str, float] = {}
    for ag in cols:
        col = f"missed_{ag}"
        if col in df.columns:
            coverage[ag] = 100.0 * (~df[col]).mean()

    # fully immunised (all antigens) coverage
    if miss_cols:
        fic = 100.0 * (~df[miss_cols].any(axis=1)).mean()
    else:
        fic = 0.0

    # median delay per antigen
    delays: Dict[str, Optional[float]] = {}
    for ag in cols:
        delay_col = f"delay_{ag}"
        if delay_col in df.columns:
            non_null = df[delay_col].dropna()
            delays[ag] = float(non_null.median()) if not non_null.empty else None
        else:
            delays[ag] = None

    return {"coverage_%": coverage, "FIC_%": fic, "median_delay_days": delays}


# -----------------------------------------------------------------------------
# FILTERED ROWSETS
# -----------------------------------------------------------------------------
def list_missed(df: pd.DataFrame, antigen: Optional[str] = None) -> pd.DataFrame:
    """
    Return sub-DataFrame of children with any missed dose (or only a specific antigen).
    Dynamically detects all 'missed_*' columns in the audited DataFrame.
    """
    miss_cols = [col for col in df.columns if col.startswith("missed_")]
    if antigen:
        col = f"missed_{antigen}"
        miss_cols = [col] if col in df.columns else []
    if not miss_cols:
        return df.iloc[0:0]
    mask = pd.concat([df[c] for c in miss_cols], axis=1).any(axis=1)
    return df.loc[mask]


def list_complete(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return sub-DataFrame of children with no missed doses across all antigens loaded.
    Dynamically detects all 'missed_*' columns.
    """
    miss_cols = [col for col in df.columns if col.startswith("missed_")]
    if not miss_cols:
        return df.iloc[0:0]
    mask = ~pd.concat([df[c] for c in miss_cols], axis=1).any(axis=1)
    return df.loc[mask]


# -----------------------------------------------------------------------------
# COVERAGE BY ROUTE & DISEASE
# -----------------------------------------------------------------------------
# These maps are derived at import from schedule JSON
from .schedule import _SPEC as _SCH_SPEC

# build antigen → route lookup
_antigen_route: Dict[str, str] = {
    a["name"]: a["doses"][0].get("route", "unknown") for a in _SCH_SPEC["antigens"]
}

# build disease → antigens lookup
_disease_to_antigens: Dict[str, List[str]] = {}
for a in _SCH_SPEC["antigens"]:
    for dose in a["doses"]:
        for dis in dose.get("diseases_prevented", []):
            _disease_to_antigens.setdefault(dis, []).append(a["name"])


def route_coverage(df: pd.DataFrame) -> Dict[str, float]:
    """
    Percentage of children fully covered for antigens delivered by each route.
    """
    cols: List[str] = df.attrs.get("vacc_cols", [])
    # group series by route
    route_map: Dict[str, List[pd.Series]] = {}
    for ag in cols:
        route = _antigen_route.get(ag, "unknown")
        route_map.setdefault(route, []).append(~df[f"missed_{ag}"])

    return {
        route: 100 * pd.concat(series, axis=1).all(axis=1).mean()
        for route, series in route_map.items()
    }


def disease_coverage(df: pd.DataFrame) -> Dict[str, float]:
    """
    Percentage of children protected against each disease.
    (i.e., at least one complete antigen series that prevents that disease).
    """
    cols: List[str] = df.attrs.get("vacc_cols", [])
    miss_map = {ag: df[f"missed_{ag}"] for ag in cols}

    dis_cov: Dict[str, float] = {}
    for disease, ag_list in _disease_to_antigens.items():
        relevant = [~miss_map[ag] for ag in ag_list if ag in miss_map]
        if relevant:
            dis_cov[disease] = 100 * pd.concat(relevant, axis=1).any(axis=1).mean()
    return dis_cov


def diseases_at_risk(df: pd.DataFrame, *, threshold: float = 80.0) -> List[str]:
    """
    List diseases whose population protection is below *threshold* percent.
    """
    return [d for d, pct in disease_coverage(df).items() if pct < threshold]
