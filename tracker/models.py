from django.db import models

class TransactionSynchronization(models.Model):

    class Meta:
        db_table = "transaction_synchronization"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        IN_PROGRESS = "IN_PROGRESS"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"

    id = models.BigAutoField(primary_key=True)
    wallet_address = models.CharField(max_length=1024)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
