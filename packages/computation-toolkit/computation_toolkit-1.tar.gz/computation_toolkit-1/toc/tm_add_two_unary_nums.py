def tm_add(input_str):
    input_str = input_str.replace(' ', '')
    tape = list(input_str)
    tape.append('_')
    head = 0
    state = 'S'
    
    transitions = {
        ('S', '1'): ('S', '1', 'R'),
        ('S', '+'): ('M', '1', 'R'),
        ('M', '1'): ('M', '1', 'R'),
        ('M', '_'): ('E', '_', 'L'),
        ('E', '1'): ('H', '_', 'S'),
    }
    
    while state != 'H':
        current_symbol = tape[head]
        key = (state, current_symbol)
        
        if key not in transitions:
            raise RuntimeError(f"No transition for state {state} and symbol {current_symbol}")
        
        new_state, write_symbol, direction = transitions[key]
        
        tape[head] = write_symbol
        
        if direction == 'R':
            head += 1
        elif direction == 'L':
            head -= 1

        state = new_state
    
    result = ''.join([c for c in tape if c != '_'])
    return result

if __name__ == "__main__":
    input_str = input("Enter a unary expression like 11+111: ")
    output_str = tm_add(input_str)
    print("Output:", output_str)
    print("Length:", len(output_str))