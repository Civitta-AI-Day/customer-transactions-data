from rest_framework import serializers

from apps.core.money import format_cents

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["id", "created_at", "type", "amount", "currency", "status", "reference"]

    def get_amount(self, obj) -> str:
        return format_cents(obj.amount_cents)


class TransactionListQuerySerializer(serializers.Serializer):
    """Validates query parameters for the transaction list endpoint."""

    status = serializers.ChoiceField(choices=Transaction.Status.choices, required=False)
