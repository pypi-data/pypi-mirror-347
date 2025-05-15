"""
This module provides implementations of various Turing machines.
"""

def increment_binary(binary):
    """
    Implements a Turing machine that increments a binary number by 1.
    
    The machine works by:
    1. Starting from the rightmost digit
    2. Converting 1s to 0s and moving left until finding a 0 or blank
    3. Converting that 0 or blank to 1 and halting
    
    Args:
        binary (str): A binary number as a string (e.g., "1011")
                     Empty string is treated as 0.
    
    Returns:
        str: The input number plus 1 in binary (e.g., "1100" for input "1011")
    
    Examples:
        >>> increment_binary("0")
        "1"
        >>> increment_binary("1")
        "10"
        >>> increment_binary("1011")
        "1100"
        >>> increment_binary("")  # Treated as 0
        "1"
    """
    tape = list('b' + binary + 'b')  # Tape with blanks
    head = len(tape) - 2  # Point to last binary digit
    state = 'q0'  # Initial state
    transitions = {
        ('q0', '1'): ('q0', '0', 'L'),  # Flip 1 to 0, move left
        ('q0', '0'): ('qf', '1', 'S'),  # Flip 0 to 1, halt
        ('q0', 'b'): ('qf', '1', 'S'),  # Write 1 on blank, halt
    }
    
    while state != 'qf':
        if head < 0:
            tape.insert(0, 'b')
            head = 0
        if head >= len(tape):
            tape.append('b')
        symbol = tape[head]
        if (state, symbol) not in transitions:
            break
        new_state, write_symbol, move = transitions[(state, symbol)]
        tape[head] = write_symbol
        state = new_state
        if move == 'L':
            head -= 1
        elif move == 'R':
            head += 1
        # 'S' means stay (halt)
    
    return ''.join(tape).strip('b') 