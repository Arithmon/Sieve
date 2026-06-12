#!/usr/bin/env python3
"""
coincidence_nulls_synthetic.py -- N0 and N1 scaffold on SYNTHETIC targets (M2).

Implements the first two null models of the frozen design
(freeze/GRAMMARS_FREEZE.md + the paper skeleton, sections 3.1-3.2) against
synthetic targets only:

- N1 (complexity-matched expression search): for a target value x with
  uncertainty sigma, the local accidental-match count is the number of
  distinct values in E(G, k) with |v - x| <= z * sigma. The formalized
  inverse-symbolic-calculator attack.
- N0 (random constants): draw synthetic observables from a log-uniform
  reference distribution and report the distribution of N1 match counts over
  the draws: the baseline density of accidental matches as a function of
  grammar, complexity budget k, precision, and z.

Everything is deterministic (fixed seed) and synthetic: no frozen observable
value is read here. Real-target scoring comes later in the pipeline, now
permitted because the freeze is deposited (v1.0, DOI 10.5281/zenodo.20666879)
but staged separately on purpose.

Output: results/nulls_synthetic.json + printed summary.
"""

import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coincidence_grammars import (G_INT, G_STRUCT, G_TRANS,
                                  enumerate_values, distinct_up_to)

SEED = 20260612          # freeze date; deterministic
MAX_NODES = 5            # smoke-test budget (production runs go deeper)
N_TARGETS = 2000         # synthetic observables per configuration
LOG_RANGE = (1e-3, 1e3)  # log-uniform reference range for synthetic targets
REL_SIGMAS = (1e-2, 1e-3, 1e-4)   # synthetic relative uncertainties
Z = 1.0                  # match window in sigmas

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                   'results', 'nulls_synthetic.json')


def n1_match_count(sorted_vals, x, abs_window):
    """Number of enumerated distinct values within +/- abs_window of x
    (binary search on the sorted value list)."""
    import bisect
    lo = bisect.bisect_left(sorted_vals, x - abs_window)
    hi = bisect.bisect_right(sorted_vals, x + abs_window)
    return hi - lo


def main():
    rng = random.Random(SEED)
    lo, hi = (math.log(LOG_RANGE[0]), math.log(LOG_RANGE[1]))
    targets = [math.exp(rng.uniform(lo, hi)) for _ in range(N_TARGETS)]

    report = {'seed': SEED, 'max_nodes': MAX_NODES, 'n_targets': N_TARGETS,
              'log_range': LOG_RANGE, 'z': Z, 'grammars': {}}

    for g in (G_INT(), G_STRUCT(betti=(21, 77)), G_TRANS()):
        print(f'== {g.name} ==')
        levels = enumerate_values(g, MAX_NODES, log=lambda s: None)
        gram = {'alphabet_size': len(g.leaves), 'growth': {}, 'n0': {}}
        for k in range(1, MAX_NODES + 1):
            gram['growth'][k] = len(distinct_up_to(levels, k))
        print(f'  |E(G,k)| by node count: {gram["growth"]}')

        vals = sorted(distinct_up_to(levels, MAX_NODES).keys())
        for rel in REL_SIGMAS:
            counts = [n1_match_count(vals, x, Z * rel * x) for x in targets]
            hit = sum(1 for c in counts if c > 0)
            gram['n0'][rel] = {
                'mean_matches': sum(counts) / len(counts),
                'frac_targets_with_match': hit / len(counts),
            }
            print(f'  rel sigma {rel:g}: mean N1 matches '
                  f'{gram["n0"][rel]["mean_matches"]:.2f}, '
                  f'P(>=1 accidental match) = '
                  f'{gram["n0"][rel]["frac_targets_with_match"]:.3f}')
        report['grammars'][g.name] = gram

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1)
    print(f'wrote {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
