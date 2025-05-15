def print_dfa(states, alphabet, transitions, start_state, accept_states):
    """
    Prints a DFA in a readable format.
    
    Args:
        states: List of states in the DFA
        alphabet: List of symbols in the alphabet
        transitions: List of tuples (state, symbol, next_state)
        start_state: The initial state of the DFA
        accept_states: List of accepting states
    """
    print("States:", states)
    print("Alphabet:", alphabet)
    print("Transitions:", transitions)
    print("Start state:", start_state)
    print("Accept states:", accept_states)


def transitions_to_table(states, alphabet, transitions):
    """
    Converts transitions to a transition table format.
    
    Args:
        states: List of states in the DFA
        alphabet: List of symbols in the alphabet
        transitions: List of tuples (state, symbol, next_state)
        
    Returns:
        A dictionary mapping (state, symbol) to next_state
    """
    return {(s, a): t for s, a, t in transitions}


def table_to_transitions(table, states, alphabet):
    """
    Converts a transition table back to a list of transitions.
    
    Args:
        table: A dictionary mapping (state, symbol) to next_state
        states: List of states in the DFA
        alphabet: List of symbols in the alphabet
        
    Returns:
        List of tuples (state, symbol, next_state)
    """
    transitions = []
    for state in states:
        for symbol in alphabet:
            if (state, symbol) in table:
                transitions.append((state, symbol, table[(state, symbol)]))
    return transitions 