#!/usr/bin/env python3
"""
coincidence_mc_match.py -- Monte-Carlo accidental-match probability and value
popularity, framework-agnostic.

Full enumeration (coincidence_grammars.py) stops near 7 nodes. A claim whose
witness is deeper cannot be ranked by enumeration at its own budget. This
estimator answers two budget-honest questions by sampling, each with a Wilson
95% interval:

  p_match    P( a random valid expression of the claim's own node budget K
               lands within the claim's achieved relative deviation of the
               target ). Small p = the match is hard to get by chance with a
               formula this complex; large p = the budget buys the match.

  popularity P( a random valid expression of a fixed SMALL reference budget
               (REF_NODES, default 5) lands within the same window ). This is a
               property of the target VALUE, not of the claim: it measures how
               reachable the number is with simple formulas. A value like 2/3
               has many simple representations (popularity high) even when it is
               the unique distinct value in its window; a value like 81/52 does
               not (popularity low). Distinguishing the two is the point: high
               precision plus low description length do not make a coincidence
               surprising if the target value is easy to produce.

DECLARED SAMPLING NULL (a researcher degree of freedom, journaled). A random
expression of n nodes is generated top-down: at n == 1 a leaf is drawn uniformly
from the alphabet; otherwise an operator is drawn uniformly from the allowed
unary+binary set (unary needs n >= 2, binary needs n >= 3), a binary split is
drawn uniformly in 1..n-2, and children recurse. The frozen guards apply
(integer exponents in [-4,4], no power nesting > 2, magnitude cap, domain
guards); guard-violating samples are INVALID and excluded from the denominator.
p = matches / valid. The model is not uniform over distinct trees; it is a
declared, reproducible null, and its valid-sample yield is reported.

Input: a claims JSON (list of {id, symbol, grammar, betti, target, dev_abs,
node_budget}); no claims ship with this repository. Output: per-claim p_match
and popularity with intervals. Deterministic seed.

Usage: coincidence_mc_match.py CLAIMS.json OUT.json [N_SAMPLES] [REF_NODES]
"""

import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from coincidence_grammars import (  # noqa: E402
    G_STRUCT, G_TRANS, apply_unary, apply_binary, _ok)

SEED = 20260613
DEFAULT_SAMPLES = 200_000
DEFAULT_REF_NODES = 5


def build_grammar(name, betti):
    if name == 'G_STRUCT':
        return G_STRUCT(betti=tuple(betti or ()))
    if name == 'G_TRANS':
        return G_TRANS()
    from coincidence_grammars import G_INT
    return G_INT()


class Sampler:
    def __init__(self, g, rng):
        self.rng = rng
        self.leaf_vals = list(g.leaves.values())
        self.unary = list(g.unary)
        self.binary = list(g.binary)

    def gen(self, n):
        if n == 1:
            return self.rng.choice(self.leaf_vals)
        ops = []
        if n >= 2:
            ops += [('u', op) for op in self.unary]
        if n >= 3:
            ops += [('b', op) for op in self.binary]
        kind, op = self.rng.choice(ops)
        if kind == 'u':
            c = self.gen(n - 1)
            r = None if c is None else apply_unary(op, c)
        else:
            i = self.rng.randint(1, n - 2)
            a = self.gen(i)
            b = self.gen(n - 1 - i)
            r = None if (a is None or b is None) else apply_binary(op, a, b)
        return r if (r is not None and _ok(r)) else None


def estimate(sampler, x, tol, n_nodes, n_samples):
    valid = match = 0
    for _ in range(n_samples):
        r = sampler.gen(n_nodes)
        if r is None:
            continue
        valid += 1
        if abs(r - x) <= tol:
            match += 1
    return valid, match


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    claims_path, out_path = sys.argv[1], sys.argv[2]
    n_samples = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_SAMPLES
    ref_nodes = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_REF_NODES
    with open(claims_path, encoding='utf-8') as f:
        claims = json.load(f)
    rng = random.Random(SEED)

    out = []
    print(f'{"id":<4} {"symbol":<12} {"G":<8} {"K":>3} {"reldev":>9} '
          f'{"p_match":>11} {"popularity":>11}')
    for c in claims:
        g = build_grammar(c['grammar'], c.get('betti'))
        s = Sampler(g, rng)
        x, K = c['target'], c['node_budget']
        tol = c['dev_abs']
        v1, m1 = estimate(s, x, tol, K, n_samples)
        v2, m2 = estimate(s, x, tol, ref_nodes, n_samples)
        p1 = m1 / v1 if v1 else float('nan')
        p2 = m2 / v2 if v2 else float('nan')
        lo1, hi1 = wilson(m1, v1)
        lo2, hi2 = wilson(m2, v2)
        out.append({'id': c['id'], 'symbol': c.get('symbol', c['id']),
                    'grammar': c['grammar'], 'node_budget': K,
                    'rel_dev': tol / abs(x),
                    'p_match': p1, 'p_match_ci95': [lo1, hi1],
                    'p_match_valid': v1, 'p_match_hits': m1,
                    'popularity': p2, 'popularity_ci95': [lo2, hi2],
                    'popularity_valid': v2, 'popularity_hits': m2,
                    'ref_nodes': ref_nodes})
        print(f'{c["id"]:<4} {c.get("symbol", c["id"]):<12} {c["grammar"]:<8} '
              f'{K:>3} {tol / abs(x):>9.2e} {p1:>11.3e} {p2:>11.3e}')

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'seed': SEED, 'n_samples': n_samples,
                   'ref_nodes': ref_nodes, 'rows': out}, f, indent=1,
                  ensure_ascii=False)
    print(f'\nwrote {out_path}')


if __name__ == '__main__':
    main()
