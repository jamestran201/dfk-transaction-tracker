import pytest
from django.test import RequestFactory
from web3 import Web3

from api.models import TransactionSynchronization
from api.views.transaction_syncrhonization import TransactionSynchronizationViewSet

pytestmark = pytest.mark.django_db


class TestTransactionSynchronizationViewSet:
    def test_create_success(self, rf: RequestFactory):
        wallet_address = "0x17d717eb3dd20a202dce9e8e396a444db1af1d28"
        request = rf.post(
            "/transaction_syncrhonization/",
            {"wallet_address": wallet_address},
            content_type="application/json",
        )

        response = TransactionSynchronizationViewSet().create(request)

        task = TransactionSynchronization.objects.last()
        checksum_address = Web3.toChecksumAddress(wallet_address)
        assert response.status_code == 201
        assert response.data == {"status": "success"}
        assert task.wallet_address == checksum_address
        assert task.status == "PENDING"

    def test_create_invalid_address_returns_error(self, rf: RequestFactory):
        request = rf.post(
            "/transaction_syncrhonization/",
            {"wallet_address": "dummy"},
            content_type="application/json",
        )

        response = TransactionSynchronizationViewSet().create(request)

        assert response.status_code == 400
        assert response.data == {"status": "failed", "message": "The given wallet address is not a valid 0x address"}

    def test_create_does_not_create_new_task_when_task_is_pending_or_in_progress(self, rf: RequestFactory):
        wallet_address = "0x17d717eb3dd20a202dce9e8e396a444db1af1d28"
        request1 = rf.post(
            "/transaction_syncrhonization/",
            {"wallet_address": wallet_address},
            content_type="application/json",
        )
        TransactionSynchronizationViewSet().create(request1)

        request2 = rf.post(
            "/transaction_syncrhonization/",
            {"wallet_address": wallet_address},
            content_type="application/json",
        )
        response = TransactionSynchronizationViewSet().create(request2)

        assert response.status_code == 202
        assert response.data == {"status": "success"}
        assert TransactionSynchronization.objects.count() == 1
