from dfk_transaction_tracker.celery import app
from tracker.models import TransactionSynchronization
from transaction_processor.utils.transaction_parser import TransactionParser


@app.task()
def get_count():
    """A pointless Celery task to demonstrate usage."""
    print(TransactionSynchronization.objects.count())

@app.task()
def sync_transactions(wallet_address, sync_task_id):
    TransactionParser(wallet_address).get_transactions()

    sync_task = TransactionSynchronization.objects.get(id=sync_task_id)
    sync_task.status = "SUCCESS"
    sync_task.save()
