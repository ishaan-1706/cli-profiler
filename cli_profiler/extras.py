# cli_profiler\extras.py
import time, psutil

class Extras:
    def __init__(self, script):
        self.script = script

    def measure_runtime(self):
        start = time.perf_counter()
        __import__("runpy").run_path(self.script, run_name="__main__")
        return time.perf_counter() - start

    def measure_cpu_percent(self):
        p = psutil.Process()
        return p.cpu_percent(interval=None)

    def generate_warnings(self, results):
        warns = []
        # CPU: many calls but low time
        for fn in results.get("cpu", []):
            if fn["ncalls"] > 10000 and fn["tottime"] < 0.01:
                warns.append(f"Function {fn['function']} called {fn['ncalls']} times—consider caching.")
        # Memory: large single allocation
        for mem in results.get("memory", {}).get("snapshot", []):
            if mem["size_kb"] > 1024:
                warns.append(f"High memory usage ({mem['size_kb']:.1f} KiB) at {mem['file']}:{mem['line']}.")
        return warns
