# 2026-10-31 — Four decisions, and what was done about them

## What I looked at

The half-pinned build workflow, the 11 landing pages holding app state, the 10 repos with no
release assets, and the 7 repos whose badge and LICENSE disagreed.

## The four decisions

Asked as multiple choice; recorded here with the answer and the outcome.

| Question | Answer | Outcome |
|---|---|---|
| Close the half-pin? | "kit updates but not to retrofit — do what is best" | Pinned the kit checkout to the workflow's own commit |
| Split the 11 app-state landing pages? | "None more — today-card was the only one worth it" | No action. today-card stays split |
| 10 repos with no release assets? | "landing page only for now; most don't need a live demo" | No action. They stay landing-only, and stay excluded from the download-block script |
| 7 soft licence claims? | "Update the LICENSE to match the friendlier badge wording" | Seven licences rewritten |

## What I changed

**The half-pin.** All four kit checkouts in `build.yml` now use:

    ref: ${{ github.job_workflow_sha || 'main' }}

`job_workflow_sha` is the commit of the reusable workflow being executed, so the kit and the
workflow are now the same commit by construction. Bumping the caller moves both. The `|| 'main'`
fallback means that if the variable is ever empty, behaviour is what it was before — no regression.

Committed as `d7c4e0cb`, then piloted on `today-card` (pin moved to it, build green). One honest
caveat: at the time of the pilot, `main` and the pin were the same commit, so that build cannot
distinguish "pinned" from "fell back". The guarantee is structural, not yet observed in a
divergent state.

**The seven licences.** Each now grants what its badge promised:

| Repo | Badge said | Licence now says |
|---|---|---|
| MATERIA-MEDICA-BUILDER | free with attribution | Free to Use, With Attribution |
| boericke-repertory | free use · attribution required | Free to Use, With Attribution |
| unstoppable-mind-companion | free to use | Free to Use |
| whispering-body-first-aid | free to use | Free to Use |
| ambient-sound-studio | personal use only | Personal Use Only |
| the-symphony-companion | personal use only | Personal Use Only |
| smartbill-app | custom dual | Free for Personal and Single-Business Use |

Each carries a no-warranty clause, and the health-related ones carry a plain "this is educational
material, not medical advice" notice. smartbill's carries a line saying the author is not liable for
tax or GST consequences of using it.

## Evidence

- `build.yml` patched at 4 sites, YAML parses, all 10 jobs intact; pilot build `success`.
- All 7 LICENSE files re-read through the API: correct title line, no "all rights reserved" left,
  grants present.
- Licence checker now returns `SUMMARY` (informational) for all 7 — zero contradictions fleet-wide.

## What I deliberately did not do

- **Did not split any landing page beyond today-card.** The five games/engines would gain a click
  before the thing the visitor came for.
- **Did not add download buttons to repos with nothing to download.**
- **Did not write a licence I would not stand behind.** These are plain-language grants matching the
  badges, not legal advice — they should be reviewed before any commercial dispute could turn on
  them.

## Next

1. Bump the remaining 35 apps onto `d7c4e0cb` so the pinned kit reaches them (batches of six).
2. Per-app artwork: drop a `docs/icon.png` into any repo and the next build uses it.
3. Item 9 of the original requirements list — still unknown.
