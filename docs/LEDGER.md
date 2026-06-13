# Decisions ledger

This is the living pre-registration of the Arithmon Sieve: the discipline, the
milestones, and the dated decisions that fix the method and the frozen inputs
before any search is scored. Labels are resolved in [`LEGEND.md`](LEGEND.md).

It records the **protocol**. A worked case study, its case-study-specific
scoring decisions, and its scorecard are the payload of the methodology paper
and are published there, not here. Pre-registration means the protocol is public
and fixed before the result is announced; the result follows in the paper. Some
`D`-numbered entries below are therefore protocol stated in general form, with
their case-study application held for the paper; the numbering is kept stable so
nothing is hidden, only located.

---

## Discipline (binding for every change in this repository)

1. **No search before the freeze (`M1`).** No expression enumeration, sampling,
   or matching against real observable values until the observable list and the
   grammars are frozen and deposited with a dated DOI. Pipeline development uses
   synthetic targets only (random values, fake frameworks). The DOI timestamp is
   what makes any later scorecard unimpeachable.
2. **The undeclared-history caveat stays explicit.** A framework's relations may
   predate this paper; the freeze governs the *paper's* null searches, not the
   framework's own development history. That history is bounded honestly in the
   paper, never claimed to be fully recovered, and the freeze is never said to
   retroactively sanitize a case study.
3. **Calibration before use.** The method must condemn deliberately constructed
   fake frameworks and reproduce known historical verdicts before it scores
   anything we care about. If it fails calibration, that failure is the result.
4. **Precision is never the headline.** The deliverable is the scorecard, not a
   single p-value.
5. **Decisions are journaled** here, dated, with rationale. A register move
   (strengthening or weakening a claim, or revisiting a frozen choice) is
   explicit and carries a new freeze version with its own DOI.

---

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| `M1` | Freeze observables and grammars, DOI deposit | **DONE 2026-06-12.** DOI [10.5281/zenodo.20666879](https://doi.org/10.5281/zenodo.20666879) (concept [10.5281/zenodo.20666878](https://doi.org/10.5281/zenodo.20666878)), via release v1.0; no search ran before deposit. |
| `M2` | Pipeline on N0 and N1; negative controls condemned | **In progress.** Grammar engine and N0/N1 on synthetic targets done; negative controls condemned (an adversarial fit and an invented alphabet land at the 89th and 17th percentile of the fitting null, below the 99.9th survival threshold). Remains: deeper complexity budget for production. |
| `M3` | Historical controls reproduce known verdicts | **Done at scaffold level.** Eddington's 136-then-137 fails at every era (revision penalty applied); the quantum Hall quantization passes. Paper-grade remains: primary Birge citations. |
| `M4` | N2 and N3 complete; full scorecard on a live case study | **In progress.** N2 and N3 complete at scaffold level (N2 prices alphabet freedom, the survival threshold is the envelope not the median; N3 catches assignment vagueness). The live case-study scorecard is the payload of the paper and is assembled there. |
| `M5` | Robustness battery | Open. Three grammars by two complexity measures; stability report. |
| `M6` | Draft, multi-reviewer read, submission | Open. |

**Sequencing.** `M2` and `M3` may be developed before `M1` is *deposited*, as
long as no real-observable search runs: synthetic and historical targets only,
the historical controls using their own frozen inputs.

---

## Decisions

- **D2 (2026-06-12).** Freeze-first discipline adopted (discipline rule 1).
  Rationale: registered-reports import; cheap now, decisive later.
- **D3 (2026-06-12).** The prior null-model run (joint significance against a
  GIFT-specific 20-symbol alphabet) is the acknowledged ancestor of `N1`. It is
  refactored, not extended: the pipeline here is grammar-parameterized and its
  inputs are framework-independent.
- **D4 (2026-06-12).** Observable freeze strategy: inclusion criteria are stated
  category by category, and each admitted category is included completely
  (anti-cherry-picking, `C3`). Values are assembled where public datasets
  overlap, but the criteria are written without reference to any framework, and
  every value is re-verified against primary sources before deposit.
- **D5 (2026-06-12).** Grammar freeze strategy: three grammars (`G_INT`,
  `G_STRUCT` with an explicit closure rule rather than a hand-picked list,
  `G_TRANS`) and two complexity measures (`kappa_MDL` in bits, `kappa_NODE`).
- **D6 (2026-06-12).** Neutrino sector frozen on NuFIT 6.1, normal ordering,
  without SK-atm, declared in the freeze. A future freeze version may revisit;
  that would be a journaled register move with a new DOI.
- **D7 (2026-06-12).** Quark masses MS-bar, PDG conventions (light quarks at
  2 GeV, m_c(m_c), m_b(m_b)); m_t treatment declared at verification time from
  what PDG quotes for ratios.
- **D8 (2026-06-12).** The pipeline code is public from `M2`, in a repository
  under the arithmon org, so anyone can re-run it against any framework, hostile
  parties included (open by construction).
- **D9 (2026-06-12).** `G_STRUCT` closure rule: dimensions and ranks of compact
  simple Lie groups of rank at most 8, Betti numbers of the framework-declared
  manifold family, and integers 1 to 9. Conservative by superset.
- **D10 (2026-06-12).** The complexity rebate for in-framework theorems (the
  formal-verification argument) is deferred to a dedicated formalization session.
  Not a blocker for `M1`.
- **D11 (2026-06-12).** Asymmetric uncertainties are symmetrized by taking the
  larger side. Conservative: this widens match windows for the null searches,
  never narrows them.
- **D12 (2026-06-12).** Gauge-coupling reference points, declared per entry:
  alpha at q^2 = 0 (the convention-free Thomson limit, the best-measured
  dimensionless constant), alpha_s at M_Z, sin^2 theta_W MS-bar at M_Z. Mixing
  reference points across entries is acceptable because each entry declares its
  own convention (`C5`); changing a convention after the freeze is not.
- **D13 (2026-06-12).** Quark-mass surface: the PDG Quark Masses review lattice
  averages (1-sigma), not the Summary Table 90% CL listings. One surface, cited
  consistently. The frozen light-quark entries are the ratios PDG actually
  evaluates (m_u/m_d, m_s/m_ud).
- **D14 (2026-06-12).** m_t in ratios: the cross-section value 162.5(2.1) GeV,
  for scheme consistency with m_b(m_b); the PDG label caveat is recorded.
- **D15 (2026-06-12).** Y_p: the observational value 0.245(3) (PDG BBN review),
  not the Planck BBN-consistency posterior (which is a prediction). eta_10 =
  6.12(4) admitted as the absolute baryon density.
- **D16 (2026-06-12).** No retroactive scheme charity (general policy). A claim
  that never declared its scheme or reference point is scored against the frozen
  entry as the basis defines it. Declaring a scheme afterwards is a revision and
  carries the revision factor. Rationale: the Eddington control shows why
  post-hoc target selection must be priced. Case-study application is in the
  paper.
- **D18 (2026-06-12).** Scorecard statistic (general). Per claim: the achieved
  relative deviation, its z, and its rank (the number of distinct values in the
  enumerated expression space matching the target as well or better). Joint
  concentration is reported as a sum of log10(N / rank) against a random-claims
  null. Declared limit: this separates structure from *random* claims, not from
  *fitted* ones; the anti-fitting closure comes from the complexity budget, the
  declared search history, and the in-framework-theorem rebate (`D10`). The
  scorecard reports all components, not one number.
- **D19 (2026-06-13).** Value popularity is a declared third scorecard
  statistic, beside isolation (the budget-filtered rank, by description length)
  and reachability (the Monte-Carlo match probability at the claim budget, by
  node count). Popularity is the peak of that match probability over the simple
  budgets up to a small reference (2 to 5 nodes): how reachable the target value
  is by the most favorable simple formula size, independent of the claim's own
  complexity. The peak, not a fixed size, because a value can be dense at one
  small size only (a value of 2/3 is reachable by many 3-node formulas but that
  signal is diluted if sampled at exactly 5 nodes). Rationale: precision plus low
  description length do not make a coincidence surprising if the value is easy
  to produce (a value of 2/3 is reachable by many simple formulas; an arbitrary
  ratio is not). The three statistics probe orthogonal axes and the scorecard
  reports all three.

> Numbering note. `D1` is internal workspace housekeeping (no protocol content).
> `D17` is case-study-specific (the claim mapping and label conventions of a
> scored framework); it is journaled with that case study and published in its
> paper. The reserved numbers are kept so this ledger stays a faithful index of
> every choice made, with nothing hidden, only located.
