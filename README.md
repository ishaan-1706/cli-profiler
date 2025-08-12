# CLI-profiler

A zero-config command-line toolkit for profiling Python scripts  
with CPU and memory insights, exportable to Markdown or JSON.

## Table of Contents

- [Requirements](#requirements)  
- [Installation](#installation)  
- [Quickstart](#quickstart)  
- [CLI Options](#cli-options)  
- [Examples](#examples)  
- [Development](#development)  
- [Project Layout](#project-layout)  
- [Contributing](#contributing)  
- [License](#license)  

## Requirements

- Python 3.8 or newer  
- cProfile (built-in)  
- tracemalloc (built-in)  
- line_profiler==3.6.0  
- memory_profiler==0.64.0  
- psutil==5.9.5  
- rich==13.5.2  

Dev dependencies (optional):

- pytest==8.4.1  
- flake8==6.0.0  
- mypy==1.8.0  
- black==23.9.1  

## Installation

1. Create and activate a virtualenv:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # or `.venv\Scripts\activate` on Windows
   ```

2. Install runtime dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install dev/test tools:

   ```bash
   pip install -r dev-requirements.txt
   ```

## Quickstart

Run a CPU profile, sort by total time, show top 10, export Markdown:

```bash
cli-profiler my_script.py --cpu --sort-cpu=tottime --top=10 --out report.md
```

Capture both CPU and memory, sort memory by cumulative size, export JSON:

```bash
cli-profiler my_script.py --cpu --mem --sort-mem=cum --top=5 --out stats.json
```

---

## CLI Options

- `script.py`        : target script to profile  
- `--cpu`            : enable CPU profiling  
- `--mem`            : enable memory profiling  
- `--sort-cpu=KEY`   : sort CPU stats by `calls`, `tottime`, or `cumtime`  
- `--sort-mem=KEY`   : sort memory stats by `size` or `cum`  
- `--top=N`          : limit output to top N entries  
- `--out PATH`       : write results to file (`.md` or `.json`)  

---

## Examples

```bash
# Top 5 functions by call count in Markdown
cli-profiler example.py --cpu --sort-cpu=calls --top=5 --out hot.md

# JSON report with CPU and memory stats
cli-profiler example.py --cpu --mem --top=3 --out stats.json
```

---

## Development

Install dev tools, then run tests and linters:

```bash
pip install .[dev]
pytest -q
flake8 cli_profiler tests
mypy cli_profiler
black --check .
```

Set up a pre-commit hook to enforce style and type checks:

```bash
pre-commit install
```

---

## Project Layout

```bash
cli_profiler/        - core package  
tests/               - pytest test suite  
requirements.txt     - runtime dependencies  
dev-requirements.txt - developer dependencies
setup.py             - build/install configuration  
README.md            - project overview  
```

---

## Contributing

1. Fork the repository and create a feature branch  
2. Write tests under `tests/` to cover your change  
3. Implement in `cli_profiler/`  
4. Ensure all tests pass and linters are happy  
5. Open a pull request against `main`  

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.