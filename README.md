# The Arithmon Sieve

The methodology arm of the [Arithmon program](https://github.com/arithmon):
a formal standard for the question *how surprising is a claimed exact relation
between mathematical invariants and measured physical constants?*

A sieve separates structure from coincidence. The field currently has no
shared instrument for that: claims oscillate between uncritical acceptance and
reflexive dismissal, and the verdicts (Eddington on one side, the quantum Hall
relation on the other) are only sorted in hindsight. This repository builds
the instrument: a declared expression space, complexity measures, a family of
null models with explicit look-elsewhere correction, and a scorecard designed
to be reused on any framework, including ours.

## Contents

- [`freeze/`](freeze/) holds the frozen inputs: the observable list (28
  dimensionless measured constants, framework-independent inclusion criteria,
  values verified against CODATA 2022 / PDG 2025 / NuFIT 6.1 / Planck 2018
  with per-value citations) and the expression grammars (three alphabets, two
  complexity measures, anti-gaming guards).
- [`scripts/`](scripts/) holds the generator for the machine-readable freeze
  and, as they land, the pipeline stages: null models N0 to N3, calibration
  controls, the scorecard.

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

Freeze v1.0 drafted and agent-verified against primary sources; human
spot-check and Zenodo deposit pending. **No expression search has run.**

## Contributing

Issues are welcome, in particular: historical cases that should join the
calibration set, null models we have not considered, and ways to game the
scorecard (rule 4 means finding them is a contribution). House style is
enforced by the [org linter](https://github.com/arithmon/.github): plain
language, no promotional vocabulary, no em-dashes.

---

<sub>GIFT is the founding framework of the Arithmon program.
Program: [arithmon.com](https://arithmon.com) ·
[github.com/arithmon](https://github.com/arithmon)</sub>
