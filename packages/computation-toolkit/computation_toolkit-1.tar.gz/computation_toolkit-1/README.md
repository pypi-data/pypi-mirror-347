# Computation Toolkit - practical assignment

## P1. NFA to DFA Converter

A Python implementation of the subset construction algorithm to convert a Non-Deterministic Finite Automaton (NFA) with ε-transitions to an equivalent Deterministic Finite Automaton (DFA).

### Algorithm
- Computes ε-closures for NFA states.
- Generates DFA states, transitions, and accept states.
- Handles ε-transitions during DFA state construction.


### Usage
#### Input Format
Define your NFA as follows:
- `nfa_states`: Set of NFA states (e.g., `{'q0', 'q1', 'q2'}`).
- `nfa_alphabet`: List of symbols including `'ε'` (e.g., `['a', 'b', 'ε']`).
- `nfa_transitions`: Dictionary where keys are tuples `(state, symbol)`, and values are sets of next states. (e.g., `{
        ('q0', 'ε'): {'q1'},
        ('q1', 'a'): {'q1', 'q2'},
        ('q1', 'b'): {'q1'},
        ('q2', 'a'): {'q2'},
    }`).
- `nfa_start`: The start state (e.g., `'q0'`).
- `nfa_accept`: Set of accept states (e.g., `{'q2'}`).

#### Function Call
```python
from computation_toolkit import nfa_to_dfa

dfa_states, dfa_alphabet, dfa_transitions, dfa_start, dfa_accept = nfa_to_dfa(
    nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept
)
```

## P2. Check CFG Ambiguity given a string
A program to determine if a given string has **more than one parse tree** under a provided context-free grammar (CFG), indicating ambiguity for that string. Uses an **shift-reduce bottom up parser** to handle common sources of ambiguity.


### Algorithm
- Detects ambiguity by checking for multiple valid parse trees.
- Uses **BFS-based shift-reduce parsing** to build the parse trees.


### Usage

Specify your CFG as a dictionary where:
- **Keys** are non-terminals (e.g., `"E"`).
- **Values** are lists of productions (e.g., `[["E", "+", "E"], ["a"]]`).

Example (ambiguous arithmetic grammar):
```python
from computation_toolkit import has_multiple_parses

grammar = {
    "E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]
}
start_symbol = "E"
input_string = "a+a*a"
print(has_multiple_parses(grammar, start_symbol, input_string))
```

## P3. Turing Machine to add two uniary numbers

A Python implementation of a Turing Machine that computes the sum of two unary numbers separated by a `+` symbol.

### Algotithm
- Implements a 3-state Turing Machine (Start, MoveToEnd, EraseLast)
- Handles edge cases (empty numbers, missing separator)
- Includes error checking for invalid inputs
- Unit test coverage for all major cases

### Usage

```python
from computation_toolkit import tm_add

input_str = "111+11"
print(tm_add(input_str))
```

# Running the Tests
To run the tests, use the following command:
```bash
python -m unittest discover tests -v
```


## Author
- Ammar Khaled [GitHub](https://github.com/Ammar-Khaled) - [LinkedIn](https://www.linkedin.com/in/ammar-noor/)