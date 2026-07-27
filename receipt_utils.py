import random


_current_receipt_number = None


def reset_receipt_number():
    global _current_receipt_number
    _current_receipt_number = None


def set_receipt_number(receipt_number):
    global _current_receipt_number
    _current_receipt_number = str(receipt_number).strip() if receipt_number is not None else None


def get_or_create_receipt_number():
    global _current_receipt_number
    if _current_receipt_number is None:
        _current_receipt_number = f"R{random.randint(0, 9999):04d}"
    return _current_receipt_number
