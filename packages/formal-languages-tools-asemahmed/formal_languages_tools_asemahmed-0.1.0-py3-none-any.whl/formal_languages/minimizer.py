def minimize_dfa(states, alphabet, transitions, start_state, accept_states):
    """
    Minimizes a deterministic finite automaton (DFA) using partition refinement.
    
    Args:
        states: List of states in the DFA
        alphabet: List of symbols in the alphabet
        transitions: List of tuples (state, symbol, next_state)
        start_state: The initial state of the DFA
        accept_states: List of accepting states
        
    Returns:
        A tuple containing (new_states, alphabet, new_transitions, new_start, new_accept)
    """
    # Initialize partitions: accepting and non-accepting states
    non_accept = [s for s in states if s not in accept_states]
    partitions = [accept_states, non_accept] if non_accept else [accept_states]
    
    # Create transition lookup dictionary for efficiency
    trans_dict = {(s, a): t for s, a, t in transitions}
    
    # Partition refinement loop
    while True:
        new_partitions = []
        changed = False
        
        for partition in partitions:
            # Group states by their transition behavior
            groups = {}
            for state in partition:
                # Create a signature for the state based on where it goes for each symbol
                signature = tuple(
                    next((i for i, p in enumerate(partitions) if trans_dict.get((state, a)) in p), -1)
                    for a in alphabet
                )
                if signature not in groups:
                    groups[signature] = []
                groups[signature].append(state)
            
            # Add new groups to new_partitions
            for group in groups.values():
                new_partitions.append(group)
                if len(group) < len(partition) and len(groups) > 1:
                    changed = True
        
        partitions = new_partitions
        if not changed:
            break
    
    # Build minimized DFA
    # Create new state names (use index of partition)
    state_map = {s: i for i, p in enumerate(partitions) for s in p}
    
    # New transitions
    new_transitions = []
    for s, a, t in transitions:
        if (state_map[s], a, state_map[t]) not in new_transitions:
            new_transitions.append((state_map[s], a, state_map[t]))
    
    # New start and accept states
    new_start = state_map[start_state]
    new_accept = list(set(state_map[s] for s in accept_states))
    
    # New states
    new_states = list(range(len(partitions)))
    
    return new_states, alphabet, new_transitions, new_start, new_accept 