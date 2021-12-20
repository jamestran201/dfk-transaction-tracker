import os

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
#main_address = '0xe674B732DC82E9CB111D18cAbDf7543CE74e2c85' # My wallet
main_address = '0x2E7669F61eA77F02445A015FBdcFe2DE47083E02'
verbose = True


console.print(f"USER: [magenta] {main_address}")

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

    # Print transaction info
    if verbose:
        console.print(f"\n[[cyan]{df_row.timestamp}[/]] || [TXN HASH] [magenta]{df_row.TxHash}[/] || {idx}",highlight=True)
        console.print(f"[yellow bold]{contract_address_from}[/] > [yellow bold]{contract_address_to}[/]",highlight=False)
        print(f"gas: {df_row.gas} [ONE]\ngasPrice: {df_row.gasPrice} [ONE]\nnonce: {df_row.nonce}\nvalue: {df_row.value} [ONE]")
    
    transaction_receipt = get_transaction_receipt(df_row['TxHash']) # transaction receipt (logs/topics) have useful information that we do not use here
    transaction_data = get_transaction_receipt_data(transaction_receipt,
            df_row['input'],
            df_row['to'],
            main_address,abidir='contracts/abi')
    process_transaction_data(transaction_data,main_address=main_address,verbose=verbose) # print transaction receipt / verbose=True
