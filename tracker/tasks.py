from dfk_transaction_tracker.celery import app

from tracker.models import TransactionSynchronization


@app.task()
def get_count():
    """A pointless Celery task to demonstrate usage."""
    print(TransactionSynchronization.objects.count())
