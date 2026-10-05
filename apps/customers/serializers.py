from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    account_manager = serializers.CharField(source="account_manager.username", read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "country", "account_manager", "created_at"]


class CustomerSearchQuerySerializer(serializers.Serializer):
    """Validates query parameters for the customer list endpoint."""

    q = serializers.CharField(required=False, max_length=100)
    country = serializers.RegexField(r"^[A-Z]{2}$", required=False)
