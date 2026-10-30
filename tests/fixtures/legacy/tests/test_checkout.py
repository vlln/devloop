import unittest
from decimal import Decimal
from src.checkout import total


class CheckoutTests(unittest.TestCase):
    def test_decimal_total(self):
        self.assertEqual(total(['0.1', '0.2']), Decimal('0.3'))

    def test_empty(self):
        self.assertEqual(total([]), Decimal('0'))


if __name__ == '__main__':
    unittest.main()
