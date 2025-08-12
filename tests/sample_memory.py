# tests/sample_memory.py

def allocate_list(n):
    # Allocate a list of zeros
    data = [0] * n
    return data

if __name__ == "__main__":
    # Trigger memory usage
    allocate_list(100000)
