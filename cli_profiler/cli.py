#cli_profiler\cli.py
import argparse
import os
from .cpu_profiler import CPUProfiler
from .memory_profiler import MemoryProfiler
from .extras import Extras
from .utils import output_summary

def main():
    parser = argparse.ArgumentParser(description="Lightweight Python profiler")
    parser.add_argument("script", help="Path to target Python script")
    parser.add_argument("--cpu", action="store_true", help="Enable CPU profiling")
    parser.add_argument("--memory", action="store_true", help="Enable memory profiling")
    parser.add_argument("--sort-cpu", choices=["time", "cumulative", "calls"], default="time")
    parser.add_argument("--sort-mem", choices=["size", "line"], default="size")
    parser.add_argument("--top", type=int, default=10, help="Number of top entries to show")
    parser.add_argument("--format", choices=["table", "json", "markdown"], default="table")
    parser.add_argument("--output", "-o", help="Write summary to file (auto-format by extension)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()

    if not os.path.isfile(args.script):
        parser.error(f"Script not found: {args.script}")

    results = {}
    extras = Extras(args.script)
    results["runtime"] = extras.measure_runtime()
    results["cpu_percent"] = extras.measure_cpu_percent()

    if args.cpu:
        cpu = CPUProfiler(args.script, args.sort_cpu, args.top)
        results["cpu"] = cpu.run()

    if args.memory:
        mem = MemoryProfiler(args.script, args.sort_mem, args.top)
        results["memory"] = mem.run()

    # Generate warnings
    results["warnings"] = extras.generate_warnings(results)

    # Output to console and/or file
    output_summary(results, args)

if __name__ == "__main__":
    main()
