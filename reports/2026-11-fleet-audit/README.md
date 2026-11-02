# Fleet audit — the whole estate, read end to end

**3 November 2026** · 100 repositories · 1.4M lines of application code · 7,169 named code units

Two documents and one machine-readable snapshot. The report is the argument; the workbook is the
evidence; `state/fleet-audit.json` is the matrix in a form a future run can diff against.

    fleet-audit-report.docx   61 pages — catalogue, four analyses, plan, risks
    fleet-inventory.xlsx      12 sheets — fleet, capability matrix, function index,
                              kit adoption, conformance, overlap, licences,
                              interoperability, activity, gaps, keep-or-retire

## How it was produced

Every repository was shallow-cloned (depth 1), walked with vendored dependency directories excluded,
and its named code units extracted per language. Capabilities were then assigned **by hand against
the source** on a fixed 19-column taxonomy — an early keyword pass tagged 44 of 100 repos as LAN apps
because `\blan\b` matched the filename `lan-kit.js`, which is the kind of error that makes a
comparison table worthless.

Kit adoption was measured from the filesystem: does the kit's `.js` file physically exist inside
another repository? A README claim is not adoption. A registry entry is not adoption. A file is.

The procedure is packaged as a reusable skill in the standalone `repo-fleet-audit` bundle
(SKILL.md, four reference documents, six working scripts), so the next audit is a re-run rather than
a re-do.

## The headline findings

1. **The kit layer is half-wired and the registry does not know it.** Of 18 shared kits, 7 are
   vendored by another repository and 11 have zero consumers. The registry claims consumers for 8
   kits that do not import them — `game-kit` against six games, `srs-kit` against four study apps.
2. **The clinical estate is the unique asset and the most fragmented family.** 13 repositories,
   271,421 rubrics, 744,394 graded remedy links, readable offline. They share four case models, four
   scorers, four search implementations and seven hand-rolled language tables.
3. **74 of 100 repositories are PolyForm Noncommercial and two are proprietary** — including HMS,
   under an EULA that withdraws the MIT licence earlier versions carried. So no bundle can be sold as
   it stands. One person holds copyright in all of it, so this is a decision rather than a blocker —
   but it has not been taken anywhere, and it conditions every suite.
4. **Two product families have an institutional buyer and are not packaged as products**: HMS (a
   complete LAN hospital system) and the Room apps (chalk, canteen, lantern).
5. **Distribution is solved and unindexed.** 57 repositories publish a release and 92 have CI. What
   is missing is one generated index with versions, checksums and licences — not a build pipeline.
6. **83 of the 100 repositories were created in October 2026.** A body of work at a velocity no
   single maintainer can keep consolidating by hand, which is the argument for the suites — not
   tidiness, arithmetic.

## What to read first

- Section 5 — the structural finding, plus **5.2 what no app does** and **5.3 keep, fold or retire**.
- Section 6 — 22 improvement pairs, ordered by value. Three of them are worth doing this month.
- Section 7 — six suites, and **7.2 which of them are licence-clean today** (Room and Weft-8 are).
- Section 9 — 17 new product specifications, with **9.13 who pays for which**.

## Limits, stated plainly

READMEs, file trees, entry points, UI headings and function names were read — not all 1.4M lines.
`The_Browser` (Chromium-derived), `HCS` (a 6,060-file codec vault), `NEO` (a compiler with four
backends) and `ziptastic` were sampled at the level of architecture and public API. Conclusions about
those four concern their place in the estate, not their internal quality.

No app was executed except where a shipped test harness made it trivial. Several conclusions rest on
the registry and changelogs as evidence of intent; where they disagree with the code, the code wins
and the report says so.
