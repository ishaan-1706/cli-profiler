# tests/test_cli.py

import subprocess
import sys
import os
import pytest

CLI = [sys.executable, "-m", "cli_profiler.cli"]

def test_cli_help():
    res = subprocess.run(CLI + ["--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Lightweight Python profiler" in res.stdout

def test_cli_cpu_mode(tmp_path):
    script = tmp_path / "sample.py"
    script.write_text("def f():\n    pass\n\nif __name__=='__main__':\n    f()")
    res = subprocess.run(CLI + [str(script), "--cpu", "--sort-cpu=calls", "--top=1"],
                         capture_output=True, text=True)
    assert res.returncode == 0
    assert "function" in res.stdout.lower()

def test_cli_memory_mode(tmp_path):
    script = tmp_path / "sample2.py"
    script.write_text("def g():\n    x=[0]*10000\n\nif __name__=='__main__':\n    g()")
    res = subprocess.run(CLI + [str(script), "--memory", "--sort-mem=size", "--top=1"],
                         capture_output=True, text=True)
    assert res.returncode == 0
    assert "snapshot" not in res.stdout.lower()  # raw console should show table, not literal dict
