#!/usr/bin/env python3
"""
coincidence_fake_frameworks.py -- negative controls (M2; skeleton 5.1).

Builds the two deliberately fake frameworks the method MUST condemn, and runs
the condemnation test. If the method fails to condemn them, the method is
broken and that is the result.

Fake A ("the adversarial fit"): for each synthetic observable, claim the
best-matching expression in E(G_STRUCT, k). This is what a motivated fitter
does with full freedom inside the declared grammar.

Fake B ("the invented alphabet"): same fitting procedure, but over a grammar
whose 'structural' alphabet is 20 random integers dressed up as invariants of
an invented manifold. Tests that an arbitrary alphabet buys nothing once the
trials factor is priced.

Condemnation statistic. A fitted framework achieves, on each observable,
essentially the nearest-neighbor distance of E(G, k): no claim can beat the
nearest value that exists in the space. So its joint score
    J = mean_i [ -log10(relative deviation_i) ]
must be TYPICAL of the fitting null: the distribution of J obtained by
applying the same best-match procedure to fresh random target sets. The
verdict rule (to be carried into the paper): a framework survives screening
only if its J sits beyond the 99.9th percentile of the fitting null computed
with the framework's own degrees of freedom. The fakes, by construction,
should land near the middle.

Synthetic targets only; deterministic seed. No frozen observable value is
read here.

Output: results/fake_frameworks.json + printed verdicts.
"""

import bisect
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coincidence_grammars import (Grammar, G_STRUCT, enumerate_values,
                                  distinct_up_to)

SEED = 20260612
MAX_NODES = 5
M_OBS = 20               # observables per fake framework
N_NULL_SETS = 500        # replicate random target sets for the fitting null
LOG_RANGE = (1e-2, 1e2)  # synthetic target range (log-uniform)
SURVIVAL_PERCENTILE = 99.9

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                   'results', 'fake_frameworks.json')


def fake_alphabet(rng, n=20):
    """Random integers 3..248 dressed up as invariants of an invented
    manifold. Same cardinality ballpark as a real structural alphabet."""
    names = ['dim_X', 'rank_X', 'b1_X', 'b2_X', 'b3_X', 'chi_X', 'w_X',
             'p1_X', 'p2_X', 'c2_X', 'h11_X', 'h21_X', 'g_X', 'n_X', 'k_X',
             'd_X', 'r_X', 's_X', 't_X', 'u_X']
    vals = rng.sample(range(3, 249), n)
    leaves = {str(i): float(i) for i in range(1, 10)}
    leaves.update({names[i]: float(vals[i]) for i in range(n)})
    return Grammar('G_FAKE', leaves)


def best_match(sorted_vals, x):
    """Relative deviation of the nearest enumerated value to x."""
    i = bisect.bisect_left(sorted_vals, x)
    cands = [sorted_vals[j] for j in (i - 1, i) if 0 <= j < len(sorted_vals)]
    return min(abs(v - x) / abs(x) for v in cands)


def joint_score(sorted_vals, targets):
    """J = mean over targets of -log10(best relative deviation)."""
    return sum(-math.log10(max(best_match(sorted_vals, x), 1e-300))
               for x in targets) / len(targets)


def draw_targets(rng, m):
    lo, hi = math.log(LOG_RANGE[0]), math.log(LOG_RANGE[1])
    return [math.exp(rng.uniform(lo, hi)) for _ in range(m)]


def condemn(name, sorted_vals, rng):
    """Build the fitted fake on its own target set, then place its joint
    score inside the fitting null (same procedure, fresh random targets)."""
    targets = draw_targets(rng, M_OBS)
    j_fake = joint_score(sorted_vals, targets)
    null = sorted(joint_score(sorted_vals, draw_targets(rng, M_OBS))
                  for _ in range(N_NULL_SETS))
    rank = bisect.bisect_left(null, j_fake)
    pct = 100.0 * rank / len(null)
    survives = pct > SURVIVAL_PERCENTILE
    verdict = 'SURVIVES (METHOD BROKEN!)' if survives else 'CONDEMNED'
    print(f'{name}: J = {j_fake:.3f}, fitting-null percentile = {pct:.1f} '
          f'(null median {null[len(null)//2]:.3f}, '
          f'99.9th {null[int(len(null)*0.999)]:.3f}) -> {verdict}')
    return {'joint_score': j_fake, 'percentile': pct,
            'null_median': null[len(null) // 2],
            'null_p999': null[int(len(null) * 0.999)],
            'verdict': verdict}


def main():
    rng = random.Random(SEED)
    report = {'seed': SEED, 'max_nodes': MAX_NODES, 'm_obs': M_OBS,
              'n_null_sets': N_NULL_SETS,
              'survival_percentile': SURVIVAL_PERCENTILE, 'fakes': {}}

    print('enumerating E(G_STRUCT, k) ...')
    g_struct = G_STRUCT(betti=(21, 77))
    vals_struct = sorted(distinct_up_to(
        enumerate_values(g_struct, MAX_NODES, log=lambda s: None),
        MAX_NODES).keys())
    print(f'  {len(vals_struct)} distinct values')
    report['fakes']['A_adversarial_fit_G_STRUCT'] = condemn(
        'Fake A (adversarial fit, G_STRUCT)', vals_struct, rng)

    print('enumerating E(G_FAKE, k) ...')
    g_fake = fake_alphabet(rng)
    vals_fake = sorted(distinct_up_to(
        enumerate_values(g_fake, MAX_NODES, log=lambda s: None),
        MAX_NODES).keys())
    print(f'  {len(vals_fake)} distinct values '
          f'(invented alphabet: {sorted(int(v) for k, v in g_fake.leaves.items() if k.endswith("_X"))})')
    report['fakes']['B_invented_alphabet'] = condemn(
        'Fake B (invented alphabet)', vals_fake, rng)

    both = all(f['verdict'] == 'CONDEMNED' for f in report['fakes'].values())
    report['negative_controls_pass'] = both
    print('negative controls:', 'PASS (both condemned)' if both
          else 'FAIL (the method let a fake through)')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1)
    print(f'wrote {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
