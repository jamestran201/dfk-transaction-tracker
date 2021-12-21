import os

from utils.utils import _process_address

from utils.transaction_parser import TXNParser
from utils.utils import get_transaction_receipt
from utils.utils import get_transaction_receipt_data
from utils.utils import process_transaction_data

from rich.console import Console
console = Console()

import warnings
warnings.simplefilter("ignore")

"""
INPUTS
"""
main_address = '***REMOVED***' # My wallet
#main_address = '***REMOVED***'
verbose = True

console.print(f"USER: [magenta] {main_address}")

# Get transaction parser
txn_parser = TXNParser(main_address)
txn_parser.get_transactions()
# Get contract address
for idx in range(txn_parser.n_transactions):
    df_row = txn_parser.all_transactions.iloc[idx]
    _contract_address_from = df_row['from']
    _contract_address_to = df_row['to']
    _contract_address_from_mapped = df_row['from_mapped']
    _contract_address_to_mapped = df_row['to_mapped']
    if _contract_address_from_mapped is None:
        contract_address_from = _contract_address_from
    else:
        contract_address_from = _contract_address_from_mapped
    if _contract_address_to_mapped is None:
        contract_address_to = _contract_address_to
    else:
        contract_address_to = _contract_address_to_mapped

    #if contract_address_to != 'Serendale_MasterGardener':
    #    continue

    # Print transaction info
    if verbose:
        console.print(f"\n[[cyan]{df_row.timestamp}[/]] || [TXN HASH] [magenta]{df_row.TxHash}[/] || {idx}",highlight=True)
        console.print(f"[yellow bold]{contract_address_from}[/] > [yellow bold]{contract_address_to}[/]",highlight=False)
        print(f"gas: {df_row.gas} [ONE]\ngasPrice: {df_row.gasPrice} [ONE]\nnonce: {df_row.nonce}\nvalue: {df_row.value} [ONE]")
   
    """
    TEST
    """
    """
    from utils.abi_parser import ABIParser
    from web3 import Web3
    w3 =  Web3(Web3.HTTPProvider('https://rpc.s0.t.hmny.io'))

    transaction_receipt = get_transaction_receipt(df_row['TxHash']) # transaction receipt (logs/topics) have useful information that we do not use here
    print(f"------[RAW] TRANSACTION RECEIPT------")
    receipt_dict = {}
    filtered_keys = ['contractAddress','cumulativeGasUsed','gasUsed','status']
    for key in filtered_keys:
        print(f"{key} || {transaction_receipt[key]}")
        receipt_dict[key] = transaction_receipt[key]
    for idx,log in enumerate(transaction_receipt['logs']):
        receipt_event_signature_hex = w3.toHex(log['topics'][0])
        jsons = [f"contracts/abi/{i}" for i in os.listdir('contracts/abi')]
        for _json in jsons:
            abi = ABIParser(_json).load_json()
            contract = w3.eth.contract(log['address'], abi=abi)
            abi_events = [abi for abi in contract.abi if abi["type"] == "event"]
            for event in abi_events:
                name = event['name']
                inputs = ','.join([param['type'] for param in event['inputs']])
                event_signature_text = f"{name}({inputs})"
                event_signature_hex = w3.toHex(w3.keccak(text=event_signature_text))
                if event_signature_hex == receipt_event_signature_hex:
                    console.print(f"[red bold]MATCH[/]: {event_signature_text} ({_json})",highlight=False)
                    _address = log['address']
                    _address = _process_address(_address,main_address)
                    print(f"logs || {log['logIndex']}")
                    console.print(f"log (address): [cyan]{_address}[/]",highlight=False)
                    """
                    #abi = ABIParser('contracts/abi/IUniswapV2Pair.json').load_json()
                    #jewel_lp = '0xA1221A5BBEa699f507CC00bDedeA05b5d2e32Eba'
                    #contract = w3.eth.contract(jewel_lp, abi=abi)
                    #token0 = contract.functions.token0().call()
                    #token1 = contract.functions.token1().call()

    """
    TEST
    """
    transaction_receipt = get_transaction_receipt(df_row['TxHash']) # transaction receipt (logs/topics) have useful information that we do not use here
    transaction_data = get_transaction_receipt_data(transaction_receipt,
            df_row['input'],
            df_row['to'],
            main_address,abidir='contracts/abi')
    process_transaction_data(transaction_data,main_address=main_address,verbose=verbose) # print transaction receipt / verbose=True
