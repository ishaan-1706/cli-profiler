from setuptools import setup, find_packages

setup(
    name="cli_profiler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "line_profiler",
        "memory_profiler",
        "psutil",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "cli_profiler=cli_profiler.cli:main",
        ],
    },
)
