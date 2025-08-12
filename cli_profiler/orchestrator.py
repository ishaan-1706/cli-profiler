# profiler_cli/orchestrator.py

import runpy
import cProfile
import tracemalloc
import pstats
import sys

class DynamicStats(pstats.Stats):
    """
    A Stats subclass whose .stream always reflects the current sys.stdout,
    and which swallows any initial assignment to stream in __init__.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def stream(self):
        # Always print to whatever sys.stdout is at call time.
        return sys.stdout

    @stream.setter
    def stream(self, value):
        # Ignore any attempts to set .stream (e.g. in base __init__).
        pass

def profile_once(script_path: str):
    #Run the target script once, collecting both CPU stats and a tracemalloc snapshot.
    #Returns a DynamicStats object and a Snapshot object.
    profiler = cProfile.Profile()
    tracemalloc.start()

    try:
        profiler.enable()
        runpy.run_path(script_path, run_name="__main__")
    finally:
        profiler.disable()
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

    # Wrap in DynamicStats so print_stats respects redirect_stdout()
    stats = DynamicStats(profiler).strip_dirs()
    return stats, snapshot

def safe_profile(script_path: str):
    # Wrap profile_once with error handling.
    try:
        return profile_once(script_path)
    except Exception as e:
        raise RuntimeError(f"Profiling failed for {script_path}: {e}") from e
