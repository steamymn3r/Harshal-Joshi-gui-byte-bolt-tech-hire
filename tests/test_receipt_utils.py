import unittest

from receipt_utils import get_or_create_receipt_number, reset_receipt_number, set_receipt_number


class ReceiptUtilsTests(unittest.TestCase):
    def setUp(self):
        reset_receipt_number()

    def test_reuses_same_receipt_number_until_reset(self):
        first = get_or_create_receipt_number()
        second = get_or_create_receipt_number()

        self.assertEqual(first, second)

    def test_can_override_receipt_number(self):
        set_receipt_number("R1234")
        self.assertEqual(get_or_create_receipt_number(), "R1234")


if __name__ == "__main__":
    unittest.main()
