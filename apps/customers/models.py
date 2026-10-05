from django.conf import settings
from django.db import models


class CustomerQuerySet(models.QuerySet):
    def visible_to(self, user):
        """Customers this user may see: staff see all, account managers see their own."""
        if user.is_staff:
            return self
        return self.filter(account_manager=user)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    country = models.CharField(max_length=2)
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="customers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomerQuerySet.as_manager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
