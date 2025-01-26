from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Folosim Infura sau Alchemy pentru a interacționa cu Ethereum (înlocuiește cu cheia ta)
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"

@app.route('/bridge', methods=['POST'])
def bridge():
    data = request.json
    address = data.get('address')
    amount = data.get('amount')

    if not address or not amount:
        return jsonify({'error': 'Missing parameters'}), 400

    # Exemplu de interogare a balanței utilizatorului
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }

    response = requests.post(INFURA_URL, json=payload)
    balance = response.json()

    return jsonify({'message': f"Bridging {amount} tokens for {address}", 'balance': balance})

if __name__ == '__main__':
    app.run(debug=True)
