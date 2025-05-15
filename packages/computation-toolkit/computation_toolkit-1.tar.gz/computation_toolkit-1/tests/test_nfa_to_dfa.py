import unittest
from toc import nfa_to_dfa, epsilon_closure


class TestNFAtoDFA(unittest.TestCase):
    def test_epsilon_closure_without_epsilon_transition(self):
        closure = epsilon_closure({'q0'}, {('q0', 'a'): {'q0'}})
        self.assertEqual(closure, frozenset({'q0'}))

    def test_epsilon_closure_with_epsilon_transition(self):
        closure = epsilon_closure({'q0'}, {('q0', 'ε'): {'q1'}})
        self.assertEqual(closure, frozenset({'q0', 'q1'}))

    def test_epsilon_closure_with_mutliple_epsilons(self):
        closure = epsilon_closure({'q0'}, {('q0', 'ε'): {'q0'}, ('q0', 'ε'): {'q1'}})
        self.assertEqual(closure, frozenset({'q0', 'q1'}))

    def test_the_example(self):
        nfa_states = {'q0', 'q1', 'q2'}
        nfa_alphabet = ['a', 'b', 'ε']
        nfa_transitions = {
            ('q0', 'ε'): {'q1'},
            ('q1', 'a'): {'q1', 'q2'},
            ('q1', 'b'): {'q1'},
            ('q2', 'a'): {'q2'},
        }
        nfa_start = 'q0'
        nfa_accept = {'q2'}

        dfa_states, dfa_alphabet, dfa_trans, dfa_start, dfa_accept = nfa_to_dfa(
            nfa_states, nfa_alphabet, nfa_transitions,
            nfa_start, nfa_accept
        )

        expected_states = {
            frozenset({'q0', 'q1'}),
            frozenset({'q1', 'q2'}),
            frozenset({'q1'})
        }
        self.assertEqual(dfa_states, expected_states)

        start_state = frozenset({'q0', 'q1'})
        self.assertEqual(dfa_trans[(start_state, 'a')], frozenset({'q1', 'q2'}))
        self.assertEqual(dfa_trans[(start_state, 'b')], frozenset({'q1'}))

        self.assertEqual(dfa_accept, {frozenset({'q1', 'q2'})})

    def test_nfa_without_epsilon(self):
        nfa_states = {'q0', 'q1'}
        nfa_alphabet = ['a', 'b']
        nfa_transitions = {
            ('q0', 'a'): {'q1'},
            ('q0', 'b'): {'q0'},
            ('q1', 'a'): {'q1'},
            ('q1', 'b'): {'q0'},
        }
        nfa_start = 'q0'
        nfa_accept = {'q1'}

        dfa_states, _, dfa_trans, dfa_start, dfa_accept = nfa_to_dfa(
            nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept
        )

        self.assertEqual(dfa_states, {frozenset({'q0'}), frozenset({'q1'})})
        self.assertEqual(dfa_start, frozenset({'q0'}))
        self.assertEqual(dfa_accept, {frozenset({'q1'})})


if __name__ == '__main__':
    unittest.main()