# TPC-C Web Server

A webserver based on the [TPC-C database benchmark](https://www.tpc.org/tpcc/default5.asp). It consists of 5 transaction
types interacting with a complex database mimicking a real-life use case.

The webserver provided routes are:

| Path                      | Body                              |
|---------------------------|-----------------------------------|
| /transaction/new_order    | `{ "w_id": 1, "c_id": 1 }`        |
| /transaction/payment      | `{ "w_id": 1, "c_id": 1 }`        |
| /transaction/order_status | `{ "c_id": 1 }`                   |
| /transaction/delivery     | `{ "w_id": 1 }`                   |
| /transaction/stock_level  | `{ "w_id": 1 }`                   |
| /init_db                  | `{ "warehouses": 10 }` _Optional_ |

Notes:

1. All routes are `POST` requests
2. `w_id` is the warehouse id, `c_id` is the customer id

## Acknowledgements

The TPC-C code is based on [Python ORM Benchmark](https://github.com/DominovTut/Python_ORM_Benchmark/).