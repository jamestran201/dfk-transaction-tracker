import os

from utils.transaction_parser import TransactionFetcher
from utils.utils import get_transaction_receipt
from utils.utils import get_transaction_receipt_data
from utils.transaction import Transaction

from rich.console import Console
console = Console()

import warnings
warnings.simplefilter("ignore")


"""
INPUTS
"""
main_addresses = [
        '***REMOVED***', # My Wallet
        #'***REMOVED***', # FriskyFox (Dev)
        #'***REMOVED***', # Raspberry Swirl (Dev)
        #'***REMOVED***', # baloo3101 (dfk auction bot)
        ]
verbose = True

for main_address in main_addresses:

    console.print(f"USER: [magenta] {main_address}[/]")
    # log of crystalId for tracking value of summoned heroes
    crystal_log = {}
    # Get transaction parser
    txn_parser = TransactionFetcher(main_address)
    txn_parser.get_transactions()
    # Get contract address
    for idx in range(txn_parser.n_transactions):
        df_row = txn_parser.all_transactions.iloc[idx]
        transaction_receipt = get_transaction_receipt(df_row['TxHash'])
        transaction_data = get_transaction_receipt_data(
            transaction_receipt,
            df_row['input'],
            df_row['to'],
            main_address
        )
        transaction = Transaction(
                main_address,
                df_row,
                transaction_receipt,
                transaction_data,
                crystal_log,
                verbose=verbose
                )
        transaction.get_info()
        # Update crystalId log
        crystal_log = transaction.crystalId_log
