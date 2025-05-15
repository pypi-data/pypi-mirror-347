import unittest
from toc import tm_add


class TestTuringMachine(unittest.TestCase):
    def test_happy_case(self):
        self.assertEqual(tm_add("111+11"), "11111")
    
    def test_single_1_addition(self):
        self.assertEqual(tm_add("1+1"), "11")
    
    def test_empty_first_number(self):
        self.assertEqual(tm_add("+11"), "11")

    def test_empty_second_number(self):
        self.assertEqual(tm_add("111+"), "111")
    
    def test_plus_only_input(self):
        self.assertEqual(tm_add("+"), "")
    
    def test_no_plus_sign(self):
        with self.assertRaises(RuntimeError):
            tm_add("1111")
    
    def test_multiple_plus_signs(self):
        with self.assertRaises(RuntimeError):
            tm_add("11+1+1")
    
    def test_invalid_character(self):
        with self.assertRaises(RuntimeError):
            tm_add("110+1")

    def test_empty_input(self):
        with self.assertRaises(RuntimeError):
            tm_add("")

    def test_ones_with_spaces(self):
        self.assertEqual(tm_add("  111  +  111  "), "111111")


if __name__ == "__main__":
    unittest.main()