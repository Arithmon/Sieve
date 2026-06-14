# The Arithmon Sieve

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20666879.svg)](https://doi.org/10.5281/zenodo.20666879)

The methodology arm of the [Arithmon program](https://github.com/arithmon):
a formal standard for the question *how surprising is a claimed exact relation
between mathematical invariants and measured physical constants?*

## In plain words

Sometimes a short formula in fundamental constants and small whole numbers
lands surprisingly close to a measured quantity. Sometimes that is a real clue
about nature. Sometimes it is an accident, made to look meaningful afterwards by
a lucky choice of formula. The hard part is telling the two apart *before* you
know which one it is.

History has both kinds. Eddington argued the fine-structure constant had to be
exactly 1/136, then exactly 1/137 once the measurement moved: a coincidence,
refitted after the fact. The quantum Hall resistance, by contrast, is an exact
ratio that was predicted, never revised, and later explained: a real relation.
The field usually only sorts cases like these in hindsight, once the verdict is
already in.

The Sieve is an attempt at an instrument that sorts them in advance, by a rule
fixed before looking. The inputs (which constants count, which formulas are
allowed) are written down and time-stamped with a public DOI before any search
runs, so nothing can be quietly tuned to the answer. The instrument is then
turned on known cases to check it behaves (Eddington must fail, the quantum Hall
relation must pass), and only after that on anything we care about, including the
GIFT framework itself. Anyone can run it on their own framework, including one
built to try to beat it.

---

**The rest of this page is the technical specification**: the expression space,
the complexity measures, the four null models, the scorecard. If you only wanted
to know what the Sieve is and why to trust it, you have it.

The program's charter and open problems live in the
[program](https://github.com/arithmon/program) repository; the map of
adjacent work lives in the [atlas](https://github.com/arithmon/atlas); the
machine-checked formal layer (certified expression-space counts and the
in-framework-theorem rebate) lives in [lean](https://github.com/arithmon/lean).

## Contents

- [`freeze/`](freeze/) holds the frozen inputs: the observable list (28
  dimensionless measured constants, framework-independent inclusion criteria,
  values verified against CODATA 2022 / PDG 2025 / NuFIT 6.1 / Planck 2018
  with per-value citations) and the expression grammars (three alphabets, two
  complexity measures, anti-gaming guards).
- [`scripts/`](scripts/) holds the pipeline: the expression-space engine
  (three grammars, two complexity measures), the four null models N0 to N3,
  the calibration controls, and the generic scorecard
  (`coincidence_scorecard.py`: feed it any framework's claims against the
  frozen targets and get the full component report).
- [`results/`](results/) holds the machine-readable outputs of every run,
  deterministic seeds throughout.
- [`docs/`](docs/) holds the living pre-registration: the
  [decisions ledger](docs/LEDGER.md) (discipline, milestones, dated decisions)
  and the [legend](docs/LEGEND.md) that resolves every label used across the
  program.

## The discipline

1. **Freeze before search.** The observable list and the grammars are
   deposited with a dated DOI before any expression search runs. The DOI
   timestamp is the proof. A data update (new PDG edition, new global fit) is
   a new freeze version with its own DOI; verdicts against the old version
   stand.
2. **Calibration before use.** The method must condemn deliberately
   constructed fake frameworks and reproduce known historical verdicts
   (Eddington's 1/136-then-1/137 must fail, including a penalty for the
   revision; the quantum Hall relation must pass) before it is allowed to
   score anything we care about. If it fails calibration, that failure is the
   result.
3. **The scorecard, not a single p-value.** Per-relation local significance,
   joint global significance under each null, complexity budget consumed, and
   an explicit declaration of researcher degrees of freedom.
4. **Open by construction.** Frozen inputs, pinned environment, deterministic
   seeds. Anyone can re-run the pipeline against any framework, hostile
   parties included.

## Status

**Freeze v1.0 DEPOSITED 2026-06-12**: DOI
[10.5281/zenodo.20666879](https://doi.org/10.5281/zenodo.20666879)
(concept DOI for all versions:
[10.5281/zenodo.20666878](https://doi.org/10.5281/zenodo.20666878)).
At deposit time, **no expression search had run**; everything below operates
against these inputs as frozen.

**Calibration complete (scaffold budget, 5-6 nodes):**

- Negative controls CONDEMNED: an adversarial best-match fit and an
  invented-alphabet framework land at the 89th and 17th percentile of the
  fitting null (survival requires the 99.9th).
- Historical verdicts reproduced: Eddington's 136-then-137 FAILS at every
  era (never within 1 sigma of contemporary data, revision penalty applied);
  the quantum Hall quantization PASSES (exact, essentially unique, never
  revised, explained by TKNN 1982).
- Four nulls implemented: N1/N2 price the search (survival thresholds clear
  the N2 alphabet-freedom envelope), N3 catches assignment vagueness, N0
  anchors the accidental-match baseline.
- First N1 against the frozen list: at a 5-node budget, 6/28 (G_INT), 3/28
  (G_STRUCT) and 2/28 (G_TRANS) entries carry information at their measured
  precision; a lone match on a loosely measured constant is worth little by
  construction.

## Contributing

Issues are welcome, in particular: historical cases that should join the
calibration set, null models we have not considered, and ways to game the
scorecard (rule 4 means finding them is a contribution). The four procedures the
Sieve owns (propose or attack a null model, submit a hostile framework, challenge
a freeze, report a cherry-picking issue) are spelled out in
[CONTRIBUTING.md](CONTRIBUTING.md). House style is enforced by the
[org linter](https://github.com/arithmon/.github): plain language, no promotional
vocabulary, no em-dashes.

---

<sub>GIFT is the founding framework of the Arithmon program.
Program: [arithmon.com](https://arithmon.com) ·
[github.com/arithmon](https://github.com/arithmon)</sub>
