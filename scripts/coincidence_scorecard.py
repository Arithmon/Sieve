#!/usr/bin/env python3
"""
coincidence_scorecard.py -- the generic scorecard statistic
(framework-agnostic; the deliverable of the methods paper, section 4.3).

Takes a claims file and produces the scorecard components for ANY framework:

  per claim   z (deviation in target-sigma units), relative deviation,
              rank_full  = number of distinct values in E(G, k) matching the
                           target as well or better (local look-elsewhere),
              rank_at_kappa = same, restricted to values of min-MDL <= the
                           claim's declared complexity (if provided)
  joint       matches at z <= 1 and z <= 2,
              concentration S = sum log10(N / rank_full),
              percentile of S against a random-claims null (R replicates,
              one uniformly drawn E-value per target)

DECLARED LIMITS (frozen design): S separates structure from RANDOM claims,
not from FITTED ones; a best-fitter attains rank 1 everywhere by spending
complexity. The anti-fitting reading lives in rank_at_kappa, the declared
search history, and the in-framework-theorem rebate (future work).

Claims file format (JSON):
  {"grammar": "G_STRUCT" | "G_INT" | "G_TRANS",
   "betti": [b2, b3],                  # for G_STRUCT, [] otherwise
   "claims": [{"name": str, "claim": float, "target": float,
               "sigma": float, "kappa_mdl": float (optional)}, ...]}

Usage: python3 coincidence_scorecard.py CLAIMS.json [OUT.json]

No claims file ships with this repository: the inputs are whatever framework
you want to screen. The frozen observable list (freeze/) provides targets and
sigmas; supplying the claims is the framework's job.
"""

import bisect
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coincidence_grammars import (G_INT, G_STRUCT, G_TRANS,
                                  enumerate_values, distinct_up_to)

SEED = 20260612
MAX_NODES = 5
R_NULL = 2000


def build_space(grammar_name, betti):
    g = {'G_INT': lambda: G_INT(),
         'G_STRUCT': lambda: G_STRUCT(betti=tuple(betti)),
         'G_TRANS': lambda: G_TRANS()}[grammar_name]()
    best = distinct_up_to(enumerate_values(g, MAX_NODES, log=lambda s: None),
                          MAX_NODES)
    pairs = sorted((v, mdl) for v, (mdl, _) in best.items())
    return {'vals': [p[0] for p in pairs], 'mdls': [p[1] for p in pairs],
            'N': len(pairs), 'grammar': grammar_name}


def ranks(space, x, dev_abs, kappa=None):
    lo = bisect.bisect_left(space['vals'], x - dev_abs)
    hi = bisect.bisect_right(space['vals'], x + dev_abs)
    full = max(hi - lo, 1)
    if kappa is None:
        return full, None
    budg = max(sum(1 for i in range(lo, hi) if space['mdls'][i] <= kappa), 1)
    return full, budg


def scorecard(spec, r_null=R_NULL, seed=SEED):
    space = build_space(spec['grammar'], spec.get('betti', []))
    N = space['N']
    rows, S = [], 0.0
    for c in spec['claims']:
        x, v = c['target'], c['claim']
        dev = abs(v - x)
        rf, rb = ranks(space, x, dev, c.get('kappa_mdl'))
        contrib = math.log10(N / rf)
        S += contrib
        rows.append({'name': c['name'], 'z': dev / c['sigma'],
                     'rel_dev': dev / abs(x), 'rank_full': rf,
                     'rank_at_kappa': rb, 'log10_N_over_rank': contrib})
    rng = random.Random(seed)
    targets = [c['target'] for c in spec['claims']]
    null = []
    for _ in range(r_null):
        s = 0.0
        for x in targets:
            v = space['vals'][rng.randrange(N)]
            s += math.log10(N / ranks(space, x, abs(v - x))[0])
        null.append(s)
    null.sort()
    return {'grammar': spec['grammar'], 'max_nodes': MAX_NODES,
            'N_values': N, 'n_claims': len(rows),
            'z_le_1': sum(1 for r in rows if r['z'] <= 1),
            'z_le_2': sum(1 for r in rows if r['z'] <= 2),
            'S': S, 'S_max': len(rows) * math.log10(N),
            'null_median': null[len(null) // 2], 'null_max': null[-1],
            'S_percentile_vs_random':
                100.0 * bisect.bisect_left(null, S) / len(null),
            'rows': rows,
            'declared_limits': 'S does not exclude fitting; see module header'}


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding='utf-8') as f:
        spec = json.load(f)
    card = scorecard(spec)
    print(f"{spec['grammar']}: N = {card['N_values']}, "
          f"claims = {card['n_claims']}, z<=1: {card['z_le_1']}, "
          f"S = {card['S']:.1f} (max {card['S_max']:.1f}), "
          f"null median {card['null_median']:.1f} / max {card['null_max']:.1f}, "
          f"percentile {card['S_percentile_vs_random']:.2f}")
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            json.dump(card, f, indent=1, ensure_ascii=False)
        print(f'wrote {sys.argv[2]}')


if __name__ == '__main__':
    main()
