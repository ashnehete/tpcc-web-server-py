# TPC-C Web Server

A webserver based on the [TPC-C database benchmark](https://www.tpc.org/tpcc/default5.asp). It consists of 5 transaction
types interacting with a complex database mimicking a real-life use case.

The webserver provided routes are:

| Path                                  | Method | Body                                                            |
|---------------------------------------|--------|-----------------------------------------------------------------|
| /init_db    	                         | POST   | `{ "warehouses": 10 }`<br>_Optional. Defaults to WAREHOUSES._ 	 |
| /orders/                              | POST   | `{ "w_id": 1, "c_id": 1 }`                                      |
| /payment/                             | POST   | `{ "w_id": 1, "c_id": 1 }`                                      |
| /customers/{customer_id}/orders       | POST   |                                                                 |
| /warehouses/{warehouse_id}/deliveries | POST   |                                                                 |
| /warehouses/{warehouse_id}/stock      | GET    |                                                                 |

Notes:

1. All routes are `POST` requests
2. `w_id` is the warehouse id, `c_id` is the customer id

## How to run

### Docker - SQLite

```shell
docker compose -f deploy/sqlite.compose.yml up -d
```

### Docker - Postgres
```shell
docker compose -f deploy/postgres.compose.yml up -d
```
This builds and starts the webserver along with a single Postgres database. Please
check [deploy/postgres.compose.yml](deploy/postgres.compose.yml) for configuration details such as username, password,
db name for postgres and gunicorn config for server.

### Local

```shell
# Init
python -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set `DATABASE_URL` and `WAREHOUSES` environment variable as required.
export DATABASE_URL=postgresql://localhost/bench_sa
export WAREHOUSES=10 # Default: 10 

# Run
cd src/ && gunicorn --bind=localhost:5000 app:app
```

## Init Database

Initialise database with all tables according to TPC-C schema and fill up with seed data for warehouses, districts,
customers, etc.

```shell
curl --request POST http://localhost:5000/init_db
```

Optionally, you can also pass the amount of warehouses,

```shell
curl --request POST 'http://localhost:5000/init_db' \
    --header 'Content-Type: application/json' \
    --data '{
        "warehouses": 20
    }'
```

## LiteFS

```shell
./litefs/run.sh up # Docker up all
./litefs/run.sh down # Docker down all

# For more info
./litefs/run.sh help
```

## Run Benchmark

```shell
# Run benchmark for 30 minutes
# Application located at http://localhost
# Output location: results/test
python benchmark.py -u http://localhost -d 1800 -o "results/test" &

# For more info
python benchmark.py --help
```

## Experiment

**Duration:** 30 minutes

**Virtual Users:** 2

5 Cloudlab instances with following specifications:

|       |                                                                |
|-------|----------------------------------------------------------------|
| CPU   | 2 x Xeon E5-2660 v3 processors (10 cores each, 2.6Ghz or more) |
| RAM   | 256GB Memory (16 x 16GB DDR4 DIMMs)                            |
| Disks | 1 x 900GB 10K SAS Drive                                        |
| NIC   | 1GbE Quad port embedded NIC (Intel)                            |
| NIC   | 1 x Solarflare Dual port SFC9120 10G Ethernet NIC              |

Each node had the following processes running:

| **Node** | **Process**      |
|----------|------------------|
| 0        | nginx            |
| 1        | primary          |
| 2        | replica          |
| 3        | replica          |
| 4        | benchmark client |

### Results

| Experiment           | MQTh    |
|----------------------|---------|
| xdn_rsync            | 29.8528 |
| cloudlab_sqlite_1800 | 27.5611 |
| kubernetes           | 22.0144 |
| postgres_1800        | 14.435  |
| no_nginx_1800        | 13.8778 |
| cloudlab_1800        | 11.2811 |
| xdn_fuselog          | 7.9711  |

## Acknowledgements

TPC-C code is based on [Python ORM Benchmark](https://github.com/DominovTut/Python_ORM_Benchmark/).