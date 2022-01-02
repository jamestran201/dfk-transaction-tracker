from django.db import transaction
from django.shortcuts import render
from django.views import View
from web3 import Web3

from tracker.models import TransactionSynchronization
from tracker.tasks import sync_transactions


class WalletAddressView(View):
    def post(self, request):
        wallet_address = request.POST["wallet_address"]

        if not Web3.isAddress(wallet_address):
            return render(request, "landing_page/index.html", {"error_message": "Please enter a valid 0x wallet address."})

        checksum_address = Web3.toChecksumAddress(wallet_address)
        should_enqueue_task = False
        with transaction.atomic():
            last_task = TransactionSynchronization.objects.filter(wallet_address=checksum_address).last()
            if last_task is None or last_task.status not in ("PENDING", "IN_PROGRESS"):
                sync_task = TransactionSynchronization(wallet_address=checksum_address)
                sync_task.save()
                should_enqueue_task = True

        if should_enqueue_task:
            sync_transactions.delay(checksum_address, sync_task.id)

        return render(request, "wallet_address/post.html")
