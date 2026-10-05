"""Authorization rules for customers.

Convention: every endpoint that touches a customer's data must check
access through CanViewCustomer (or Customer.objects.visible_to for lists).
Never compare users inline in a view.
"""

from rest_framework.permissions import BasePermission


def can_view_customer(user, customer) -> bool:
    return user.is_staff or customer.account_manager_id == user.id


class CanViewCustomer(BasePermission):
    """Object-level permission: the user may view this customer and its data."""

    message = "You do not have access to this customer."

    def has_object_permission(self, request, view, obj):
        return can_view_customer(request.user, obj)
