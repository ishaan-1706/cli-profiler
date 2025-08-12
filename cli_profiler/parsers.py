# cli_profiler/parsers.py

import linecache
import tracemalloc
from pstats import Stats
from typing import Any, List, Dict

def parse_cpu(stats: Stats, top_n: int, sort_by: str) -> List[Dict]:
    """
    Turn a pstats.Stats object into a list of dicts:
      - function: function name
      - file:     filename
      - line:     lineno
      - ncalls:   number of calls
      - tottime:  total time in the function
      - cumtime:  cumulative time including subcalls
    """
    stats.sort_stats(sort_by)

    # Work around Pylance not knowing about Stats.stats
    raw_stats: Dict[Any, Any] = getattr(stats, "stats", {})

    parsed = []
    for idx, ((file, line, func), (cc, nc, tt, ct, callers)) in enumerate(raw_stats.items()):
        if idx >= top_n:
            break
        parsed.append({
            "function": func,
            "file": file,
            "line": line,
            "ncalls": nc,
            "tottime": tt,
            "cumtime": ct,
        })
    return parsed

def parse_memory(snapshot: tracemalloc.Snapshot, top_n: int, sort_by: str) -> Dict:
    stats = snapshot.statistics("lineno")

    if sort_by == "line":
        stats.sort(key=lambda s: s.traceback[0].lineno)
    else:  # sort_by == "size"
        stats.sort(key=lambda s: s.size, reverse=True)

    entries = []
    for stat in stats[:top_n]:
        frame = stat.traceback[0]
        filename = frame.filename
        lineno = frame.lineno
        code_line = linecache.getline(filename, lineno).strip()

        entries.append({
            "file": filename,
            "line": lineno,
            "code": code_line,
            "size_kb": stat.size / 1024,
        })

    return {"snapshot": entries}
