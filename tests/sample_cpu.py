# tests/sample_cpu.py

def busy_loop(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == "__main__":
    # Trigger some work
    busy_loop(5000)
