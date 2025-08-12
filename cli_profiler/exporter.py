# cli_profiler/exporter.py

import json
from rich.table import Table
from itertools import zip_longest

def to_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def to_markdown(table: Table, filepath: str):
    headers = [str(col.header) for col in table.columns]
    # materialize cells into true lists so len() and zip_longest work without type complaints
    columns_cells = [list(col.cells) for col in table.columns]

    with open(filepath, "w", encoding="utf-8") as f:
        # header row
        f.write("| " + " | ".join(headers) + " |\n")
        # separator row
        f.write("| " + " | ".join("---" for _ in headers) + " |\n")
        # data rows via zip_longest — no need to compute row_count manually
        for row in zip_longest(*columns_cells, fillvalue=""):
            f.write("| " + " | ".join(str(cell) for cell in row) + " |\n")
