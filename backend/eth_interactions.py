from web3 import Web3

# Conectare la Ethereum (Anvil)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# ✅ Actualizează cu adresa CONTRACTULUI, NU a unui cont!
contract_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"  # Înlocuiește cu adresa reală a contractului

# ✅ ABI-ul contractului - trebuie copiat din Remix după deploy
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}],
        "name": "mint",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "from", "type": "address"}, {"name": "amount", "type": "uint256"}],
        "name": "burn",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# ✅ Inițializează contractul
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# ✅ Adresa și cheia privată pentru contul 0 din Anvil (folosit pentru tranzacții)
account_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

# ✅ Funcție pentru minting (creare de tokenuri)
def mint_ethereum(to_address, amount):
    nonce = web3.eth.get_transaction_count(account_address)

    txn = contract.functions.mint(to_address, amount).build_transaction({
        'from': account_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })

    # Semnează și trimite tranzacția
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"✅ Minting {amount} IBT tokens to {to_address} | TX Hash: {web3.to_hex(tx_hash)}")

# ✅ Funcție pentru burn (ardere de tokenuri)
def burn_ethereum(from_address, amount):
    nonce = web3.eth.get_transaction_count(account_address)

    txn = contract.functions.burn(from_address, amount).build_transaction({
        'from': account_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })

    # Semnează și trimite tranzacția
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"🔥 Burning {amount} IBT tokens from {from_address} | TX Hash: {web3.to_hex(tx_hash)}")
