from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from .models import Customer
from .permissions import CanViewCustomer
from .serializers import CustomerSearchQuerySerializer, CustomerSerializer


class CustomerListView(generics.ListAPIView):
    """GET /api/customers/ — customers visible to the current user, with optional search."""

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "customer-search"

    def get_queryset(self):
        params = CustomerSearchQuerySerializer(data=self.request.query_params)
        params.is_valid(raise_exception=True)
        qs = Customer.objects.visible_to(self.request.user).select_related("account_manager")
        if q := params.validated_data.get("q"):
            qs = qs.filter(name__icontains=q)
        if country := params.validated_data.get("country"):
            qs = qs.filter(country=country)
        return qs


class CustomerDetailView(generics.RetrieveAPIView):
    """GET /api/customers/{id}/ — one customer, only if the user may view it."""

    queryset = Customer.objects.select_related("account_manager")
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, CanViewCustomer]
