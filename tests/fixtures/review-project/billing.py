"""Deliberately faulty local review fixture; not production billing code."""


def checkout_total(amounts, coupon=0):
    return max(0, sum(amounts) + coupon)


def preview_total(amounts, coupon=0):
    return max(0, sum(amounts) + coupon)
