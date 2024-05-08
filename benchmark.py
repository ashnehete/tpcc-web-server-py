import json
import time
from datetime import datetime
from multiprocessing import Value, Process
from random import randint

import requests

BASE_URL = 'http://127.0.0.1:8080'
WAREHOUSES = 10
DURATION = 5

import logging

# Configure the logger
logging.basicConfig(
    filename="benchmark.log",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    filemode='w',
)
logger = logging.getLogger(__name__)


def virtual_user(pid: int, count_orders: Value, run: Value):
    transaction_log = []
    while run.value:
        choice = randint(1, 100)
        if choice <= 45:
            # new_order
            transaction = {
                'method': 'POST',
                'url': BASE_URL + '/orders',
                'json': {'w_id': randint(1, WAREHOUSES), 'c_id': randint(1, WAREHOUSES * 10)}
            }
            with count_orders.get_lock():
                count_orders.value += 1
        elif choice <= 88:
            # payment
            transaction = {
                'method': 'POST',
                'url': BASE_URL + '/payment',
                'json': {'w_id': randint(1, WAREHOUSES), 'c_id': randint(1, WAREHOUSES * 10)},
            }
        elif choice <= 92:
            # order_status
            transaction = {
                'method': 'GET',
                'url': BASE_URL + f'/customers/{randint(1, WAREHOUSES * 10)}/orders',
            }
        elif choice <= 96:
            # delivery
            transaction = {
                'method': 'POST',
                'url': BASE_URL + f'/warehouses/{randint(1, WAREHOUSES)}/deliveries',
            }
        else:
            # stock_level
            transaction = {
                'method': 'GET',
                'url': BASE_URL + f'/warehouses/{randint(1, WAREHOUSES)}/stock',
            }

        start_time = time.time()
        response = requests.request(**transaction)
        transaction_log.append({
            'path': transaction['url'],
            'time': time.time() - start_time
        })

        logger.info(transaction['url'])

        if not response.ok:
            logger.error(response.json())

    with open(f'results/latency_{pid}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json', 'w') as writer:
        json.dump(transaction_log, writer)


def init():
    return requests.post(BASE_URL + '/init_db', json={'warehouses': WAREHOUSES})


def stopper(run: Value, start: Value, duration: int):
    while run.value:
        if time.time() - start.value >= duration:
            run.value = False
        time.sleep(1)


def write_results(count_orders: int, duration: int):
    filename = f'results/benchmark_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    with open(filename, 'w') as writer:
        json.dump({
            'duration': duration,
            'count_orders': count_orders,
        }, writer)


def main():
    logger.info('Benchmark starting...')

    res = init()
    if res.ok:
        logger.info('Initialized successfully')
    else:
        logger.error('Initialization failed: {}', res.json())
        exit(1)

    count_orders = Value('i', 0)
    start = Value('d', 0.0)
    run = Value('b', True)

    start.value = time.time()
    processes = []
    for i in range(2):
        process = Process(target=virtual_user, args=(i, count_orders, run))
        process.start()
        processes.append(process)

    process = Process(target=stopper, args=(run, start, DURATION))
    process.start()
    processes.append(process)

    for process in processes:
        process.join()

    write_results(count_orders.value, DURATION)


if __name__ == '__main__':
    main()
