"""
This module provides functionality for working with Context-Free Grammars (CFG).
"""

def cfg_to_cnf(cfg):
    """
    Convert a Context-Free Grammar (CFG) to Chomsky Normal Form (CNF).
    
    Args:
        cfg (dict): A dictionary representing the CFG where keys are variables (non-terminals)
                   and values are lists of production bodies.
                   
    Returns:
        dict: A new dictionary representing the grammar in CNF form.
    """
    productions = dict(cfg)
    new_prods = {}
    var_count = 1

    # Step 1: Add new start symbol
    new_prods['S0'] = ['S']
    productions['S0'] = ['S']

    # Step 2: Eliminate epsilon productions
    nullable = set()
    for var, bodies in productions.items():
        if 'epsilon' in bodies:
            nullable.add(var)
            bodies.remove('epsilon')

    for var, bodies in list(productions.items()):
        new_bodies = bodies.copy()
        for body in bodies:
            if any(c in nullable for c in body):
                for i in range(1, 1 << len(body)):
                    new_body = ''.join(c for j, c in enumerate(body) if i & (1 << j))
                    if new_body:
                        new_bodies.append(new_body)
        productions[var] = new_bodies

    # Step 3: Eliminate unit productions
    for var in productions:
        bodies = productions[var]
        i = 0
        while i < len(bodies):
            body = bodies[i]
            if len(body) == 1 and body in productions:
                bodies.extend(productions[body])
                bodies.pop(i)
            else:
                i += 1

    # Step 4: Convert to CNF
    for var, bodies in productions.items():
        new_prods.setdefault(var, [])
        for body in bodies:
            if len(body) == 1 and not body.isupper():
                new_prods[var].append(body)
            elif len(body) == 2 and body.isupper():
                new_prods[var].append(body)
            else:
                temp = list(body)
                # Replace terminals
                for i, c in enumerate(temp):
                    if not c.isupper():
                        new_var = f'X{var_count}'
                        var_count += 1
                        new_prods[new_var] = [c]
                        temp[i] = new_var
                # Break long productions
                while len(temp) > 2:
                    new_var = f'X{var_count}'
                    var_count += 1
                    new_prods[new_var] = temp[:2]
                    temp = [new_var] + temp[2:]
                new_prods[var].append(''.join(temp))

    return new_prods 