from django.views import defaults as default_views
from django.urls import path

from tracker.views import landing_page
from tracker.views.wallet_address import WalletAddressView
from tracker.views.transactions import TransactionsView


app_name = "tracker"
urlpatterns = [
    path('', landing_page.index, name='index'),
    path('wallet_address/', WalletAddressView.as_view(), name="wallet_address"),
    path('transactions/', TransactionsView.as_view(), name="transactions"),
    path("500/", default_views.server_error),
]
