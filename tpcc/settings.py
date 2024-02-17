import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/bench_sa")
AMOUNT_OF_WAREHOUSES = int(os.environ.get("AMOUNT_OF_WAREHOUSES", 10))
