"""
Command-line interface for nimmunize.
"""

import click
from .survey import load, audit, metrics, list_missed
from .catchup import plan as catchup_plan
from typing import Dict, List, Optional, Sequence, Any


@click.group()
def main():
    """nimmunize: schedule, survey, catchup CLI."""
    pass


@main.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option("--outfile", "-o", type=click.Path(), help="Save annotated CSV")
def survey_cmd(infile, outfile):
    df = load(infile)
    audited = audit(df)
    if outfile:
        audited.to_csv(outfile, index=False)
        click.echo(f"Annotated data written to {outfile}")
    else:
        click.echo(metrics(audited))


@main.command()
@click.argument("dob", type=str)
@click.option("--taken", "-t", multiple=True, nargs=2, help="Antigen DATE (YYYY-MM-DD)")
@click.option("--as-of", type=str, default=None, help="Reference date")
def nextdose(dob, taken, as_of):
    from datetime import datetime

    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
    taken_dict = {k.lower(): datetime.strptime(v, "%Y-%m-%d").date() for k, v in taken}
    nd = catchup_plan(
        dob_date,
        taken_dict,
        as_of=datetime.strptime(as_of, "%Y-%m-%d").date() if as_of else None,
    )
    click.echo(nd)
