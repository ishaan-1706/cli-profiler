import pytest
from cli_profiler.memory_profiler import MemoryProfiler

def test_memory_profiler_runs(sample_mem_file):
    profiler = MemoryProfiler(sample_mem_file, sort_by="size", top_n=3)
    result = profiler.run()

    assert "snapshot" in result
    assert isinstance(result["snapshot"], list)
    assert all("size_kb" in entry for entry in result["snapshot"])
