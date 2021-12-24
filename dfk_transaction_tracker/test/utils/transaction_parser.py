from utils.pyhmy.pyhmy import account
from utils.pyhmy.pyhmy import numbers
from utils.pyhmy.pyhmy.util import convert_one_to_hex
from contracts.contract_address import SerendaleContractAddress
from contracts.contract_address import Tokens
from datetime import datetime
from collections import Counter
import pandas as pd

def _convert_timestamp(x):
    return datetime.fromtimestamp( x ).strftime("%Y/%m/%d, %H:%M:%S")

def _convert_one_to_hex(x):
    return convert_one_to_hex( x )

def _map_address(x,main_address):
    # Parse with SerendaleContractAddress
    CONTRACT_ADDRESSES = SerendaleContractAddress.CONTRACT_ADDRESS
    CONTRACT_ADDRESSES['USER'] = main_address
    for key,values in CONTRACT_ADDRESSES.items():
        if x.lower() == values.lower():
            return key
    # Parse with Tokens
    TOKEN_ADDRESSES = Tokens.TOKEN_ADDRESS
    for key,values in TOKEN_ADDRESSES.items():
        if x.lower() == values.lower():
            return key
    return None 

class TransactionParser:
    def __init__(self,main_address,main_net='https://rpc.s0.t.hmny.io'):
        self.main_address = main_address
        self.main_net = main_net

    def _get_transactions(self):
        """
        Newest transactions are indexed earlier
        """
        all_txns = account.get_transaction_history(self.main_address,
                include_full_tx=True,
                order='DESC',
                endpoint=self.main_net)
        return all_txns

    def _process(self,all_txns):
        df = pd.DataFrame.from_dict(all_txns)
        df['blockHash'] = df['blockHash']
        df['blockNumber'] = df['blockNumber']
        df['timestamp'] = df.apply(lambda row: _convert_timestamp(row['timestamp']),axis=1)
        df['gas'] = df['gas'] / 10e17
        df['gasPrice'] = df['gasPrice'] / 10e17
        df['TxHash'] = df['hash']
        df['input'] = df['input'] # TRANSACTION DATA, for smart contracts
        df['nonce'] = df['nonce']
        df['to'] = df.apply(lambda row: _convert_one_to_hex(row['to']),axis=1)
        df['to_mapped'] = df.apply(lambda row: _map_address(row['to'],self.main_address),axis=1)
        df['from'] = df.apply(lambda row: _convert_one_to_hex(row['from']),axis=1)
        df['from_mapped'] = df.apply(lambda row: _map_address(row['from'],self.main_address),axis=1)
        df['transactionIndex'] = df['transactionIndex']
        df['value'] = df['value'] / 10e17
        df['shardID'] = df['shardID']
        df['toShardID'] = df['toShardID']
        # Clean up
        df = df.drop(columns=['hash','ethHash','r','s','v'])

        return df.sort_values(by='timestamp',ascending=False)

    def get_transactions(self,n_loops=1):
        all_txns = self._get_transactions()
        all_txns = self._process(all_txns)

        self.n_transactions = all_txns.shape[0]

        self.all_transactions = all_txns
