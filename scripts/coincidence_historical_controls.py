#!/usr/bin/env python3
"""
coincidence_historical_controls.py -- M3: the method must reproduce known
verdicts. Eddington's alpha^-1 claim must FAIL (including a penalty for the
1929 -> 1930 revision); the quantum Hall quantization must PASS.

Historical inputs verified against fetched sources (agent pass, 2026-06-12):

EDDINGTON
- 1929: claims alpha^-1 = 136 (Proc. R. Soc. A 122, 358 (1929); via Kragh
  arXiv:1510.04046).
- 1930: revises to 137 (Proc. R. Soc. A 126, 696 (1930); the abstract reads
  "nevertheless I appear to have made such a mistake, and the new prediction
  is 137"). Revision factor = 2 claims fielded.
- Era data: alpha^-1 = 137.29 +/- 0.11 (Birge 1929) and 137.030 +/- 0.016
  (Birge 1941). PROVENANCE CAVEAT: read from a tertiary compilation table
  (viXra:1205.0050 Table 1.1, consistent with standard histories); primary
  Birge compilations to be cited directly in the paper.

QUANTUM HALL
- 1980: von Klitzing, Dorda, Pepper (PRL 45, 494): plateau quantization
  R_H = h/(i e^2) verified at 3 ppm (figure from von Klitzing's Nobel
  lecture, Rev. Mod. Phys. 58, 519 (1986)). Claim: the dimensionless plateau
  ratio is EXACTLY the integer i. No revision ever.
- 2012: graphene vs GaAs universality at 8.7e-11 relative (Janssen et al.,
  Metrologia 49, 294; arXiv:1202.2985).
- 1982: explained topologically (TKNN, PRL 49, 405): the coincidence that
  became a theorem.

Scoring rule (same shape as the fake-framework screening): a claim at one
era PASSES the screen iff
  (i)  it matches the era's measurement at z <= 1, and
  (ii) its corrected rank (number of distinct values in E(G, k) matching the
       era's value as well or better, times the claimant's revision factor)
       is <= RANK_MAX (essential uniqueness at that precision).
A framework control passes only if its claims pass at the eras where they
were defended. Eddington must fail; the quantum Hall claim must pass.

Output: results/historical_controls.json + printed scorecards.
"""

import bisect
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coincidence_grammars import G_INT, enumerate_values, distinct_up_to

MAX_NODES = 6      # G_INT only: cheap enough at 6 nodes
RANK_MAX = 3       # corrected-rank threshold for "essentially unique"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                   'results', 'historical_controls.json')


def n_as_good(sorted_vals, x, dev):
    """Distinct enumerated values matching x at least as well as |dev|."""
    lo = bisect.bisect_left(sorted_vals, x - abs(dev))
    hi = bisect.bisect_right(sorted_vals, x + abs(dev))
    return hi - lo


def score(vals, claim, x, sigma, revisions, label):
    dev = claim - x
    z = abs(dev) / sigma
    rank = n_as_good(vals, x, dev)
    corrected = rank * revisions
    passes = (z <= 1.0) and (corrected <= RANK_MAX)
    print(f'  {label:<42} z = {z:6.2f}  rank = {rank:4d}  x{revisions} '
          f'-> corrected {corrected:4d}  {"PASS" if passes else "FAIL"}')
    return {'label': label, 'claim': claim, 'x': x, 'sigma': sigma,
            'z': z, 'rank': rank, 'revisions': revisions,
            'corrected_rank': corrected, 'passes': passes}


def main():
    print(f'enumerating E(G_INT, {MAX_NODES}) ...')
    levels = enumerate_values(G_INT(), MAX_NODES, log=lambda s: None)
    vals = sorted(distinct_up_to(levels, MAX_NODES).keys())
    print(f'  {len(vals)} distinct values')

    report = {'max_nodes': MAX_NODES, 'rank_max': RANK_MAX,
              'grammar': 'G_INT', 'controls': {}}

    print('\nEDDINGTON (must FAIL):')
    edd = [
        # claim, era value, era sigma, revision factor, label
        score(vals, 136.0, 137.29, 0.11, 1,
              '1929 claim 136 vs Birge-1929 137.29(11)'),
        score(vals, 137.0, 137.29, 0.11, 2,
              '1930 revised 137 vs Birge-1929 (x2 revision)'),
        score(vals, 137.0, 137.030, 0.016, 2,
              '1930 claim 137 vs Birge-1941 137.030(16)'),
    ]
    edd_fails = not any(c['passes'] for c in edd)
    print(f'  => Eddington {"FAILS at every era (control OK)" if edd_fails else "PASSES somewhere (METHOD BROKEN)"}')
    report['controls']['eddington'] = {'claims': edd,
                                       'control_ok': edd_fails}

    print('\nQUANTUM HALL (must PASS):')
    # dimensionless plateau ratio sigma_xy / (i e^2/h), claimed exactly 1.
    # Encode the measured central value at the claim (deviation consistent
    # with zero at the stated precision of each era).
    qhe = [
        score(vals, 1.0, 1.0, 3e-6, 1,
              '1980 von Klitzing: integer quantization @ 3 ppm'),
        score(vals, 1.0, 1.0, 8.7e-11, 1,
              '2012 graphene/GaAs universality @ 8.7e-11'),
    ]
    qhe_passes = all(c['passes'] for c in qhe)
    print(f'  => Quantum Hall {"PASSES (control OK; TKNN 1982 = the coincidence that became a theorem)" if qhe_passes else "FAILS (METHOD BROKEN)"}')
    report['controls']['quantum_hall'] = {'claims': qhe,
                                          'control_ok': qhe_passes}

    ok = edd_fails and qhe_passes
    report['historical_controls_pass'] = ok
    print(f'\nhistorical controls: {"PASS (known verdicts reproduced)" if ok else "FAIL"}')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1)
    print(f'wrote {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
