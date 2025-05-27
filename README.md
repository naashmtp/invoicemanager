# Invoice Manager

This project provides a simple Flask-based API to manage clients and invoices.

## Requirements
- Python 3.8+
- Flask

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Start the server:
```bash
python app.py
```

### Creating a client
```bash
curl -X POST http://localhost:5000/clients -H 'Content-Type: application/json' -d '{"id": "client1", "name": "John Doe"}'
```

### Creating an invoice
```bash
curl -X POST http://localhost:5000/invoices -H 'Content-Type: application/json' -d '{"id": "inv1", "client_id": "client1", "amount": 100.0, "description": "Website design"}'
```

### Listing invoices for a client
```bash
curl http://localhost:5000/clients/client1/invoices
```

Data is stored in JSON files under the `data/` directory for simplicity.
