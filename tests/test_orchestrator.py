# tests/test_orchestrator.py

import pytest
import tracemalloc
from pstats import Stats
from cli_profiler.orchestrator import profile_once, safe_profile

def test_profile_once_returns_stats_and_snapshot(sample_file):
    stats, snapshot = profile_once(sample_file)

    assert isinstance(stats, Stats)
    assert isinstance(snapshot, tracemalloc.Snapshot)

    # Ensure 'busy_loop' appears in the printed stats output
    from io import StringIO
    from contextlib import redirect_stdout

    buf = StringIO()
    # Capture print_stats() output
    with redirect_stdout(buf):
        stats.print_stats()
    output = buf.getvalue()
    assert "busy_loop" in output
    assert "busy_loop" in output

def test_safe_profile_on_bad_script(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("def foo(:\n    pass")  # syntax error
    with pytest.raises(RuntimeError) as excinfo:
        safe_profile(str(bad))
    assert "Profiling failed" in str(excinfo.value)
