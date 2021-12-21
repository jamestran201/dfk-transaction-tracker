from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.transaction_syncrhonization import TransactionSynchronizationViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'transaction_syncrhonization', TransactionSynchronizationViewSet, basename="transaction_syncrhonization")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
