# tests/test_exporter.py

import json
import os
import pytest
from cli_profiler.exporter import to_json, to_markdown
from rich.table import Table

def test_to_json(tmp_path):
    data = {"key": "value", "num": 42}
    f = tmp_path / "out.json"
    to_json(data, str(f))
    assert f.exists()
    loaded = json.loads(f.read_text())
    assert loaded == data

def test_to_markdown(tmp_path):
    # Create a dummy Rich table
    table = Table(title="MD")
    table.add_column("A")
    table.add_column("B")
    table.add_row("x", "y")
    out = tmp_path / "report.md"
    to_markdown(table, str(out))
    assert out.exists()
    content = out.read_text()
    assert "| A | B |" in content  # markdown header row
    assert "| x | y |" in content
