from django.test import TestCase
from library.helpers import *


class BookPrefixTest(TestCase):
    def test_book_prefix_check(self):
        tests = [("AA4", "AA4"),
                 ("CA4", "CA4"),
                 ("AA45", "AA45"),
                 ("AA4 ", "AA4"),
                 ("A4 ", False),
                 ("4AA ", False),
                 ("33 ", False),
                 ("FG33A ", False),
                 ("FG33 a ", False),
                 ]
        for test_str, expected in tests:
            if not expected:
                with self.assertRaises(ValueError):
                    validate_book_prefix(test_str)
            else:
                self.assertEquals(validate_book_prefix(test_str), expected)
