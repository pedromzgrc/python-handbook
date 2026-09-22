import time
from app import app

def run_benchmark():
    with app.test_client() as client:
        # Warmup
        for _ in range(50):
            client.get('/')

        start = time.perf_counter()
        for _ in range(500):
            client.get('/')
        end = time.perf_counter()
        print(f"500 requests to '/' took: {end - start:.4f} seconds")

        # unit detail
        start = time.perf_counter()
        for _ in range(500):
            client.get('/unit/basic-data-types')
        end = time.perf_counter()
        print(f"500 requests to '/unit/basic-data-types' took: {end - start:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
