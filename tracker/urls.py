from django.urls import path

from tracker.views import landing_page
from tracker.views.wallet_address import WalletAddressView


app_name = "tracker"
urlpatterns = [
    path('', landing_page.index, name='index'),
    path('wallet_address/', WalletAddressView.as_view(), name="wallet_address")
]
