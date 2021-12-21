from django.db import transaction
from django.shortcuts import render
from django.views import View
from web3 import Web3

from tracker.models import TransactionSynchronization


class WalletAddressView(View):
    def post(self, request):
        wallet_address = request.POST["wallet_address"]

        if not Web3.isAddress(wallet_address):
            return render(request, "landing_page/index.html", {"error_message": "The given wallet address is not a valid 0x address."})

        checksum_address = Web3.toChecksumAddress(wallet_address)
        with transaction.atomic():
            # TODO: pass the function that enqueues a Celery task into on_commit()
            # transaction.on_commit()

            last_task = TransactionSynchronization.objects.filter(wallet_address=checksum_address).last()
            if last_task is None or last_task.status not in ("PENDING", "IN_PROGRESS"):
                TransactionSynchronization(wallet_address=checksum_address).save()

            return render(request, "wallet_address/post.html")
