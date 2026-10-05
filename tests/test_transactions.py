import pytest

pytestmark = pytest.mark.django_db


def test_lists_transactions_newest_first(api, alice, make_customer, make_transaction):
    customer = make_customer(alice)
    make_transaction(customer, amount_cents=1000)
    make_transaction(customer, amount_cents=-250, type="refund")

    response = api(alice).get(f"/api/customers/{customer.id}/transactions/")

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert response.data["results"][0]["amount"] == "-2.50"


def test_filters_by_status(api, alice, make_customer, make_transaction):
    customer = make_customer(alice)
    make_transaction(customer, status="completed")
    make_transaction(customer, status="failed")

    response = api(alice).get(f"/api/customers/{customer.id}/transactions/", {"status": "failed"})

    assert response.data["count"] == 1


def test_rejects_unknown_status(api, alice, make_customer):
    customer = make_customer(alice)

    response = api(alice).get(f"/api/customers/{customer.id}/transactions/", {"status": "lost"})

    assert response.status_code == 400


def test_unknown_customer_returns_404(api, alice):
    response = api(alice).get("/api/customers/999999/transactions/")

    assert response.status_code == 404
