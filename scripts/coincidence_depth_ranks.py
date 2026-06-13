#!/usr/bin/env python3
"""
coincidence_depth_ranks.py -- how a claim's rank moves as the enumeration
deepens, framework-agnostic.

The scorecard ranks (the distinct values matching a target as well or better)
are first computed in a shallow enumeration. A claim whose own witness is deeper
than that enumeration is then ranked below its own complexity budget, and
competitors that only appear deeper are invisible. That is the depth caveat.

This script recomputes, for each claim, two ranks at enumeration depths 5, 6, 7
(the practical full-enumeration ceiling in pure Python; level 7 of the larger
grammar holds ~22M distinct values):

  rank_full       distinct values within +-dev of the target, no budget filter.
                  This SCALES with |E(G,d)|; it is not depth-invariant and is
                  reported only to show why the budget filter is needed.
  rank_at_kappa   the subset whose own min description length is at most the
                  claim's budget (the principled statistic). Once the
                  enumeration exceeds what the budget can buy, no new sub-budget
                  competitor appears and this CONVERGES. A claim whose
                  rank_at_kappa is 1 and stable across the last two depths is a
                  depth-certified, budget-unique match.

Claims whose budget is larger than depth 7 can buy do not converge here; their
rank is finished by the Monte-Carlo estimator (coincidence_mc_match.py).

Input: a claims JSON (list of {id, symbol, grammar, betti, target, dev_abs,
kappa_MDL, node_budget}); no claims ship with this repository.

Usage: coincidence_depth_ranks.py CLAIMS.json OUT.json [MAX_DEPTH]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from coincidence_grammars import (  # noqa: E402
    G_STRUCT, G_TRANS, G_INT, enumerate_lean, rank_at)

DEFAULT_MAX_DEPTH = 7
CHECKPOINTS = (5, 6, 7)


def build_grammar(name, betti):
    if name == 'G_STRUCT':
        return G_STRUCT(betti=tuple(betti or ()))
    if name == 'G_TRANS':
        return G_TRANS()
    return G_INT()


def main():
    claims_path, out_path = sys.argv[1], sys.argv[2]
    max_depth = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_MAX_DEPTH
    with open(claims_path, encoding='utf-8') as f:
        claims = json.load(f)

    # group claims by (grammar, betti) so each grammar is enumerated once
    groups = {}
    for c in claims:
        key = (c['grammar'], tuple(c.get('betti') or ()))
        groups.setdefault(key, []).append(c)

    snaps = {}
    for (gname, betti), members in groups.items():
        g = build_grammar(gname, betti)
        # the bigger alphabet (G_TRANS) is capped one depth lower for memory
        depth = max_depth if gname == 'G_STRUCT' else min(max_depth, 6)
        cks = tuple(d for d in CHECKPOINTS if d <= depth)
        print(f'enumerating E({gname}, betti={betti}) to depth {depth} ...')
        snaps[(gname, betti)] = enumerate_lean(g, depth, cks,
                                               log=lambda s: None)
        print(f'  depths {sorted(snaps[(gname, betti)])}')

    out = []
    print(f'\n{"id":<4} {"symbol":<12} {"kMDL":>6} {"full 5/6/7":>18}   '
          f'{"budget 5/6/7":>16}  conv')
    for c in claims:
        key = (c['grammar'], tuple(c.get('betti') or ()))
        avail = snaps[key]
        depths = sorted(avail)
        full, budg = {}, {}
        for d in depths:
            rf, rb = rank_at(avail[d], c['target'], c['dev_abs'],
                             kappa=c['kappa_MDL'])
            full[d], budg[d] = rf, rb
        converged = len(depths) >= 2 and budg[depths[-1]] == budg[depths[-2]]
        out.append({'id': c['id'], 'symbol': c.get('symbol', c['id']),
                    'grammar': c['grammar'], 'kappa_MDL': c['kappa_MDL'],
                    'node_budget': c['node_budget'], 'rel_dev':
                    c['dev_abs'] / abs(c['target']),
                    'rank_full_by_depth': full,
                    'rank_at_kappa_by_depth': budg,
                    'budget_converged': converged})
        fc = '/'.join(str(full[d]) for d in depths)
        bc = '/'.join(str(budg[d]) for d in depths)
        print(f'{c["id"]:<4} {c.get("symbol", c["id"]):<12} '
              f'{c["kappa_MDL"]:>6.1f} {fc:>18}   {bc:>16}  '
              f'{"yes" if converged else "NO"}')

    deepest = lambda o: o['rank_at_kappa_by_depth'][
        max(o['rank_at_kappa_by_depth'])]
    b1 = [o for o in out if deepest(o) == 1]
    conv = [o for o in b1 if o['budget_converged']]
    opn = [o for o in b1 if not o['budget_converged']]
    print(f'\nrank_at_kappa = 1 at deepest enum: {len(b1)} '
          f'({", ".join(o["id"] for o in b1)})')
    print(f'  depth-converged (caveat lifted): {len(conv)} '
          f'({", ".join(o["id"] for o in conv)})')
    print(f'  not converged -> MC needed: {len(opn)} '
          f'({", ".join(o["id"] for o in opn)})')

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'max_depth': max_depth, 'checkpoints': list(CHECKPOINTS),
                   'rows': out}, f, indent=1, ensure_ascii=False)
    print(f'\nwrote {out_path}')


if __name__ == '__main__':
    main()
