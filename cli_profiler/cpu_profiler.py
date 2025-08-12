# cli_profiler/cpu_profiler.py

import os
import cProfile
import pstats
import runpy

class CPUProfiler:
    def __init__(self, script: str, sort_by: str, top_n: int):
        self.script  = script
        # allow "time" → "tottime"; otherwise accept "calls", "tottime", "cumtime"
        self.sort_by = "tottime" if sort_by == "time" else sort_by
        self.top_n   = top_n

    def run(self):
        # 1. Run the profiler on your script
        profiler = cProfile.Profile()
        profiler.enable()
        runpy.run_path(self.script, run_name="__main__")
        profiler.disable()

        # 2. Load stats and strip absolute paths down to basenames
        stats = pstats.Stats(profiler)
        stats.strip_dirs()

        # 3. Decide which column index to sort on
        #
        #    stats.stats[key] = (
        #       primitive_calls, total_calls, total_time, cumulative_time, callers
        #    )
        sort_indices = {"calls": 1, "tottime": 2, "cumtime": 3}
        idx = sort_indices.get(self.sort_by)
        if idx is None:
            raise ValueError(f"Unsupported sort key: {self.sort_by!r}")

        # 4. Filter out everything except functions defined in your script
        script_name = os.path.basename(self.script)
        raw_items = [
            (func_key, stat_tuple)
            for func_key, stat_tuple in stats.stats.items()  # type: ignore[attr-defined]
            if func_key[0] == script_name
        ]

        # 5. Sort by the chosen metric (descending) and take top_n
        sorted_items = sorted(
            raw_items,
            key=lambda kv: kv[1][idx],
            reverse=True
        )[: self.top_n]

        # 6. Build your output list
        entries = []
        for (filename, lineno, func_name), data in sorted_items:
            _, total_calls, total_time, cum_time, _ = data
            entries.append({
                "function": func_name,
                "file":     filename,
                "line":     lineno,
                "ncalls":   total_calls,
                "tottime":  total_time,
                "cumtime":  cum_time,
            })

        return entries
