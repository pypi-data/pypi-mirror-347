def epsilon_closure(states, nfa_transitions):  # This function computes the epsilon closure for a set of NFA states
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if (state, 'ε') in nfa_transitions:  # Check for epsilon transitions
            for next_state in nfa_transitions[(state, 'ε')]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return frozenset(closure)  
    # I used frozenset because they are unordered and immutable/hashable, 
    # so it can be used as a key in dictionaries and elements in sets

def nfa_to_dfa(nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept):
    
    # DFA alphabet is the same as the NFA except the epsilon
    dfa_alphabet = [symb for symb in nfa_alphabet if symb != 'ε']
    
    # Initial state is the epsilon closure of NFA's start state
    initial = epsilon_closure({nfa_start}, nfa_transitions)
    
    dfa_states = set()
    dfa_transitions = {}
    dfa_start = initial
    dfa_accept = set()
    
    queue = [initial]
    dfa_states.add(initial)
    
    while queue:
        current = queue.pop(0)
        
        # Check if current state is an accept state
        if any(state in nfa_accept for state in current):
            dfa_accept.add(current)
        
        for symbol in dfa_alphabet:
            # Compute move on symbol
            move = set()
            for state in current:
                if (state, symbol) in nfa_transitions:
                    move.update(nfa_transitions[(state, symbol)])
            # Compute epsilon closure of the move
            next_state = epsilon_closure(move, nfa_transitions)
            
            # Record the transition
            dfa_transitions[(current, symbol)] = next_state
            
            # Add next_state to DFA states if new
            if next_state not in dfa_states:
                dfa_states.add(next_state)
                queue.append(next_state)
    
    return (dfa_states, dfa_alphabet, dfa_transitions, dfa_start, dfa_accept)

if __name__ == "__main__":
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

    dfa_states, dfa_alphabet, dfa_transitions, dfa_start, dfa_accept = \
    nfa_to_dfa(nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept)

    
    print("\nDFA States:")
    for state in dfa_states:
        print(f"  {set(state)}")  # I converted the frozenset to set just for readability


    print("\nDFA Transitions:")
    for (from_state, symbol), to_state in dfa_transitions.items():
        print(f"  ({set(from_state)}, '{symbol}') -> {set(to_state)}")

    print("\nDFA Start State:")
    print(f"  {set(dfa_start)}")

    print("\nDFA Accept States:")
    for state in dfa_accept:
        print(f"  {set(state)}")