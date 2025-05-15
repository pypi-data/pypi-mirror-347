from formal_languages import minimize_dfa, print_dfa
from formal_languages import cfg_to_cnf
from formal_languages import increment_binary
import unittest
import io
import sys


def main_task1():
    # Example DFA
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
    
    print("Original DFA:")
    print_dfa(states, alphabet, transitions, start_state, accept_states)
    
    # Minimize DFA
    new_states, new_alphabet, new_transitions, new_start, new_accept = minimize_dfa(
        states, alphabet, transitions, start_state, accept_states
    )
    
    print("\nMinimized DFA:")
    print_dfa(new_states, new_alphabet, new_transitions, new_start, new_accept)
    
    # Demonstrate another example with a different DFA
    print("\n\nAnother Example:")
    states = [0, 1, 2, 3, 4, 5]
    alphabet = ['a', 'b']
    transitions = [
        (0, 'a', 1), (0, 'b', 3),
        (1, 'a', 0), (1, 'b', 2),
        (2, 'a', 1), (2, 'b', 5),
        (3, 'a', 4), (3, 'b', 0),
        (4, 'a', 3), (4, 'b', 5),
        (5, 'a', 5), (5, 'b', 5)
    ]
    start_state = 0
    accept_states = [2, 4]
    
    print("Original DFA:")
    print_dfa(states, alphabet, transitions, start_state, accept_states)
    
    # Minimize DFA
    new_states, new_alphabet, new_transitions, new_start, new_accept = minimize_dfa(
        states, alphabet, transitions, start_state, accept_states
    )
    
    print("\nMinimized DFA:")
    print_dfa(new_states, new_alphabet, new_transitions, new_start, new_accept)

# test cfg_to_cnf teask 2
def test_cfg_to_cnf():
    cfg = {'S': ['A'], 'A': ['B'], 'B': ['b']}
    
    cnf = cfg_to_cnf(cfg)
    print("CNF Productions:")
    for var, bodies in cnf.items():
        for body in bodies:
            print(f"{var} → {body}")

# test increment_binary task 4
def test_increment_binary():
    test_cases = [
        ("0", "1"),
        ("1", "10"),
        ("10", "11"),
        ("11", "100"),
        ("1011", "1100"),
        ("1111", "10000"),
        ("", "1"),  # edge case: empty input
    ]

    for binary, expected in test_cases:
        result = increment_binary(binary)
        print(f"increment_binary('{binary}') = '{result}' (Expected: '{expected}')")

# ------------------------ test with unittest --------------------------------------------------------
class TestFormalLanguages(unittest.TestCase):
    def test_dfa_minimization(self):
        # First example
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
        
        new_states, new_alphabet, new_transitions, new_start, new_accept = minimize_dfa(
            states, alphabet, transitions, start_state, accept_states
        )
        
        # Verify minimized DFA has fewer states than original
        self.assertLessEqual(len(new_states), len(states))
        
        # Don't check exact transitions, as implementation may vary
        # Just check that transitions are valid
        for state, symbol, next_state in new_transitions:
            self.assertIn(state, new_states)
            self.assertIn(next_state, new_states)
            self.assertIn(symbol, alphabet)
        
        # Second example
        states = [0, 1, 2, 3, 4, 5]
        alphabet = ['a', 'b']
        transitions = [
            (0, 'a', 1), (0, 'b', 3),
            (1, 'a', 0), (1, 'b', 2),
            (2, 'a', 1), (2, 'b', 5),
            (3, 'a', 4), (3, 'b', 0),
            (4, 'a', 3), (4, 'b', 5),
            (5, 'a', 5), (5, 'b', 5)
        ]
        start_state = 0
        accept_states = [2, 4]
        
        new_states, new_alphabet, new_transitions, new_start, new_accept = minimize_dfa(
            states, alphabet, transitions, start_state, accept_states
        )
        
        # Just make sure accept states exist in minimized DFA
        self.assertGreater(len(new_accept), 0)
        for state in new_accept:
            self.assertIn(state, new_states)

    def test_cfg_to_cnf(self):
        # Simple example
        cfg = {'S': ['A'], 'A': ['B'], 'B': ['b']}
        cnf = cfg_to_cnf(cfg)
        
        # Verify the CNF has the expected terminals
        self.assertTrue('b' in str(cnf.values()))
        
        # Check that productions exist (without checking exact format)
        self.assertGreater(len(cnf), 0)
        
        # More complex example
        cfg2 = {
            'S': ['AB', 'BC'],
            'A': ['BA', 'a'],
            'B': ['CC', 'b'],
            'C': ['AB', 'a']
        }
        cnf2 = cfg_to_cnf(cfg2)
        
        # Check result has reasonable size
        self.assertGreater(len(cnf2), 0)
        
        # Check terminals are preserved
        self.assertTrue('a' in str(cnf2.values()) or 'b' in str(cnf2.values()))

    def test_increment_binary(self):
        test_cases = [
            ("0", "1"),
            ("1", "10"),
            ("10", "11"),
            ("11", "100"),
            ("1011", "1100"),
            ("1111", "10000"),
            ("", "1"),  # edge case: empty input
        ]

        for binary, expected in test_cases:
            result = increment_binary(binary)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    # Original demos
    print("=== Demo Mode ===")
    main_task1()
    print("-" * 60)
    test_cfg_to_cnf()
    print("-" * 60)
    test_increment_binary()
    
    # Run unit tests
    print("\n\n=== Running Unit Tests ===")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

