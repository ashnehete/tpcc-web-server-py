from flask import Flask, abort, request, jsonify
from werkzeug.exceptions import HTTPException

from tpcc.init_db import init_db
from tpcc.transactions import *

app = Flask(__name__)

transactions = {
    "new_order": new_order_tran,
    "payment": payment_tran,
    "order_status": order_status_tran,
    "delivery": delivery_tran,
    "stock_level": stock_level_tran
}


@app.route("/transaction/<transaction>", methods=['POST'])
def transaction_route(transaction):
    if transaction in transactions:
        data = request.json
        transaction_fn = transactions[transaction]
        result = transaction_fn(**data)
        return jsonify(result=result)

    abort(404)


@app.route("/init_db", methods=["POST"])
def init_db_route():
    try:
        warehouses = request.json['warehouses']
    except:
        warehouses = AMOUNT_OF_WAREHOUSES

    init_db(warehouses)
    return jsonify(result=True)


@app.errorhandler(Exception)
def handle_exception(exception):
    status_code = 500
    if isinstance(exception, TypeError):
        status_code = 400
    elif isinstance(exception, HTTPException):
        status_code = exception.code

    return jsonify(error=type(exception).__name__, message=str(exception)), status_code
