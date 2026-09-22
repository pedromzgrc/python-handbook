import time
from content_loader import load_units

def benchmark():
    start = time.time()
    for _ in range(100):
        load_units()
    end = time.time()
    print(f"Time taken for 100 calls: {end - start:.4f} seconds")

if __name__ == '__main__':
    benchmark()
