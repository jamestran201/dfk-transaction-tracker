import pytest

from django.test import Client
from unittest.mock import patch
from web3 import Web3

from tracker.models import TransactionSynchronization
from tracker.views.wallet_address import WalletAddressView

pytestmark = pytest.mark.django_db


@pytest.fixture
def sync_task_mock():
    with patch("tracker.views.wallet_address.sync_transactions") as mock_task:
        yield mock_task

class TestWalletAddressView:
    def test_post_success(self, client: Client, sync_task_mock):
        wallet_address = "0x17d717eb3dd20a202dce9e8e396a444db1af1d28"

        response = client.post(
            "/wallet_address/",
            {"wallet_address": wallet_address},
        )

        template_names = [template.name for template in response.templates]
        assert response.status_code == 200
        assert "wallet_address/post.html" in template_names

        task = TransactionSynchronization.objects.last()
        checksum_address = Web3.toChecksumAddress(wallet_address)
        assert task.wallet_address == checksum_address
        assert task.status == "PENDING"

        sync_task_mock.delay.assert_called_with(checksum_address, task.id)

    def test_post_invalid_address_returns_error(self, client: Client, sync_task_mock):
        response = client.post(
            "/wallet_address/",
            {"wallet_address": "dummy"},
        )
        view = WalletAddressView()

        template_names = [template.name for template in response.templates]
        assert response.status_code == 200
        assert "landing_page/index.html" in template_names
        assert response.context["error_message"] == "Please enter a valid 0x wallet address."

        sync_task_mock.delay.assert_not_called()


    def test_post_does_not_create_new_task_when_task_is_pending_or_in_progress(self, client: Client, sync_task_mock):
        wallet_address = "0x17d717eb3dd20a202dce9e8e396a444db1af1d28"
        client.post(
            "/wallet_address/",
            {"wallet_address": wallet_address},
        )

        response = client.post(
            "/wallet_address/",
            {"wallet_address": wallet_address},
        )

        template_names = [template.name for template in response.templates]
        assert response.status_code == 200
        assert "wallet_address/post.html" in template_names
        assert TransactionSynchronization.objects.count() == 1

        sync_task_mock.delay.assert_called_once()
