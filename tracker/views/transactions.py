from math import ceil

from django.db.models import Q
from django.shortcuts import render
from django.views import View

from tracker.models import Transaction
from tracker.presenters.transaction_presenter import TransactionPresenter
from tracker.presenters.transaction_paginator import TransactionPaginator


TRANSACTIONS_PER_PAGE = 10


class TransactionsView(View):
    def get(self, request):
        wallet_address = request.GET["wallet_address"]
        current_page = int(request.GET["page"])

        query_condition = Q(address_to=wallet_address) | Q(address_from=wallet_address)

        start = (current_page - 1) * TRANSACTIONS_PER_PAGE
        end = start + TRANSACTIONS_PER_PAGE
        transactions = Transaction.objects.filter(query_condition).order_by("-transaction_timestamp")[start:end]

        total_transactions = Transaction.objects.filter(query_condition).count()
        total_pages = ceil(total_transactions / TRANSACTIONS_PER_PAGE)
        pagination_presenter = TransactionPaginator(total_pages, current_page)
        presenters = [TransactionPresenter(t) for t in transactions]

        return render(request, "transactions/get.html", {"transactions": presenters, "paginator": pagination_presenter, "wallet_address": wallet_address})
