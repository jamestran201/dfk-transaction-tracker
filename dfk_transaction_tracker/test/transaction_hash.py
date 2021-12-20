from utils.pyhmy.pyhmy import transaction
from utils.utils import get_transaction_receipt
from utils.utils import get_transaction_receipt_data
from utils.utils import process_transaction_data
from utils.pyhmy.pyhmy.util import convert_one_to_hex

from rich.console import Console
console = Console()

import warnings
warnings.simplefilter("ignore")

"""
INPUTS
"""
txn_hash = '0xde7a1d0e653b16bb017f4176eefc69651f1b3224875740458fce9210fc45fae5'
verbose = True
main_net='https://rpc.s0.t.hmny.io'
main_address = '0x0000000000000000000000000000000000000000'

if verbose: 
    console.print(f"TRANSACTION HASH: [magenta] {txn_hash}")

transaction_info = transaction.get_transaction_by_hash(txn_hash,endpoint=main_net)
transaction_receipt = get_transaction_receipt(txn_hash) # transaction receipt (logs/topics) have useful information that we do not use here
transaction_data = get_transaction_receipt_data(transaction_receipt,
        transaction_info['input'],
        convert_one_to_hex(transaction_info['to']),
        main_address = main_address, # FILL
        abidir='contracts/abi')
process_transaction_data(transaction_data,main_address=main_address,verbose=verbose) # print transaction receipt / verbose=True
