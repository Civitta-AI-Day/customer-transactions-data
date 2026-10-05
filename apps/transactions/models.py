from django.db import models

from apps.customers.models import Customer


class Transaction(models.Model):
    class Type(models.TextChoices):
        PAYMENT = "payment"
        REFUND = "refund"
        TRANSFER = "transfer"
        FEE = "fee"

    class Status(models.TextChoices):
        COMPLETED = "completed"
        PENDING = "pending"
        FAILED = "failed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=20, choices=Type.choices)
    amount_cents = models.BigIntegerField(help_text="Signed amount in cents. Never a float.")
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=Status.choices, db_index=True)
    reference = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.reference
