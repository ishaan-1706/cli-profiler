# cli_profiler\utils.py
import json
import rich
from rich.table import Table
from rich.console import Console

def output_summary(results, args):
    console = Console(color_system=None if args.no_color else "auto")

    if args.format == "table":
        # CPU table
        if "cpu" in results:
            tbl = Table(title="CPU Profile")
            for h in ["function","file","line","ncalls","tottime","cumtime"]:
                tbl.add_column(h, justify="right")
            for e in results["cpu"]:
                tbl.add_row(e["function"], e["file"], str(e["line"]),
                            str(e["ncalls"]), f"{e['tottime']:.4f}", f"{e['cumtime']:.4f}")
            console.print(tbl)
        # Memory table
        if "memory" in results:
            tbl = Table(title=f"Memory Profile (peak {results['memory']['peak_kb']:.1f} KiB)")
            for h in ["file","line","code","size_kb"]:
                tbl.add_column(h)
            for e in results["memory"]["snapshot"]:
                tbl.add_row(e["file"], str(e["line"]), e["code"], f"{e['size_kb']:.1f}")
            console.print(tbl)
        # Warnings
        if results["warnings"]:
            console.print("\n[bold yellow]Warnings:[/]\n" + "\n".join(results["warnings"]))

    elif args.format == "json":
        payload = results.copy()
        with open(args.output, "w") as f:
            json.dump(payload, f, indent=2)

    elif args.format == "markdown":
        # simple markdown export
        md = "# Profiling Report\n\n"
        md += f"- Runtime: {results['runtime']:.3f}s  \n"
        md += f"- CPU%: {results['cpu_percent']}%  \n\n"
        if "cpu" in results:
            md += "## CPU Top Functions\n\n| func | file | line | calls | tottime | cumtime |\n|---|---|---|---|---|---|\n"
            for e in results["cpu"]:
                md += f"| {e['function']} | {e['file']} | {e['line']} | {e['ncalls']} | {e['tottime']:.4f} | {e['cumtime']:.4f} |\n"
        if "memory" in results:
            md += f"\n## Memory Top Lines (peak {results['memory']['peak_kb']:.1f} KiB)\n\n| file | line | code | size_kb |\n|---|---|---|---|\n"
            for e in results["memory"]["snapshot"]:
                md += f"| {e['file']} | {e['line']} | `{e['code']}` | {e['size_kb']:.1f} |\n"
        if results["warnings"]:
            md += "\n## Warnings\n\n" + "\n".join(f"- {w}" for w in results["warnings"])
        with open(args.output, "w") as f:
            f.write(md)

    # Also write to file if output path given for table format
    if args.format == "table" and args.output:
        with open(args.output, "w") as f:
            f.write(console.export_text())
