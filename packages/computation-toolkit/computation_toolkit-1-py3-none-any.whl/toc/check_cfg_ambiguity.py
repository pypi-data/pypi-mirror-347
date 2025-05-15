from collections import deque

def has_multiple_parses(grammar, start_symbol, string):
    parse_trees = set()
    tokens = list(string)
    
    queue = deque([([], tokens, [])])  # Each state: (stack, remaining_input, current_tree)
    
    while queue:
        stack, input_tokens, current_tree = queue.popleft()
        
        # Base case -> Successful parse -> when stack has start_symbol, input is empty
        if not input_tokens and len(stack) == 1 and stack[0] == start_symbol:
            parse_trees.add(repr(current_tree[0]))
            if len(parse_trees) > 1:
                return True
            continue
        
        # Shift
        if input_tokens:
            next_token = input_tokens[0]
            new_stack = stack + [next_token]
            new_tree = current_tree + [next_token]
            queue.append((new_stack, input_tokens[1:], new_tree))
        
        # Reduce: Apply all matching productions
        for nt in grammar:
            for production in grammar[nt]:
                prod_len = len(production)
                if stack[-prod_len:] == production:
                    new_stack = stack[:-prod_len] + [nt]
                    subtree = (nt, current_tree[-prod_len:])

                    new_tree = current_tree[:-prod_len] + [subtree]
                    queue.append((new_stack, input_tokens, new_tree))
    
    return len(parse_trees) > 1


if __name__ == "__main__":
    ambiguous_grammar = { "E": [["E", "+", "E"], ["E", "*", "E"], ["a"]] }

    unambiguous_grammar = {
        "E": [["E", "+", "T"], ["T"]],
        "T": [["T", "*", "F"], ["F"]],
        "F": [["a"]]
    }

    start_symbol = "E"
    string = "a+a*a"

    print("First:", has_multiple_parses(ambiguous_grammar, start_symbol, string))
    print("Second:", has_multiple_parses(unambiguous_grammar, start_symbol, string))
