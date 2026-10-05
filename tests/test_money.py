from apps.core.money import format_cents


def test_format_cents():
    assert format_cents(12345) == "123.45"
    assert format_cents(5) == "0.05"
    assert format_cents(-250) == "-2.50"
