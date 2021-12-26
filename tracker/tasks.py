from dfk_transaction_tracker.celery import app
from tracker.models import TransactionSynchronization
from transaction_processor.utils.transaction_parser import TransactionFetcher


@app.task()
def sync_transactions(wallet_address, sync_task_id):
    try:
        TransactionFetcher(wallet_address).get_transactions()
    except Exception as e:
        sync_task = TransactionSynchronization.objects.get(id=sync_task_id)
        sync_task.status = "FAILED"
        sync_task.save()

        raise e

    sync_task = TransactionSynchronization.objects.get(id=sync_task_id)
    sync_task.status = "SUCCESS"
    sync_task.save()
