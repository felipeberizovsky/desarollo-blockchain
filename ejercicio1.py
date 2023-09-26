# Correr pip install web3
from web3 import Web3
import os


# Variables de entorno

sepolia_http = os.environ.get('SEPOLIA_HTTP')
account = os.environ.get('ADDRESS_ACOUNT')
private_key = os.environ.get('PRIVATE_KEY')
# Me conecto al nodo para leer la información
web3 = Web3(Web3.HTTPProvider(sepolia_http))


#Verifico si me conecte exitosamente
print("Conexion:" , web3.is_connected())


# Dirección del contrato y ABI del contrato
# URL del contrato: https://sepolia.etherscan.io/address/0x757e09217F616c3b62A27573DE7c9484C57379EF
contract_address = '0x757e09217F616c3b62A27573DE7c9484C57379EF'
contract_abi = """
[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"newValue","type":"uint256"}],"name":"CounterUpdated","type":"event"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"addToWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decrement","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"increment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"removeFromWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"}]
"""

# Crea una instancia del contrato
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


# Funcion para incrementar el contador
def increment_counter():
    
    nonce = web3.eth.get_transaction_count(account)

    tx = {
        "nonce": nonce,
        "gas":200000,
        "gasPrice" :web3.eth.gas_price,
        "value":0 ,
        "chainId" :11155111,
    }
    contract_data = contract.functions.increment().build_transaction(tx)
    signed_txn = web3.eth.account.sign_transaction(contract_data, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(txn_hash.hex())


  


# Función para agregar una dirección a la whitelist
def add_to_whitelist(address_to_add):
    nonce = web3.eth.get_transaction_count(account)
    
    tx = {
        'chainId': 11155111,
        'gas': 200000, 
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
        'value': 0,
    }
    contract_data = contract.functions.addToWhitelist(address_to_add).build_transaction(tx)
    signed_txn = web3.eth.account.sign_transaction(contract_data, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(txn_hash.hex())

# Función para obtener el valor del contador
def get_count():
    return contract.functions.getCount().call({"from": "0x8233e840Fe808eeA7Cd4ba8fB18AfCAd7B6C3BcC"})


# Función para escuchar el evento y mostrar la data
def listen_to_counter_updated_event():
    filter = contract.events.CounterUpdated.create_filter(fromBlock='latest')
    
    print("Escuchando eventos CounterUpdated...")
    for event in filter.get_all_entries():
        user = event['args']['user']
        new_value = event['args']['newValue']
        
        print(f"Evento CounterUpdated capturado:")
        print(f"Usuario: {user}")
        print(f"Nuevo valor: {new_value}\n")

# Llama a la función para escuchar el evento


# LLama funciones

# print(get_count())
# add_to_whitelist("0x202b75AD34d0C51CE89f82C9558960ED9A5C4d4A")
increment_counter()
listen_to_counter_updated_event()