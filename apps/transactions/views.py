from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.customers.models import Customer

from .serializers import TransactionListQuerySerializer, TransactionSerializer


class CustomerTransactionListView(generics.ListAPIView):
    """GET /api/customers/{customer_id}/transactions/ — paginated, newest first."""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = TransactionListQuerySerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        customer = get_object_or_404(Customer, pk=self.kwargs["customer_id"])
        qs = customer.transactions.all()
        if status := params.validated_data.get("status"):
            qs = qs.filter(status=status)
        return qs
