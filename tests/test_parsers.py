# tests/test_parsers.py

import pytest
import tracemalloc
from pstats import Stats
from cli_profiler.parsers import parse_cpu, parse_memory
import io, cProfile

def make_dummy_stats():
    prof = cProfile.Profile()
    prof.enable()
    # Dummy workload
    for _ in range(10000):
        pass
    prof.disable()
    return Stats(prof)

def test_parse_cpu_default():
    stats = make_dummy_stats()
    parsed = parse_cpu(stats, top_n=5, sort_by="tottime")
    assert isinstance(parsed, list)
    assert all("function" in entry for entry in parsed)
    # Should include some internal functions like <module> or builtins
    assert parsed[0]["ncalls"] >= 1

def test_parse_memory(tmp_path):
    # Create a snapshot via tracemalloc
    tracemalloc.start()
    x = [0] * 1000
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()

    mem = parse_memory(snapshot, top_n=3, sort_by="size")
    assert "snapshot" in mem
    assert len(mem["snapshot"]) <= 3
    for entry in mem["snapshot"]:
        assert "file" in entry and "line" in entry and "size_kb" in entry
        assert entry["size_kb"] >= 0
