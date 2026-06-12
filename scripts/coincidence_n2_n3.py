#!/usr/bin/env python3
"""
coincidence_n2_n3.py -- N2 (adversarial numerologist) and N3 (permutation),
completing the four-null family (skeleton 3.3-3.5). Synthetic targets only;
deterministic seed.

N2, the adversarial numerologist (skeleton 3.3). The fitter is granted one
more degree of freedom than in N1: the alphabet itself. Within declared
bounds (here: any 20-integer 'invented manifold' alphabet, T candidate
alphabets), the adversary fits every alphabet to the targets and keeps the
best. The resulting envelope
    J_N2 = max over alphabets of J_fit(alphabet, targets)
upper-bounds the achievable-by-fitting region. Consequence for the verdict
rule: a framework's joint score must clear the N2 ENVELOPE, not merely the
single-alphabet fitting null; alphabet freedom is part of the researcher
degrees of freedom and must be priced.

N3, the permutation null (skeleton 3.4). Shuffle the assignment of claimed
expressions to observables and re-score. N3 tests ASSIGNMENT SPECIFICITY:
whether each claim is about its own observable, or whether the claims are so
loose that anything matches anything. Documented honestly (skeleton 3.5):
a best-match FITTED framework passes N3 (fits are target-specific by
construction), so N3 alone does NOT detect fitting. That is why the family
is needed: N1/N2 price the search, N3 catches vagueness, N0 anchors the
accidental-match baseline.

Output: results/n2_n3_synthetic.json + printed summary.
"""

import bisect
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coincidence_grammars import enumerate_values, distinct_up_to
from coincidence_fake_frameworks import fake_alphabet, draw_targets

SEED = 20260612
MAX_NODES = 4            # N2 scaffold budget (T alphabets to enumerate)
M_OBS = 20
T_ALPHABETS = 12         # adversary's alphabet trials (declared bound)
N_PERMS = 2000           # N3 permutation replicates
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                   'results', 'n2_n3_synthetic.json')


def enum_sorted(grammar):
    levels = enumerate_values(grammar, MAX_NODES, log=lambda s: None)
    return sorted(distinct_up_to(levels, MAX_NODES).keys())


def best_dev(sorted_vals, x):
    i = bisect.bisect_left(sorted_vals, x)
    cands = [sorted_vals[j] for j in (i - 1, i) if 0 <= j < len(sorted_vals)]
    return min(abs(v - x) / abs(x) for v in cands)


def fit(sorted_vals, targets):
    """Best-match claims; returns per-target relative deviations."""
    return [max(best_dev(sorted_vals, x), 1e-300) for x in targets]


def J(devs):
    return sum(-math.log10(d) for d in devs) / len(devs)


def main():
    rng = random.Random(SEED)
    targets = draw_targets(rng, M_OBS)
    report = {'seed': SEED, 'max_nodes': MAX_NODES, 'm_obs': M_OBS}

    # ---------------- N2: adversarial numerologist ----------------
    print(f'N2: fitting {T_ALPHABETS} candidate alphabets '
          f'(20 invented integers each, {MAX_NODES}-node budget) ...')
    scores = []
    for t in range(T_ALPHABETS):
        g = fake_alphabet(rng)
        s = J(fit(enum_sorted(g), targets))
        scores.append(s)
        print(f'  alphabet {t + 1:2d}: J = {s:.3f}')
    n2_envelope = max(scores)
    report['n2'] = {'t_alphabets': T_ALPHABETS, 'scores': scores,
                    'envelope': n2_envelope,
                    'single_alphabet_median': sorted(scores)[len(scores) // 2]}
    print(f'  N2 envelope (best of {T_ALPHABETS}): J = {n2_envelope:.3f} '
          f'(median single alphabet {report["n2"]["single_alphabet_median"]:.3f})')
    print('  -> verdict rule consequence: survival thresholds must clear the '
          'ENVELOPE, not the median; alphabet freedom is priced.')

    # ---------------- N3: permutation null ----------------
    # Case 1: a fitted (target-specific) framework. Claims = best matches.
    print(f'\nN3: permutation null ({N_PERMS} shuffles) ...')
    g = fake_alphabet(rng)
    vals = enum_sorted(g)
    i0 = bisect.bisect_left  # noqa: F841  (kept for clarity)
    claims = []
    for x in targets:
        i = bisect.bisect_left(vals, x)
        cands = [vals[j] for j in (i - 1, i) if 0 <= j < len(vals)]
        claims.append(min(cands, key=lambda v: abs(v - x)))

    def j_assign(perm):
        return J([max(abs(claims[p] - targets[i]) / abs(targets[i]), 1e-300)
                  for i, p in enumerate(perm)])

    ident = j_assign(range(M_OBS))
    perms = []
    idx = list(range(M_OBS))
    for _ in range(N_PERMS):
        rng.shuffle(idx)
        perms.append(j_assign(idx))
    perms.sort()
    pct_fit = 100.0 * bisect.bisect_left(perms, ident) / len(perms)
    print(f'  fitted framework: identity J = {ident:.3f}, permutation null '
          f'median {perms[len(perms) // 2]:.3f}, identity percentile {pct_fit:.1f}')
    print('  -> N3 NOT triggered by fitting (fits are target-specific): '
          'documented limit, why the family is needed (skeleton 3.5).')

    # Case 2: a vague framework. Claims drawn independently of the targets
    # (same magnitudes, no assignment information).
    vague_claims = [min([vals[bisect.bisect_left(vals, y) - 1],
                         vals[min(bisect.bisect_left(vals, y), len(vals) - 1)]],
                        key=lambda v: abs(v - y))
                    for y in draw_targets(rng, M_OBS)]

    def j_vague(perm):
        return J([max(abs(vague_claims[p] - targets[i]) / abs(targets[i]),
                      1e-300) for i, p in enumerate(perm)])

    ident_v = j_vague(range(M_OBS))
    perms_v = sorted(j_vague(random.Random(SEED + 1 + r).sample(
        range(M_OBS), M_OBS)) for r in range(N_PERMS))
    pct_vague = 100.0 * bisect.bisect_left(perms_v, ident_v) / len(perms_v)
    print(f'  vague framework: identity J = {ident_v:.3f}, permutation null '
          f'median {perms_v[len(perms_v) // 2]:.3f}, identity percentile {pct_vague:.1f}')
    print('  -> identity assignment indistinguishable from shuffles: '
          'N3 condemns claims that are not about their own observables.')

    report['n3'] = {
        'n_perms': N_PERMS,
        'fitted': {'identity_J': ident, 'null_median': perms[len(perms) // 2],
                   'identity_percentile': pct_fit},
        'vague': {'identity_J': ident_v,
                  'null_median': perms_v[len(perms_v) // 2],
                  'identity_percentile': pct_vague},
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1)
    print(f'\nwrote {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
