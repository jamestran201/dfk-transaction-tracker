from dfk_transaction_tracker.celery import app
from tracker.models import TransactionSynchronization
from tracker.models import Wallet as WalletModel
from tracker.models import Transaction as TransactionModel
from transaction_processor.utils.transaction_parser import TransactionFetcher
from transaction_processor.utils.utils import get_transaction_receipt, get_transaction_receipt_data
from transaction_processor.utils.transaction import Transaction
from datetime import datetime

@app.task()
def sync_transactions(wallet_address, sync_task_id):
    sync_task = TransactionSynchronization.objects.get(id=sync_task_id)
    sync_task.status = "IN_PROGRESS"
    sync_task.save()

    try:
        # Save wallet into db
        defaults = {
            'wallet_address': wallet_address,
            'updated_at': datetime.now()
        }
        wallet, _ = WalletModel.objects.update_or_create(
            wallet_address=wallet_address,
            defaults=defaults
        )

        # Get transactions
        txn_parser = TransactionFetcher(wallet_address)
        txn_parser.get_transactions()
        all_txns = txn_parser.all_transactions

        df_transactions = filter_db_transactions(all_txns)
        for idx in range(df_transactions.shape[0]):
            df_row = df_transactions.iloc[idx]
            transaction_receipt = get_transaction_receipt(df_row['TxHash'])
            transaction_data = get_transaction_receipt_data(
                transaction_receipt,
                df_row['input'],
                df_row['to'],
                wallet_address
            )
            transaction = Transaction(
                wallet_address,
                df_row,
                transaction_receipt,
                transaction_data,
                wallet.crystal_log,
                verbose=False
            )
            transaction.get_info()

            # set wallet created_at time to when the dfk profile was created
            if transaction.info['to_mapped'] == 'Serendale_Profiles':
                wallet.created_at = datetime.strptime(
                    transaction.info['timestamp'],
                    "%Y/%m/%d, %H:%M:%S"
                )
                wallet.save()

            # Convert transaction.info['status'] into DB CharField
            if transaction.info['status'] == 1:
                status = "SUCCESS"
            else:
                status = "FAILED"

            # Save Transaction into database
            defaults = {
                'wallet':wallet,
                'transaction_hash':transaction.info['TxHash'],
                'transaction_timestamp':datetime.strptime(transaction.info['timestamp'],"%Y/%m/%d, %H:%M:%S"),
                'status':status,
                'address_from':transaction.info['from'],
                'address_to':transaction.info['to'],
                'from_mapped':transaction.info['from_mapped'],
                'to_mapped':transaction.info['to_mapped'],
                'function':transaction.info['function'],
                'transaction_fee':transaction.info['TxFee'],
                'token_transaction':transaction.info['TxTokens'],
                'hero_transaction':transaction.hero_log,
                'lp_transaction':transaction.liquiditypool,
            }

            transaction_model, txn_created = TransactionModel.objects.update_or_create(
                transaction_hash=transaction.info['TxHash'],
                defaults=defaults
            )

            wallet.crystal_log = transaction.crystalId_log
            wallet.save()

            transaction_model.update_balance()
    except Exception as e:
        sync_task.status = "FAILED"
        sync_task.save()

        raise e

    sync_task.status = "SUCCESS"
    sync_task.save()

def filter_db_transactions(df):
    """
    Remove transactions that are already stored in the database.
    """
    txn_hashes = df['TxHash'].to_list()
    db_txns = [ txn_hash for txn_hash in txn_hashes \
            if TransactionModel.objects.filter(transaction_hash=txn_hash).exists() ]

    return df[~df['TxHash'].isin(db_txns)].reset_index(drop=True)
