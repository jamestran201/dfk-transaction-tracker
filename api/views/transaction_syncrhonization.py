from django.db import transaction
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from web3 import Web3

from api.models import TransactionSynchronization


class TransactionSynchronizationViewSet(ViewSet):
    def create(self, request):
        data = JSONParser().parse(request)
        wallet_address = data["wallet_address"]

        if not Web3.isAddress(wallet_address):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"status": "failed", "message": "The given wallet address is not a valid 0x address"})

        checksum_address = Web3.toChecksumAddress(wallet_address)
        with transaction.atomic():
            # TODO: pass the function that enqueues a Celery task into on_commit()
            # transaction.on_commit()

            last_task = TransactionSynchronization.objects.filter(wallet_address=checksum_address).last()
            if last_task is None or last_task.status not in ("PENDING", "IN_PROGRESS"):
                TransactionSynchronization(wallet_address=checksum_address).save()
                return Response(status=status.HTTP_201_CREATED, data={"status": "success"})
            else:
                return Response(status=status.HTTP_202_ACCEPTED, data={"status": "success"})
