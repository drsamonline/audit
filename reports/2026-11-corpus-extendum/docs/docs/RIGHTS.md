# Rights

This library exists on one claim: **every book here is out of copyright**. If
that claim is wrong for a single title, the library is not trustworthy for any
of them. So the rule is narrow and it is applied before a book is fetched, not
after.

## The two-test gate

Copyright terms are national. A book must pass **both** tests:

| Jurisdiction | Test | As of 2026 |
|---|---|---|
| **India** | author's death + 60 years | died before **1966** |
| **United States** | published before the current cut-off | published before **1930** |

The stricter test wins. Both are computed at ingest and written into the record:

```json
"rights": {
  "basis": "author d. 1898; first published 1865 — public domain in India (life + 60) and the United States (pre-1930)",
  "india": true,
  "us": true,
  "verified": "2026-11-15"
}
```

A reader can audit the claim instead of trusting it, and a future audit can
recompute it from the record.

## Translations

For a translation the term runs on the **translator's** death, not the author's.
So a translated work is gated on a person the author check never sees.

The gate reads the translator from the edition's own record — the OPF contributor
carrying the MARC relator `trl` — and then requires an entry in
`data/translators.json` with `verified: true` and a source that was actually read:

| Check | Rule |
|---|---|
| translator named by the edition | otherwise the author gate applies alone |
| present in `data/translators.json` | unknown translators are refused |
| `verified: true` with a source | an unverified entry is refused |
| translator's death + 60 ≤ current year | India |
| translation first published before 1930 | United States |

The translation's own publication year comes from the book entry, not from the
edition date — a Standard Ebooks edition is modern even when the translation is
Victorian.

**Refused today:** F. A. Malleson, F. H. Peters, and the anonymous Modern
Library translator of *Candide* — the edition credits a publisher, not a person,
which can never pass. Verne's other novels wait on those.

**Shelved today:** Long's Epictetus and Marcus Aurelius, Legge's Tao Te Ching,
Towle's Verne, Arnold's Gita, Jowett's Plato, and **Constance Garnett's
Chekhov** — her death was read from three sources (17 December 1946) after being
refused for two rounds on memory alone.

## Sources, and what each one's licence actually says

### Standard Ebooks

The texts are public domain. The **edition** — proofreading, typesetting,
artwork, and the CC0 dedication on their contributions — is released under
**CC0 1.0 Universal**, which is why it can be reused without conditions.

Our PDFs are not their PDFs: they are typeset from their source XHTML with our
own stylesheet. If you want the edition as they intended it, take the EPUB.

### Project Gutenberg, via the GITenberg mirror

The texts are public domain. The **licence Project Gutenberg attaches is a
separate agreement** with its own terms, and those terms are respected here:

- attribution to the source ebook number is kept in the record;
- redistribution is free of charge;
- no Project Gutenberg name, logo or trademark is used, and nothing here
  suggests Project Gutenberg endorses this library.

The boilerplate is stripped; the credit stays.

### Internet Archive

Declared in the design, **not implemented**. Its `collection:gutenberg` items are
metadata stubs with no text — checked. Real scans live in other collections and
each item's own rights statement would have to be checked individually before
shelving.

## What this library owns

| Thing | Licence |
|---|---|
| The texts | public domain, by definition |
| Our typesetting, generated covers | CC0 1.0 |
| Catalogue records and metadata | CC0 1.0 |
| The site, the pipeline, the documentation | CC0 1.0 |

A library that gates its own catalogue behind a licence has misunderstood the
assignment.

## Corrections

If a rights basis here is wrong, open an issue.

The fix is one commit: correct `meta.json` in the vault and remove the
corresponding line from that vault's `index.txt`. The book disappears from the
catalogue on the next rebuild. A **sealed** vault can be corrected this way — it
simply cannot be added to.

Nothing is ever deleted from a sealed vault. The catalogue stops showing the
book, and the file stays where the record says it is.

## What this library is not

It is not legal advice, and it is not a rights clearance service. If you intend
to republish anything you find here — especially commercially, and especially
from outside India and the United States — check your own jurisdiction. Public
domain is a national fact, not a global one.
