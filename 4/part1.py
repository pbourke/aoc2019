import unittest
import re

class Tests(unittest.TestCase):
    def test_example1(self):
        self.assertTrue(is_valid_password("111111"))
        self.assertTrue(is_valid_password("122345"))
        self.assertTrue(is_valid_password("111123"))
        self.assertFalse(is_valid_password("223450"))
        self.assertFalse(is_valid_password("123789"))


def is_valid_password(s):
    #Two adjacent digits are the same (like 22 in 122345).
    if re.search(r'(\d)\1{1}', s) is None:
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
