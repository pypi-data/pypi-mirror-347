# Formal Languages Tools
- name: Asem Ahmed Mohamed Abdallah
- section: 3
- id: 4494
This package provides tools for working with formal languages, automata, and grammars.

## Features

- DFA Minimization - Minimize deterministic finite automata using partition refinement
- CFG to CNF Conversion - Convert context-free grammars to Chomsky Normal Form
- Turing Machine Simulation - Simple Turing machine for binary operations

## Installation

```bash
pip install -e .
```

## Usage

### DFA Minimization

```python
from formal_languages import minimize_dfa, print_dfa

# Define your DFA
states = [0, 1, 2, 3, 4]
alphabet = ['a', 'b']
transitions = [
    (0, 'a', 1), (0, 'b', 2),
    (1, 'a', 1), (1, 'b', 3),
    (2, 'a', 1), (2, 'b', 2),
    (3, 'a', 1), (3, 'b', 4),
    (4, 'a', 1), (4, 'b', 2)
]
start_state = 0
accept_states = [4]

# Minimize the DFA
new_states, new_alphabet, new_transitions, new_start, new_accept = minimize_dfa(
    states, alphabet, transitions, start_state, accept_states
)

# Display the results
print_dfa(new_states, new_alphabet, new_transitions, new_start, new_accept)
```

### CFG to CNF Conversion

```python
from formal_languages import cfg_to_cnf

# Define your CFG
cfg = {'S': ['A'], 'A': ['B'], 'B': ['b']}

# Convert to CNF
cnf = cfg_to_cnf(cfg)

# Display the results
for var, bodies in cnf.items():
    for body in bodies:
        print(f"{var} → {body}")
```

### Binary Incrementer (Turing Machine)

```python
from formal_languages import increment_binary

# Increment a binary number
result = increment_binary("1011")  # Returns "1100"
print(result)
```

## Package Structure

- `formal_languages/` - Main package directory
  - `minimizer.py` - DFA minimization algorithms
  - `grammar.py` - Grammar conversions and operations
  - `turing.py` - Turing machine implementations
  - `utils.py` - Utility functions

## Example Usage

See `example.py` for complete usage examples of the formal languages tools.

## License

MIT 
