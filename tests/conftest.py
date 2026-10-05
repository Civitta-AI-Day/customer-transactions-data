import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.customers.models import Customer
from apps.transactions.models import Transaction


@pytest.fixture
def make_user(db):
    def _make(username, is_staff=False):
        return get_user_model().objects.create_user(
            username=username, password="x", is_staff=is_staff
        )

    return _make


@pytest.fixture
def alice(make_user):
    return make_user("alice")


@pytest.fixture
def bob(make_user):
    return make_user("bob")


@pytest.fixture
def carol(make_user):
    return make_user("carol", is_staff=True)


@pytest.fixture
def make_customer(db):
    def _make(manager, name="Test Customer", country="AM"):
        return Customer.objects.create(
            name=name, email="c@example.com", country=country, account_manager=manager
        )

    return _make


@pytest.fixture
def make_transaction(db):
    counter = {"n": 0}

    def _make(
        customer,
        amount_cents=1000,
        status="completed",
        type="payment",
        currency="EUR",
        created_at=None,
    ):
        counter["n"] += 1
        return Transaction.objects.create(
            customer=customer,
            type=type,
            amount_cents=amount_cents,
            currency=currency,
            status=status,
            reference=f"TEST-{counter['n']:06d}",
            created_at=created_at or timezone.now(),
        )

    return _make


@pytest.fixture
def api():
    def _client(user=None):
        client = APIClient()
        if user is not None:
            client.force_authenticate(user)
        return client

    return _client
