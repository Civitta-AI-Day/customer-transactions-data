"""Money helpers.

Convention: money is always stored and passed around as integer cents.
Convert to a decimal string only at the edge (API output, CSV, UI).
"""

from decimal import Decimal


def format_cents(amount_cents: int) -> str:
    """Return a cents amount as a string with exactly 2 decimals, e.g. 12345 -> "123.45"."""
    return f"{Decimal(amount_cents) / 100:.2f}"
