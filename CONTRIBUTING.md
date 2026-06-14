# Contributing to the Sieve

The Sieve is an instrument for one question: *how surprising is a claimed exact
relation between mathematical invariants and measured physical constants?* The
most valuable contributions are the ones that make the instrument harder to
fool, including on us. Adversarial input is welcome by design.

Org-wide rules (what helps, what does not, house style) are in the
[organization CONTRIBUTING](https://github.com/arithmon/.github/blob/main/CONTRIBUTING.md).
This file covers the four procedures the Sieve owns.

## Propose or attack a null model

The Sieve ships four null models (N0 to N3). A good attack shows that one of
them is too generous, that a survivor would not survive a stronger but still
fair null, or that a null leaks a free parameter.

1. Open an issue titled `null: <which> <what is wrong>`.
2. State the null precisely: the draw, the alphabet, the closeness criterion,
   the look-elsewhere correction.
3. If you can, give the survivor count it would produce on the frozen 28
   observables, so the claim is checkable rather than rhetorical.
4. A null that strengthens the test is merged with attribution. A null that is
   weaker than an existing one is not, and the issue records why.

A new null never replaces a frozen one retroactively. It is added, versioned,
and the scorecard is recomputed openly.

## Submit a hostile or rival framework

Send any framework, including one built to make the Sieve pass something it
should not, or fail something it should not.

1. Provide the framework's claimed exact relations, its declared vocabulary
   (the invariants it is allowed to use), and any pre-registration date.
2. We encode it in the frozen grammars without charity: no per-claim schema
   tweak, no retroactive vocabulary widening.
3. The resulting scorecard is published whatever it says. A hostile framework
   that scores high is the most useful result you can give us: it is either a
   real signal or a hole in the test.

## Challenge a freeze

The frozen inputs (observable list, grammars, DOI
[10.5281/zenodo.20666879](https://doi.org/10.5281/zenodo.20666879)) are dated
on purpose. You cannot ask for a silent edit, but you can challenge them.

1. Open an issue titled `freeze: <claim>`.
2. Valid challenges: a value that disagrees with its cited source, a grammar
   guard that is circumventable, an inclusion criterion that is not
   framework-independent.
3. Accepted challenges produce a **new** dated freeze, with the old one left
   in place and the change logged. The point of a freeze is that history is
   visible, not erased.

## Report a possible cherry-picking issue

If you suspect a result depends on a choice made after seeing the data (an
observable quietly dropped, a grammar tuned to a target, a null selected for
its verdict), report it.

1. Name the specific choice and when, relative to the data, you believe it was
   made.
2. Point to the artifact: a commit, a frozen file, a scorecard entry.
3. We answer with the dated record. If the record cannot exonerate the choice,
   the result is flagged in place, not deleted.

---

Siblings: [Program](https://github.com/arithmon/program) ·
[Atlas](https://github.com/arithmon/atlas) ·
[Lean](https://github.com/arithmon/lean)

<sub>GIFT is the founding framework of the Arithmon program.
Program: [arithmon.com](https://arithmon.com) ·
[github.com/arithmon](https://github.com/arithmon)</sub>
