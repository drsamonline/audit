# 2026-11-03 — The whole fleet read end to end: 100 repos, 7,169 functions, four analyses

## What I looked at

All 100 repositories under the account. Each one shallow-cloned at depth 1, its tree walked with
vendored dependency directories excluded, and its named code units extracted per language — Python
`def`/`class`/route decorators, JavaScript function/arrow/class/export, Rust `pub fn`, C/C++
definitions, Dart, Go.

    100 of 100 cloned
     1.4M lines of application code
     7,169 named code units indexed
     1.5 GB working tree

Capabilities were assigned by hand against the source on a fixed 19-column taxonomy. The first pass
was keyword-based and produced a matrix that was confidently wrong — 44 of 100 repos tagged as LAN
apps because `\blan\b` matched the filename `lan-kit.js`. The hand pass took an hour and is the
difference between a table that can be acted on and one that cannot.

## What was wrong

Three things, and the first is the one that matters.

**1. The kit registry overstates adoption.** Measured from the filesystem — does the kit's `.js` file
physically exist inside another repository — of 18 shared kits, 7 are used and 11 have zero consumers:

    web-kit        25 adopters
    export-kit      8
    lan-kit         3
    frame-kit       3
    optical-kit     3
    search-kit      2
    case-kit        2
    --------------- 11 kits with no adopter at all
    game-kit, art-kit, audio-kit, ml-kit, ui-kit, book-kit,
    srs-kit, repertory-kit, astro-kit, compress-kit, crypto-kit (1, and not the one claimed)

The registry claims consumers for eight kits that do not import them: `game-kit` against six games,
`repertory-kit` against four repertories, `srs-kit` against four study apps, `book-kit` against four
companions. Of the two claims that are partly right, both name the wrong adopters.

**2. The clinical library is the unique asset and the most fragmented family.** 13 repositories,
271,421 rubrics, 744,394 graded remedy links, readable with no network. They share almost nothing:
four case models, four repertorisation scorers, four search implementations, seven hand-rolled
English–Hindi–Gujarati string tables.

**3. The licence position has never been stated, and the most important repository is not what its
earlier releases said.** 74 repositories are PolyForm Noncommercial, 7 MIT, and two are proprietary
EULA — including HMS, which explicitly withdraws the MIT licence earlier versions carried. Two
(`HCS`, `compfactory`) have no LICENSE file at all, including the one that vendors codecs under
LGPL-3 and GPL-3 obligations.

My own first pass got this wrong: a machine classifier read HMS as MIT because the EULA quotes the
MIT withdrawal near the top of the file. It took reading the file to see it. A wrong licence cell is
worse than a missing one, because it looks like diligence — so every licence below was re-read by
hand from its header.

    PolyForm Noncommercial 1.0.0   74
    MIT                             7
    Free-to-use (custom)            4
    All rights reserved             4
    Personal-use (custom)           3
    Proprietary EULA                2   <- HMS and Mnemosyne
    Other / custom                  2
    No licence file                 2   <- HCS and compfactory
    Mixed CC0 + GPL-3.0             1
    CC0-1.0                         1

## What I changed

Nothing in any other repository. This is a measurement, not a sweep. What changed is in this repo:

    reports/2026-11-fleet-audit/fleet-audit-report.docx   61 pages
    reports/2026-11-fleet-audit/fleet-inventory.xlsx      12 sheets
    reports/2026-11-fleet-audit/README.md                 the summary above
    state/fleet-audit.json                                the matrix, diffable

The report carries a catalogue entry for all 100 repositories, then the four analyses asked for:
22 improvement pairs, 6 suites, 8 merges, 17 new product specifications — plus capability gaps
(what *no* app does), keep/fold/retire decisions, licence feasibility per suite, and a buyer table.

## Evidence

The measurements the findings rest on, all reproducible from the workbook:

    kit adoption            sheets "Kits", "Libraries"
    capability matrix       100 x 19, sheet "Capability matrix"
    every code unit         7,169 rows, sheet "Function index"
    licences                sheet "Licences" (per repo, with second licence files)
    releases                57 of 100 publish a release
    conventions             92 CI, 99 licence file, 77 self-tests, 93 landing page,
                            35 service workers of which only 9 advertise installability
    velocity                83 of 100 repositories created in October 2026

Two cross-checks that came back clean and are worth recording, because they are the failure modes
one would expect:

- **No permissive app vendors a restrictive kit.** All ~50 vendoring relationships checked; zero
  licence conflicts.
- **The mixed-content repositories handle it correctly.** Four carry a second licence file — the JSON
  corpus separates its CC0 material from the GPL-3 `repertorium-publicum-2008/` folder, and
  `kent-repertory-explorer` carries the GPL-3 text alongside its own PolyForm licence because it
  embeds that corpus.

## What I deliberately did not do

- **Did not read all 1.4M lines.** `The_Browser` (Chromium-derived, 1.97M lines with vendored trees),
  `HCS` (6,060 files), `NEO` and `ziptastic` were sampled at architecture, entry points and public
  API. Conclusions about them are about placement in the estate, not code quality.
- **Did not execute the apps.** No app was run except where a shipped test harness made it trivial.
  Everything here describes what the code declares, not what it does under load.
- **Did not fix anything.** The duplication, the eleven unused kits and the two missing licence files
  are recorded, not repaired. A sweep that deletes a kit while its successor is unwritten is how a
  consolidation turns into a regression.
- **Did not take the relicensing decision.** It is the author's to take, per suite, and the report
  sets out what each suite needs rather than choosing for them.

## Next

Phase 0 is one week and almost free, and everything after it is cheaper because of it:

1. Generate the kit registry from the filesystem instead of maintaining it by hand — the check that
   produced the adoption table is the generator.
2. Decide adopt / fold / delete on the eleven unused kits within 90 days, and delete what is not
   adopted. A kit that exists and is not used is worse than no kit.
3. Write one English–Hindi–Gujarati corpus and migrate the seven apps that hand-roll it.
4. Freeze a case-record schema before Suite A or B begins.
5. Add a LICENSE to `HCS` and `compfactory`.

Then: Suite B (the repertory library) first, because it is the highest value at the lowest risk;
Suite A (the clinic) second, on the schema Phase 0 froze; and if a suite is wanted this month, build
Room or Weft-8 — those two are licence-clean and need no decision at all.
