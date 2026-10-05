"""Seed the local database with realistic fake data.

    python manage.py seed                      # 200,000 transactions (default)
    python manage.py seed --transactions 50000 # smaller, faster
    python manage.py seed --reset              # wipe existing data first

The data is deterministic (fixed random seed), so everyone gets the same database.
"""

import random
import time
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.audit.models import AuditLog
from apps.customers.models import Customer
from apps.transactions.models import Transaction

USERS = [
    # username, is_staff, API token
    ("alice", False, "alice-token"),
    ("bob", False, "bob-token"),
    ("carol", True, "carol-token"),
]

COMPANY_WORDS = [
    "Acme",
    "Ararat",
    "Nordic",
    "Blue",
    "Silver",
    "Cedar",
    "Summit",
    "Harbor",
    "Atlas",
    "Orion",
    "Vertex",
    "Granite",
    "Lumen",
    "Pioneer",
    "Sevan",
    "Delta",
    "Echo",
    "Maple",
    "Quantum",
    "Zenith",
]
COMPANY_SUFFIXES = ["Logistics", "Trading", "Foods", "Labs", "Travel", "Energy", "Retail", "Studio"]
COUNTRIES = ["AM", "DE", "EE", "FR", "GB", "LT", "NL", "US"]
CURRENCIES = ["EUR"] * 6 + ["USD"] * 3 + ["AMD"]
TYPE_WEIGHTS = [("payment", 70), ("refund", 10), ("transfer", 15), ("fee", 5)]
STATUS_WEIGHTS = [("completed", 85), ("pending", 10), ("failed", 5)]

NUM_CUSTOMERS = 300
BIG_CUSTOMER_SHARE = 0.3  # customer #1 gets 30% of all transactions
BATCH_SIZE = 5000


class Command(BaseCommand):
    help = "Seed users, customers and transactions with deterministic fake data."

    def add_arguments(self, parser):
        parser.add_argument("--transactions", type=int, default=200_000)
        parser.add_argument("--reset", action="store_true", help="Delete existing data first")

    def handle(self, *args, transactions, reset, **options):
        started = time.monotonic()
        rng = random.Random(42)

        if Transaction.objects.exists() and not reset:
            self.stdout.write(self.style.WARNING("Data already exists. Use --reset to re-seed."))
            return
        if reset:
            self._reset()

        users = self._create_users()
        customers = self._create_customers(rng, users)
        self._create_transactions(rng, customers, transactions)

        took = time.monotonic() - started
        self.stdout.write(self.style.SUCCESS(f"\nSeeded in {took:.1f}s.\n"))
        self._print_summary(customers)

    def _reset(self):
        self.stdout.write("Deleting existing data...")
        AuditLog.objects.all().delete()
        Transaction.objects.all().delete()
        Customer.objects.all().delete()
        Token.objects.all().delete()
        get_user_model().objects.filter(username__in=[u[0] for u in USERS]).delete()

    def _create_users(self):
        User = get_user_model()
        users = {}
        for username, is_staff, token in USERS:
            user = User.objects.create_user(
                username=username,
                password="workshop",
                is_staff=is_staff,
                email=f"{username}@example.com",
            )
            Token.objects.create(user=user, key=token)
            users[username] = user
        return users

    def _create_customers(self, rng, users):
        managers = [users["alice"], users["bob"]]
        customers = []
        for i in range(NUM_CUSTOMERS):
            if i == 0:
                name = "Acme Logistics"
            else:
                name = f"{rng.choice(COMPANY_WORDS)} {rng.choice(COMPANY_SUFFIXES)} {i}"
            customers.append(
                Customer(
                    name=name,
                    email=f"billing{i}@example.com",
                    country=rng.choice(COUNTRIES),
                    account_manager=managers[i % 2],  # even ids -> alice, odd -> bob
                )
            )
        Customer.objects.bulk_create(customers)
        self.stdout.write(f"Created {len(customers)} customers.")
        return list(Customer.objects.order_by("id"))

    def _create_transactions(self, rng, customers, total):
        now = timezone.now()
        big = customers[0]
        others = customers[1:]
        types, type_w = zip(*TYPE_WEIGHTS, strict=True)
        statuses, status_w = zip(*STATUS_WEIGHTS, strict=True)

        batch = []
        with transaction.atomic():
            for i in range(total):
                customer = big if rng.random() < BIG_CUSTOMER_SHARE else rng.choice(others)
                tx_type = rng.choices(types, type_w)[0]
                amount = rng.randint(100, 500_000)  # 1.00 to 5,000.00
                if tx_type in ("refund", "fee"):
                    amount = -amount
                batch.append(
                    Transaction(
                        customer=customer,
                        type=tx_type,
                        amount_cents=amount,
                        currency=rng.choice(CURRENCIES),
                        status=rng.choices(statuses, status_w)[0],
                        reference=f"TX-{i + 1:08d}",
                        created_at=now - timedelta(minutes=rng.randint(0, 3 * 365 * 24 * 60)),
                    )
                )
                if len(batch) == BATCH_SIZE:
                    Transaction.objects.bulk_create(batch)
                    batch.clear()
                    self.stdout.write(f"  {i + 1:,} / {total:,} transactions", ending="\r")
            if batch:
                Transaction.objects.bulk_create(batch)
        self.stdout.write(f"Created {total:,} transactions.            ")

    def _print_summary(self, customers):
        big = customers[0]
        self.stdout.write("Users (password for all: workshop)")
        self.stdout.write("  alice  token: alice-token  account manager, even customer ids")
        self.stdout.write("  bob    token: bob-token    account manager, odd customer ids")
        self.stdout.write("  carol  token: carol-token  staff, sees every customer")
        self.stdout.write(
            f"\nBiggest customer: #{big.id} {big.name} "
            f"({big.transactions.count():,} transactions, managed by alice)"
        )
        self.stdout.write("\nTry it:")
        self.stdout.write(
            '  curl -H "Authorization: Token alice-token" '
            "http://127.0.0.1:8000/api/customers/1/transactions/"
        )
