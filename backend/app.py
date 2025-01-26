from flask import Flask, request, jsonify
from web3 import Web3
import json
from flask_cors import CORS

# Conectare la blockchain (Anvil)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Adresa contractului (înlocuiește cu adresa reală de la deploy!)
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

with open("IBT_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Conectare la contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Adresa și cheia privată a owner-ului (Anvil Account 0)
owner_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8080"}})  # ✅ Permite doar frontend-ul tău

# Endpoint pentru mint
@app.route('/mint', methods=['POST'])
def mint():
    data = request.json
    to = data.get("to")
    amount = int(data.get("amount"))

    # Construim tranzacția
    tx = contract.functions.mint(to, amount).build_transaction({
        'from': owner_address,
        'gas': 3000000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(owner_address),
    })

    # Semnăm și trimitem tranzacția
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)  # ✅ Folosește `raw_transaction`
    
    return jsonify({"tx_hash": tx_hash.hex()}), 200

# Endpoint pentru burn
@app.route('/burn', methods=['POST'])
def burn():
    data = request.json
    from_address = data.get("from")
    amount = int(data.get("amount"))

    # Construim tranzacția
    tx = contract.functions.burn(from_address, amount).build_transaction({
        'from': owner_address,
        'gas': 3000000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(owner_address),
    })

    # Semnăm și trimitem tranzacția
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)  # ✅ Folosește `raw_transaction`

    return jsonify({"tx_hash": tx_hash.hex()}), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "No address provided"}), 400

    balance = contract.functions.balanceOf(address).call()
    return jsonify({"balance": balance}), 200


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)  # ✅ Rulează Flask pe port 8080
