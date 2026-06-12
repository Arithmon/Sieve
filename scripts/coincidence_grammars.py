#!/usr/bin/env python3
"""
coincidence_grammars.py -- the expression-space engine (M2).

Implements the three grammars and two complexity measures exactly as frozen
in freeze/GRAMMARS_FREEZE.md (v1.0, DOI 10.5281/zenodo.20666879):

- G_INT:    integers 1..9; ops {+, -, *, /, ^, sqrt, inv, sq}
- G_STRUCT: dims + ranks of compact simple Lie groups of rank <= 8, Betti
            numbers of the framework-declared manifold family (parameter),
            integers 1..9; same ops
- G_TRANS:  G_INT alphabet + {pi, e, phi, gamma, ln2, zeta(3..11 odd)};
            ops + {log}

Complexity measures:
- kappa_MDL:  cost(leaf) = log2 |A|, cost(op) = log2 |O|, summed over the tree
- kappa_NODE: node count

Anti-gaming guards (freeze section 4): integer exponents in [-4, 4] only, no
nested powers deeper than 2, domain guards, canonicalization by VALUE so the
trials factor counts distinct values rather than syntax trees.

Enumeration: dynamic programming over node count. Level n holds a map
{canonical value -> (min kappa_MDL, witness expression)}. The witness with
minimal MDL is kept per value; ties resolved arbitrarily (the count, not the
witness, is the deliverable).

DISCIPLINE NOTE: this module evaluates expressions and enumerates expression
spaces. Nothing in this file reads the frozen observable values; matching
against the frozen list is only allowed because the freeze is deposited
(v1.0, 2026-06-12). All M2 calibration runs use synthetic targets.
"""

import math
from dataclasses import dataclass, field

SIG_DIGITS = 12          # value canonicalization for dedup
MAG_CAP = 1e12           # magnitude guard (and 1/MAG_CAP below)
EXP_RANGE = (-4, 4)      # integer exponents allowed for ^


def _zeta(s, terms=200_000):
    return sum(1.0 / k ** s for k in range(1, terms))


def lie_alphabet(max_rank=8):
    """Dims + ranks of compact simple Lie groups of rank <= max_rank (D9 rule).
    Conventions: A_n n>=1, B_n n>=2, C_n n>=3, D_n n>=4, plus G2 F4 E6 E7 E8."""
    a = {}
    for n in range(1, max_rank + 1):
        a[f'dim_A{n}'] = n * (n + 2)
    for n in range(2, max_rank + 1):
        a[f'dim_B{n}'] = n * (2 * n + 1)
    for n in range(3, max_rank + 1):
        a[f'dim_C{n}'] = n * (2 * n + 1)
    for n in range(4, max_rank + 1):
        a[f'dim_D{n}'] = n * (2 * n - 1)
    a.update({'dim_G2': 14, 'dim_F4': 52, 'dim_E6': 78, 'dim_E7': 133,
              'dim_E8': 248})
    for r in range(1, max_rank + 1):
        a[f'rank_{r}'] = r
    return a


@dataclass
class Grammar:
    name: str
    leaves: dict                      # name -> float value
    unary: tuple = ('sqrt', 'inv', 'sq')
    binary: tuple = ('+', '-', '*', '/', '^')

    @property
    def n_ops(self):
        return len(self.unary) + len(self.binary)

    def leaf_cost(self):
        return math.log2(len(self.leaves))

    def op_cost(self):
        return math.log2(self.n_ops)


def G_INT():
    return Grammar('G_INT', {str(i): float(i) for i in range(1, 10)})


def G_STRUCT(betti=()):
    """betti: the framework-declared manifold family's Betti numbers,
    e.g. (21, 77) for the GIFT case study. Empty for synthetic work."""
    leaves = {str(i): float(i) for i in range(1, 10)}
    leaves.update({k: float(v) for k, v in lie_alphabet().items()})
    for i, b in enumerate(betti):
        leaves[f'betti_{i}'] = float(b)
    return Grammar('G_STRUCT', leaves)


def G_TRANS():
    leaves = {str(i): float(i) for i in range(1, 10)}
    leaves.update({'pi': math.pi, 'e': math.e,
                   'phi': (1 + math.sqrt(5)) / 2,
                   'gamma': 0.5772156649015329, 'ln2': math.log(2)})
    for s in (3, 5, 7, 9, 11):
        leaves[f'zeta{s}'] = _zeta(s)
    return Grammar('G_TRANS', leaves,
                   unary=('sqrt', 'inv', 'sq', 'log'))


# ---------------------------------------------------------------------------
# guarded evaluation
# ---------------------------------------------------------------------------

def _ok(v):
    return v is not None and math.isfinite(v) and 1 / MAG_CAP < abs(v) < MAG_CAP


def apply_unary(op, v):
    try:
        if op == 'sqrt':
            return math.sqrt(v) if v > 0 else None
        if op == 'inv':
            return 1.0 / v if v != 0 else None
        if op == 'sq':
            return v * v
        if op == 'log':
            return math.log(v) if v > 0 else None
    except (OverflowError, ValueError):
        return None
    raise ValueError(op)


def apply_binary(op, a, b):
    try:
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            return a / b if b != 0 else None
        if op == '^':
            # guard: integer exponents in EXP_RANGE only, no 0^0, base > 0
            # for non-integer-safe cases handled by float pow on positive base
            n = round(b)
            if abs(b - n) > 1e-9 or not (EXP_RANGE[0] <= n <= EXP_RANGE[1]):
                return None
            if n == 0:
                return None if a == 0 else 1.0
            if a == 0 and n < 0:
                return None
            return float(a ** n)
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    raise ValueError(op)


def canon(v):
    """Canonical dedup key: round to SIG_DIGITS significant digits."""
    return float(f'%.{SIG_DIGITS}g' % v)


# ---------------------------------------------------------------------------
# enumeration by node count, min-MDL witness per distinct value
# ---------------------------------------------------------------------------

@dataclass
class Level:
    """values: canonical value -> (min_mdl, expr_string, power_depth)."""
    values: dict = field(default_factory=dict)


def enumerate_values(g, max_nodes, log=print):
    """E(g, k) organized by node count. Returns list levels[1..max_nodes]
    where levels[n] maps canonical value -> (min_mdl, expr, pdepth).
    pdepth tracks nesting of '^' to enforce the depth-2 guard."""
    lc, oc = g.leaf_cost(), g.op_cost()
    levels = {n: {} for n in range(1, max_nodes + 1)}

    def put(n, v, mdl, expr, pdepth):
        cv = canon(v)
        cur = levels[n].get(cv)
        if cur is None or mdl < cur[0]:
            levels[n][cv] = (mdl, expr, pdepth)

    for name, v in g.leaves.items():
        if _ok(v):
            put(1, v, lc, name, 0)

    for n in range(2, max_nodes + 1):
        # unary: child has n-1 nodes
        for cv, (mdl, expr, pd) in levels[n - 1].items():
            for op in g.unary:
                r = apply_unary(op, cv)
                if r is not None and _ok(r):
                    put(n, r, mdl + oc, f'{op}({expr})', pd)
        # binary: children i + j = n - 1
        for i in range(1, n - 1):
            j = n - 1 - i
            for av, (amdl, aexpr, apd) in levels[i].items():
                for bv, (bmdl, bexpr, bpd) in levels[j].items():
                    for op in g.binary:
                        if op == '^':
                            pd = max(apd, bpd) + 1
                            if pd > 2:
                                continue
                        else:
                            pd = max(apd, bpd)
                        r = apply_binary(op, av, bv)
                        if r is not None and _ok(r):
                            put(n, r, amdl + bmdl + oc,
                                f'({aexpr} {op} {bexpr})', pd)
        log(f'  [{g.name}] nodes={n}: {len(levels[n])} distinct values')
    return levels


def distinct_up_to(levels, n):
    """Distinct values across levels 1..n with their min MDL (the size of
    E(G, k) after value canonicalization; figure F2 data)."""
    best = {}
    for m in range(1, n + 1):
        for cv, (mdl, expr, _) in levels[m].items():
            if cv not in best or mdl < best[cv][0]:
                best[cv] = (mdl, expr)
    return best


if __name__ == '__main__':
    for g in (G_INT(), G_STRUCT(betti=(21, 77)), G_TRANS()):
        print(f'{g.name}: |A| = {len(g.leaves)}, leaf cost {g.leaf_cost():.2f} '
              f'bits, op cost {g.op_cost():.2f} bits')
        levels = enumerate_values(g, 5)
        total = distinct_up_to(levels, 5)
        print(f'  |E({g.name}, 5 nodes)| = {len(total)} distinct values')
