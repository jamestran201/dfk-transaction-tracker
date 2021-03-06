from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from web3 import Web3

from tracker.models import TransactionSynchronization, Transaction
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

        return render(request, "wallet_address/post.html", {"wallet_address": checksum_address})
        # return redirect(f"/transactions?wallet_address={checksum_address}&page=1")

    def get(self, request):
        wallet_address = request.GET["wallet_address"]

        query_condition = Q(address_to=wallet_address) | Q(address_from=wallet_address)
        total_transactions = Transaction.objects.filter(query_condition).count()

        sync_task = TransactionSynchronization.objects.filter(wallet_address=wallet_address).last()

        return JsonResponse({"status": sync_task.status, "total_transactions": total_transactions})
