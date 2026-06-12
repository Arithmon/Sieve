#!/usr/bin/env python3
"""
coincidence_n1_frozen.py -- N1 against the FROZEN observable list.

First real-data run of the pipeline. Permitted because the freeze is
deposited (v1.0, DOI 10.5281/zenodo.20666879, 2026-06-12); this script reads
the frozen JSON and nothing else.

For each frozen observable x with uncertainty sigma, and each frozen grammar,
reports the N1 local accidental-match count: the number of distinct values in
E(G, k) with |v - x| <= z * sigma (z = 1). This is the per-observable
look-elsewhere baseline every claimed relation must be scored against: a
"match" on an observable whose count is 50 is worth nothing; a match on an
observable whose count is 0 carries information.

Output: results/n1_frozen.json + printed table.
"""

import bisect
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coincidence_grammars import (G_INT, G_STRUCT, G_TRANS,
                                  enumerate_values, distinct_up_to)

MAX_NODES = 5
Z = 1.0
HERE = os.path.dirname(os.path.abspath(__file__))
FREEZE = os.path.join(HERE, '..', 'freeze', 'observables_freeze_draft.json')
OUT = os.path.join(HERE, '..', 'results', 'n1_frozen.json')


def count(sorted_vals, x, w):
    lo = bisect.bisect_left(sorted_vals, x - w)
    hi = bisect.bisect_right(sorted_vals, x + w)
    return hi - lo


def main():
    with open(FREEZE, encoding='utf-8') as f:
        freeze = json.load(f)
    entries = freeze['entries']

    grammars = {}
    for g in (G_INT(), G_STRUCT(betti=(21, 77)), G_TRANS()):
        levels = enumerate_values(g, MAX_NODES, log=lambda s: None)
        grammars[g.name] = sorted(distinct_up_to(levels, MAX_NODES).keys())
        print(f'{g.name}: |E(G,{MAX_NODES})| = {len(grammars[g.name])}')

    rows = []
    print(f'\nN1 accidental-match counts at z = {Z} (node budget {MAX_NODES}):')
    print(f'{"entry":<28} {"value":>12} {"rel sigma":>10} '
          f'{"G_INT":>6} {"G_STRUCT":>9} {"G_TRANS":>8}')
    for e in entries:
        x, s = e['value'], e['error']
        c = {name: count(vals, x, Z * s) for name, vals in grammars.items()}
        rows.append({'name': e['name'], 'value': x, 'error': s,
                     'rel_sigma': s / abs(x), 'counts': c})
        print(f'{e["name"]:<28} {x:>12.6g} {s/abs(x):>10.2e} '
              f'{c["G_INT"]:>6} {c["G_STRUCT"]:>9} {c["G_TRANS"]:>8}')

    summary = {g: {'zero_count_entries':
                   sum(1 for r in rows if r['counts'][g] == 0),
                   'total_matches': sum(r['counts'][g] for r in rows)}
               for g in grammars}
    print('\nentries with ZERO accidental match (information-bearing at this '
          f'budget): ' + ', '.join(f'{g}: {s["zero_count_entries"]}/28'
                                   for g, s in summary.items()))

    report = {'freeze_doi': '10.5281/zenodo.20666879', 'z': Z,
              'max_nodes': MAX_NODES, 'rows': rows, 'summary': summary}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1)
    print(f'wrote {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
