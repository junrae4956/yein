from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 임시 데이터 저장소 (예: In-memory storage)
orders = []

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    order = {
        'id': len(orders) + 1,
        'details': data['details'],
        'status': 'created',
        'created_at': datetime.now(),
        'assigned_driver': None,
        'assigned_time': None,
        'delivered_at': None,
        'additional_items': []
    }
    orders.append(order)
    return jsonify(order), 201

@app.route('/order/<int:order_id>/assign', methods=['POST'])
def assign_driver(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'assigned'
            order['assigned_driver'] = request.json['driver']
            order['assigned_time'] = datetime.now()
            return jsonify(order), 200
    return jsonify({'error': 'Order not found'}), 404

@app.route('/order/<int:order_id>/deliver', methods=['POST'])
def deliver_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'delivered'
            order['delivered_at'] = datetime.now()
            return jsonify(order), 200
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == "__main__":
    app.run(debug=True)
