import time
from interview_loader import load_categories

def run_benchmark():
    start = time.time()
    for _ in range(100):
        load_categories()
    end = time.time()
    print(f"100 iterations took {end - start:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
