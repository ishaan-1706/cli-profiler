import pytest

SAMPLE_CPU = """\
def busy_loop(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == "__main__":
    busy_loop(10)
"""

SAMPLE_MEMORY = """\
def allocate_list(n):
    data = [0] * n
    return data

if __name__ == "__main__":
    allocate_list(100000)
"""

@pytest.fixture
def sample_file(tmp_path):
    f = tmp_path / "sample_cpu.py"
    f.write_text(SAMPLE_CPU)
    return str(f)

@pytest.fixture
def sample_mem_file(tmp_path):
    f = tmp_path / "sample_memory.py"
    f.write_text(SAMPLE_MEMORY)
    return str(f)
