from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Minisat22

def var_id(cell):
    return cell[0] * 9 + cell[1] + 1

def encode_equals(cnf, vars_list, k):
    """Encode Σ vars_list == k into CNF"""
    n = len(vars_list)

    # At most k  → every (k+1)-subset cannot all be true
    for combo in combinations(vars_list, k+1):
        cnf.append([-v for v in combo])

    # At least k → every (n-k+1)-subset must include at least one true
    for combo in combinations(vars_list, n-k+1):
        cnf.append(list(combo))

def normalize(test1):
    if len(test1) == 1 and isinstance(test1[0], list):
        test1 = test1[0]
    
    fixed = []
    for clause in test1:
        *coords, val = clause
        coords = [tuple(c) for c in coords]
        fixed.append((tuple(coords), val))
    return fixed

def custom_sat(test1):

    raw_clauses = normalize(test1)

    # collect all variables
    all_cells = sorted({cell for group,_ in raw_clauses for cell in group})
    mapping = {cell: var_id(cell) for cell in all_cells}

    # ---- Build CNF object ----
    cnf = CNF()

    for group, val in raw_clauses:
        encoded_vars = [mapping[cell] for cell in group]
        encode_equals(cnf, encoded_vars, val)

    # ---- Solve base CNF ----
    solver = Minisat22(bootstrap_with=cnf.clauses)
    sat = solver.solve()
    print("\nSAT:", sat)

    if not sat:
        print("UNSAT - Constraints contradict.")
    # ---- Infer each variable ----
    results = {}
    for cell, vid in mapping.items():
        # check if vid = 1 is possible
        s1 = Minisat22(bootstrap_with=cnf.clauses)
        s1.add_clause([vid])
        mine_possible = s1.solve()
        # check if vid = 0 is possible
        s2 = Minisat22(bootstrap_with=cnf.clauses)
        s2.add_clause([-vid])
        safe_possible = s2.solve()
        if mine_possible and not safe_possible:
            results[cell] = 1   # forced mine
        elif safe_possible and not mine_possible:
            results[cell] = 0   # forced safe
        else:
            results[cell] = -1  # ambiguous

    print("\nFinal Inference:")
    for k in sorted(results):
        print(k, "→", results[k])

    return results
