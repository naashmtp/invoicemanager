import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_FILE = os.path.join(BASE_DIR, 'data', 'clients.json')
INVOICES_FILE = os.path.join(BASE_DIR, 'data', 'invoices.json')


def load_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@app.route('/clients', methods=['POST'])
def create_client():
    data = load_data(CLIENTS_FILE)
    payload = request.get_json()
    client_id = payload.get('id')
    if not client_id:
        return jsonify({'error': 'Client id is required'}), 400
    if client_id in data:
        return jsonify({'error': 'Client already exists'}), 400
    data[client_id] = {
        'name': payload.get('name', '')
    }
    save_data(CLIENTS_FILE, data)
    return jsonify({'message': 'Client created', 'client': data[client_id]})


@app.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    data = load_data(CLIENTS_FILE)
    client = data.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({'client': client})


@app.route('/invoices', methods=['POST'])
def create_invoice():
    invoices = load_data(INVOICES_FILE)
    clients = load_data(CLIENTS_FILE)
    payload = request.get_json()
    invoice_id = payload.get('id')
    client_id = payload.get('client_id')
    if not invoice_id or not client_id:
        return jsonify({'error': 'Invoice id and client id are required'}), 400
    if invoice_id in invoices:
        return jsonify({'error': 'Invoice already exists'}), 400
    if client_id not in clients:
        return jsonify({'error': 'Client does not exist'}), 400
    invoice = {
        'client_id': client_id,
        'amount': payload.get('amount', 0),
        'description': payload.get('description', '')
    }
    invoices[invoice_id] = invoice
    save_data(INVOICES_FILE, invoices)
    return jsonify({'message': 'Invoice created', 'invoice': invoice})


@app.route('/clients/<client_id>/invoices', methods=['GET'])
def list_invoices(client_id):
    clients = load_data(CLIENTS_FILE)
    if client_id not in clients:
        return jsonify({'error': 'Client not found'}), 404
    invoices = load_data(INVOICES_FILE)
    client_invoices = {
        inv_id: inv
        for inv_id, inv in invoices.items()
        if inv['client_id'] == client_id
    }
    return jsonify({'invoices': client_invoices})


if __name__ == '__main__':
    # Listen on all interfaces so the app is reachable from the network
    app.run(host='0.0.0.0', debug=True)
