import unittest

from pascal_string_escape_lib import decode


class TestPlain(unittest.TestCase):
    def test_plain_passthrough(self):
        self.assertEqual(decode("Hello"), "Hello")

    def test_empty(self):
        self.assertEqual(decode(""), "")


class TestDecimalEscape(unittest.TestCase):
    def test_single_decimal(self):
        self.assertEqual(decode("#65"), "A")

    def test_decimal_zero(self):
        self.assertEqual(decode("#0"), "\x00")

    def test_chained_decimal(self):
        self.assertEqual(decode("#65#66#67"), "ABC")

    def test_decimal_mixed_with_text(self):
        self.assertEqual(decode("A#66C"), "ABC")


class TestHexEscape(unittest.TestCase):
    def test_single_hex(self):
        self.assertEqual(decode("#$41"), "A")

    def test_chained_hex(self):
        self.assertEqual(decode("#$41#$42"), "AB")

    def test_mixed_hex_and_decimal(self):
        self.assertEqual(decode("#$41#66"), "AB")

    def test_uppercase_hex(self):
        self.assertEqual(decode("#$4A"), "J")


class TestUnicode(unittest.TestCase):
    def test_three_digit_unicode(self):
        self.assertEqual(decode("#8364"), "€")

    def test_hex_four_digit_unicode(self):
        self.assertEqual(decode("#$20AC"), "€")

    def test_huge_codepoint(self):
        # 0x10FFFF is the maximum valid Unicode scalar value.
        self.assertEqual(decode("#$10FFFF"), "\U0010FFFF")


class TestQuoteDoubling(unittest.TestCase):
    def test_doubled_quote(self):
        self.assertEqual(decode("it''s"), "it's")

    def test_two_doubled_quotes(self):
        self.assertEqual(decode("a''b''c"), "a'b'c")


class TestErrors(unittest.TestCase):
    def test_dangling_hash(self):
        with self.assertRaises(ValueError):
            decode("abc#")

    def test_hash_not_followed_by_digit(self):
        with self.assertRaises(ValueError):
            decode("#x")

    def test_hash_dollar_no_hex(self):
        with self.assertRaises(ValueError):
            decode("#$")

    def test_lone_quote(self):
        with self.assertRaises(ValueError):
            decode("it's")

    def test_trailing_single_quote(self):
        with self.assertRaises(ValueError):
            decode("abc'")


if __name__ == "__main__":
    unittest.main()
