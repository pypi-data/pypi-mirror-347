import unittest
from toc import has_multiple_parses


class TestHasMutlipleParses(unittest.TestCase):
    def test_ambiguous_grammar(self):
        ambiguous_grammar = {
            "E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]
        }
        start_symbol = "E"
        string = "a+a*a"
        self.assertTrue(has_multiple_parses(ambiguous_grammar, start_symbol, string))

    def test_unambiguous_grammar(self):
        unambiguous_grammar = {
            "E": [["E", "+", "T"], ["T"]],
            "T": [["T", "*", "F"], ["F"]],
            "F": [["a"]]
        }
        start_symbol = "E"
        string = "a+a*a"
        self.assertFalse(has_multiple_parses(unambiguous_grammar, start_symbol, string))

    def test_empty_string(self):
        ambiguous_grammar = {
            "E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]
        }
        start_symbol = "E"
        string = ""
        self.assertFalse(has_multiple_parses(ambiguous_grammar, start_symbol, string))

    def test_single_token(self):
        ambiguous_grammar = {
            "E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]
        }
        start_symbol = "E"
        string = "a"
        self.assertFalse(has_multiple_parses(ambiguous_grammar, start_symbol, string))


    def test_no_grammar(self):
        ambiguous_grammar = {}
        start_symbol = "E"
        string = "a+a*a"
        self.assertFalse(has_multiple_parses(ambiguous_grammar, start_symbol, string))

    def test_no_start_symbol(self):
        ambiguous_grammar = {
            "E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]
        }
        start_symbol = ""
        string = "a+a*a"
        self.assertFalse(has_multiple_parses(ambiguous_grammar, start_symbol, string))


if __name__ == "__main__":
    unittest.main()