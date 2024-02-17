from flask import Flask, abort, request, jsonify

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
def hello_world(transaction):
    if transaction in transactions:
        try:
            data = request.json
            transaction_fn = transactions[transaction]
            result = transaction_fn(**data)
            return jsonify(result=result)
        except Exception as e:
            return jsonify(error=type(e).__name__, message=str(e)), 400

    abort(404)
