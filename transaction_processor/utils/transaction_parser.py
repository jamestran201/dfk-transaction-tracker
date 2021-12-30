from pyhmy import account
from pyhmy import numbers
from pyhmy.util import convert_one_to_hex
from transaction_processor.contracts.contract_address import SerendaleContractAddress
from transaction_processor.contracts.contract_address import Tokens
from datetime import datetime
from collections import Counter
import pandas as pd

def _convert_timestamp(x):
    return datetime.fromtimestamp( x ).strftime("%Y/%m/%d, %H:%M:%S")

def _map_address_to_readable_name(address, main_address):
    # Parse with SerendaleContractAddress
    address = address.lower()

    CONTRACT_ADDRESSES = SerendaleContractAddress.CONTRACT_ADDRESS
    CONTRACT_ADDRESSES[main_address.lower()] = "USER"
    name = CONTRACT_ADDRESSES.get(address, None)
    if name:
        return name

    name = Tokens.TOKEN_ADDRESS.get(address, None)
    return name

class TransactionFetcher:
    def __init__(self,main_address,main_net='https://rpc.s0.t.hmny.io'):
        self.main_address = main_address
        self.main_net = main_net

    def _is_txn_relevant(self, transaction):
        to_address = convert_one_to_hex(transaction["to"]).lower()
        from_address = convert_one_to_hex(transaction["from"]).lower()

        return to_address in SerendaleContractAddress.CONTRACT_ADDRESS or \
                    to_address in Tokens.TOKEN_ADDRESS or \
                    from_address in SerendaleContractAddress.CONTRACT_ADDRESS or \
                    from_address in Tokens.TOKEN_ADDRESS

    def _select_defi_kingdoms_txn(self, all_txns):
        return [txn for txn in all_txns if self._is_txn_relevant(txn)]

    def _get_transactions(self):
        """
        Newest transactions are indexed earlier
        """
        #print(account.get_transactions_count(self.main_address,'ALL',endpoint=self.main_net))
        all_txns = account.get_transaction_history(
                self.main_address,
                page=0,
                page_size=50_000,
                include_full_tx=True,
                order='DESC',
                endpoint=self.main_net)
        return all_txns

    def _process(self,all_txns):
        filtered_txns = self._select_defi_kingdoms_txn(all_txns)
        df = pd.DataFrame.from_dict(filtered_txns)

        df['blockHash'] = df['blockHash']
        df['blockNumber'] = df['blockNumber']
        df['timestamp'] = df.apply(lambda row: _convert_timestamp(row['timestamp']),axis=1)
        df['gas'] = df['gas'] / 10e17
        df['gasPrice'] = df['gasPrice'] / 10e17
        df['TxHash'] = df['hash']
        df['input'] = df['input'] # TRANSACTION DATA, for smart contracts
        df['nonce'] = df['nonce']
        df['to'] = df.apply(lambda row: convert_one_to_hex(row['to']),axis=1)
        df['to_mapped'] = df.apply(lambda row: _map_address_to_readable_name(row['to'],self.main_address),axis=1)
        df['from'] = df.apply(lambda row: convert_one_to_hex(row['from']),axis=1)
        df['from_mapped'] = df.apply(lambda row: _map_address_to_readable_name(row['from'],self.main_address),axis=1)
        df['transactionIndex'] = df['transactionIndex']
        df['value'] = df['value'] / 10e17
        df['shardID'] = df['shardID']
        df['toShardID'] = df['toShardID']
        # Clean up
        df = df.drop(columns=['hash','ethHash','r','s','v'])

        return df.sort_values(by='timestamp',ascending=True)

    def get_transactions(self,n_loops=1):
        all_txns = self._get_transactions()
        all_txns = self._process(all_txns)

        self.n_transactions = all_txns.shape[0]

        self.all_transactions = all_txns
