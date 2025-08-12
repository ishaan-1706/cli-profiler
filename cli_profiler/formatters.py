# cli_profiler\formatters.py

from rich.table import Table
from rich.console import Console

def make_table(title: str, columns: list[str], rows: list[dict]):
    table = Table(title=title)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(row[col.lower()]) for col in columns])
    return table

def display(table):
    Console().print(table)
