from django.urls import path

from .views import CustomerTransactionListView

urlpatterns = [
    path(
        "customers/<int:customer_id>/transactions/",
        CustomerTransactionListView.as_view(),
        name="customer-transaction-list",
    ),
]
