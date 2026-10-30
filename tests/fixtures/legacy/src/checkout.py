from decimal import Decimal


def total(amounts):
    return sum((Decimal(value) for value in amounts), Decimal('0'))
