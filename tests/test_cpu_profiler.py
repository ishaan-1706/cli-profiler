import pytest
from cli_profiler.cpu_profiler import CPUProfiler

def test_cpu_profiler_runs(sample_file):
    profiler = CPUProfiler(sample_file, sort_by="tottime", top_n=3)
    entries = profiler.run()

    assert isinstance(entries, list)
    # Should report busy_loop
    funcs = [e["function"] for e in entries]
    assert "busy_loop" in funcs

    for e in entries:
        assert isinstance(e["ncalls"], int)
        assert e["tottime"] >= 0
