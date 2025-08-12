# tests/test_formatters.py

from cli_profiler.formatters import make_table, display
from rich.table import Table
import pytest

def test_make_table_and_display(capsys):
    columns = ["Name", "Value"]
    rows = [{"name": "foo", "value": 123}, {"name": "bar", "value": 456}]
    table: Table = make_table("Test", columns, rows)
    assert isinstance(table, Table)
    assert table.row_count == 2

    # Test display does not error
    display(table)
    captured = capsys.readouterr()
    assert "foo" in captured.out
    assert "123" in captured.out
