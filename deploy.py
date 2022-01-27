from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# Create a JSON file with compiled code
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get the ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

print("Connecting to http provider...")

#################################################################################
# Connect to ganache
# w3 = Web3(Web3.HTTPProvider(os.getenv("MY_HTTP_PROVIDER")))
# chain_id = 1337
# my_address = os.getenv("MY_ADDRESS")
# private_key = os.getenv("PRIVATE_KEY")
#################################################################################

#################################################################################
# Connect to the Rinkeby testnet using infura and metamask
w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_RINKEBY_ENDPOINT")))
chain_id = int(os.getenv("RINKEBY_CHAIN_ID"))
my_address = os.getenv("MM_DEV_ADDRESS")
private_key = os.getenv("MM_DEV_PRIV_KEY")
#################################################################################

print("Connected to http provider")

print("Deploying contract...")
# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction count
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1. Create transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# 2. Sign transaction
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed!")


# Working with a contract, we need:
# 1. Contract address
# 2. Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("Current favoriteNumber: ", simple_storage.functions.retreive().call())

print("Setting new favorite number to 15")

## Create transaction that stores number

# 1. Build transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)

# 2. Sign transaction
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# 3. Send transaction
store_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_store_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print("Done storing new number")
print("Current favoriteNumber: ", simple_storage.functions.retreive().call())

