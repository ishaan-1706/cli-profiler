# cli_profiler\memory_profiler.py
import tracemalloc
import runpy
import linecache

class MemoryProfiler:
    def __init__(self, script, sort_by, top_n):
        self.script = script
        self.sort_by = sort_by
        self.top_n = top_n

    def run(self):
        tracemalloc.start()
        runpy.run_path(self.script, run_name="__main__")
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        stats = snapshot.statistics("lineno")
        if self.sort_by == "line":
            stats.sort(key=lambda s: s.traceback[0].lineno)
        else:
            stats.sort(key=lambda s: s.size, reverse=True)

        entries = []
        for stat in stats[: self.top_n]:
            frame = stat.traceback[0]
            code = linecache.getline(frame.filename, frame.lineno).strip()
            entries.append({
                "file": frame.filename,
                "line": frame.lineno,
                "code": code,
                "size_kb": stat.size / 1024,
            })
        # add peak memory
        peak = tracemalloc.get_traced_memory()[1] / 1024
        return {"snapshot": entries, "peak_kb": peak}
