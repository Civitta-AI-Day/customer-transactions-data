import pytest

pytestmark = pytest.mark.django_db


def test_list_shows_only_own_customers(api, alice, bob, make_customer):
    mine = make_customer(alice, name="Mine")
    make_customer(bob, name="Not mine")

    response = api(alice).get("/api/customers/")

    assert response.status_code == 200
    assert [c["id"] for c in response.data["results"]] == [mine.id]


def test_staff_sees_all_customers(api, alice, bob, carol, make_customer):
    make_customer(alice)
    make_customer(bob)

    response = api(carol).get("/api/customers/")

    assert response.data["count"] == 2


def test_list_rejects_invalid_country(api, alice):
    response = api(alice).get("/api/customers/", {"country": "armenia"})

    assert response.status_code == 400


def test_detail_forbidden_for_other_manager(api, alice, bob, make_customer):
    customer = make_customer(bob)

    response = api(alice).get(f"/api/customers/{customer.id}/")

    assert response.status_code == 403


def test_requires_authentication(api):
    response = api().get("/api/customers/")

    assert response.status_code == 401
