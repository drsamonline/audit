# Documentation

Corpus Extendum is a static library of out-of-copyright books, built from a
pipeline that verifies rights, typesets reading files and shelves them in
storage repositories.

**The shelf:** https://drsamonline.github.io/corpus-extendum/
**The catalogue without a browser:** [`index.txt`](../index.txt)
**What is on the shelf right now:** 46 books, 12 categories, 152.3 MB

---

## Start here

| If you want to… | Read |
|---|---|
| understand how the whole thing fits together | [Architecture](ARCHITECTURE.md) |
| know how a book gets on the shelf | [Pipeline](PIPELINE.md) |
| find a field, or add one | [Data model](DATA-MODEL.md) |
| add a book, rebuild, rotate, deploy, or fix something | [Operations](OPERATIONS.md) |
| work on the page or the reader | [Frontend](FRONTEND.md) |
| understand the storage repositories | [Vaults](VAULTS.md) |
| know why something is the way it is | [Decisions](DECISIONS.md) |
| check a copyright claim | [Rights](RIGHTS.md) |
| see what was built, and what broke | [Changelog](../CHANGELOG.md) |

## The one-paragraph version

Books come from Standard Ebooks and the Gutenberg mirror. Each is checked
against two copyright tests — author's death + 60 for India, published before
1930 for the United States — and refused unless both pass. It is then typeset
into an A5 PDF, its EPUB is kept, plain text is extracted, and two hashes are
stored: one for the file, one for the normalised text, which is the dedupe key.
Files go into a vault repository; the catalogue is rebuilt from the vaults'
own records; the site reads only that catalogue and fetches books from a CDN.
A vault seals at 600 books or 2.5 GB and the next one opens.

## What is built, and what is not

The documentation marks every feature **built**, **designed** or **planned**.
The current gaps, stated plainly:

| Gap | Consequence |
|---|---|
| Translator registry is short | only translators with a read source are accepted, so Chekhov and most Verne wait on an entry |
| No in-book search | the reader has no text layer to search |
| No format conversion | MOBI, DjVu, DOCX, CBR are not handled |
| No archive.org adapter | scanned editions are unreachable |

## Conventions in these documents

- Numbers are measured, not estimated. Where a figure came from a run, it says so.
- A decision that cost a debugging round is written down with its symptom, so it
  costs one round and not two.
- Nothing is described as working unless a command produced the output that
  proves it.

_Updated 2026-11-16._
