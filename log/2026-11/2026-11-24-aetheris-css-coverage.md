# Aetheris — the page was unstyled for two reasons, and neither was the properties

**Rows:** `0.7` fixed, `0.8` opened. **Date:** 2026-11-24.

## The plan this came from

Rather than take another inherited tail, the question was put to a measurement: what does a real page's
stylesheet actually get from this engine? `tools/css-coverage.cpp` resolves one element twice per
declaration - once with nothing, once with that declaration - and compares `fingerprint()`.

## The answer was not the properties

| | |
| --- | --- |
| declarations in the page's CSS | 2,869 |
| changed the resolved style | **2,821 (98.3%)** |
| did not | 48 - every one setting a property to its own initial value (`display: block`, `opacity: 1`), which changes nothing and so cannot be seen this way |

"The engine drops CSS properties" was wrong. Worth knowing before writing another row about property
support.

## The real causes, one layer down

**215,771 bytes of real CSS parsed to 7 rules.** Two reasons:

1. **Stylesheets were classified by their `.css` suffix.** Wikipedia serves CSS from
   `/w/load.php?...&only=styles`, so all 41 stylesheets were fetched, cached as **images**, and never
   concatenated into the cascade. The render's own output said "12330 bytes of CSS" - only the inline
   `<style>` - and that number had been sitting there for two days.
2. **`@supports`, `@layer`, `@container` fell through to the rule path**, where the at-rule condition was
   compiled as a selector and everything after the block was lost. The page carries 70 `@supports` blocks.

Fixed: dependencies now carry their kind (from `href` on `<link>`, not from the URL), and the grouping
at-rules recurse like `@media`.

| | before | after |
| --- | --- | --- |
| CSS in the cascade | 12,330 bytes | **3,905,094 bytes** |
| rules parsed | 7 | **922** (1,818 selectors) |
| the render | a column of unstyled text | styled: tabs, blue section links, real layout |

## What the first styled render exposed

Large **black boxes** where backgrounds should be light. That defect was invisible while the page was
unstyled, because nothing painted a background. Row `0.8`, with its probe named.

## Also

`tools/setup.sh` - toolchain, HarfBuzz, both build dirs, one command; `--check` reports without changing.
The pod recycled four times in this session and each cost ten to forty minutes of rediscovery.
Suite 67/67 twice, 158.37 s and 200.75 s.
