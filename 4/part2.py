import unittest
import re

class Tests(unittest.TestCase):
    def test_example1(self):
        self.assertFalse(is_valid_password("111111"))
        self.assertTrue(is_valid_password("122345"))
        self.assertFalse(is_valid_password("111123"))
        self.assertTrue(is_valid_password("112233"))
        self.assertFalse(is_valid_password("223450"))
        self.assertFalse(is_valid_password("123789"))
        self.assertFalse(is_valid_password("123444"))
        self.assertTrue(is_valid_password("111122"))


def is_valid_password(s):
    #Two adjacent digits are the same (like 22 in 122345).
    #the two adjacent matching digits are not part of a larger group of matching digits.
    even_repeated_digits = list(len(m.group()) for m in re.finditer(r'(\d)\1{1,}', s))
    if 2 not in even_repeated_digits:
        return False

    #Going from left to right, the digits never decrease
    digits = list(s)
    return digits == sorted(digits)


if __name__ == '__main__':
    #183564-657474
    valid_count = 0
    for candidate in range(183564, 657475):
        if is_valid_password(str(candidate)):
            valid_count = valid_count + 1

    print(valid_count)
