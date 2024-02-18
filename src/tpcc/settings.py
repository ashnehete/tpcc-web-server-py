import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/bench_sa")
WAREHOUSES = int(os.environ.get("WAREHOUSES", 10))
