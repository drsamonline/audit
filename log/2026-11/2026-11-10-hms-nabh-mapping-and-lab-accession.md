# hms — the NABH mapping the specification promised, and a specimen accession

Date: 2026-11-10 · Repo `drsamonline/HMS` · branch `batch-23-nabh-lab`, PR #103 (open,
not merged)
References read: `nabh.co/software/yro-systems-pvt-ltd/` (a certification record, used
as a checklist shape) and `DIGI-UW/OpenELIS-Global-2` (sample-centric lab workflow).
Neither was adopted; see below.

## What I looked at
`docs/MASTER_SPECIFICATION.md` (NABH AYUSH stated three times, mapped nowhere),
`backend/app/models/investigation.py`, `investigation_result.py`,
`backend/app/api/v1/endpoints/investigations.py`,
`backend/app/services/investigation.py`, `backend/tests/_qa_harness.py`, and the
existing NCH work on this branch (`services/certificates.py`,
`services/adverse_events.py`, `services/nch_compliance.py`).

## What was wrong
Two things, both about claims outrunning code.

The specification says the product supports NABH AYUSH documentation. That was true
of the intent and unchecked in the code: nothing anywhere listed which Objective
Elements the application can evidence, so "we support NABH" could not be argued or
disproved.

And an investigation had a result but no sample. The laboratory's own identifier for
the specimen — the number written on the tube, the thing a result is traced back
through — did not exist, so two specimens could not be distinguished and a mislabelled
result could not be caught.

## What I changed
**Slice A** — `docs/NABH-MAPPING.md`, 25 rows across access and accountability,
records, medication and laboratory, retention, digital-health and configuration.
Each row names the element, what the standard asks, what HHMS does, the file or
endpoint that proves it, and a state. Ten rows are `absent` and collected into a
roadmap with no owners or dates. Two are `partial`, and say what is missing: the
prescriber's registration number is stored but not yet printed, and a specimen has an
accession but no collector, collection time or sample type.

This extends the specification's own claim rather than competing with it;
`MASTER_SPECIFICATION.md` is unchanged.

**Slice B** — `sample_accession` on `Investigation`: nullable, unique when set,
migration `0040`, accepted on create and returned on read. A service check names the
accession already in use instead of letting a unique constraint surface as a 500.

`backend/tests/test_batch_b37_nabh_mapping.py` asserts every file the mapping cites
exists and every endpoint it cites is mounted. `test_batch_b36_lab_accession.py`
covers the round-trip, the duplicate refusal and the no-sample case.

## Evidence
    cd backend && python -m pytest -q        # in eight slices, reconciled:
                                             # 875 passed, 2 skipped, 877 collected
    python -m alembic heads                  # 0040_investigation_accession (head)

    # failing before — service reverted, everything else left in place
    git checkout -- backend/app/services/investigation.py
    python -m pytest tests/test_batch_b36_lab_accession.py -q
    -> 2 failed, 2 passed  (round-trip; duplicate refusal)

    # passing after — service restored
    -> 4 passed

    # every citation resolves
    32 file paths cited, 0 missing; 6 endpoints cited, all mounted.

## What I deliberately did not do
- **No status filter.** The brief asked for one; `GET /investigations` already
  filters by `investigation_status`. Rebuilt would have been a second way to do it.
- **No FHIR or openEHR.** A data-model rewrite for a LAN SQLite product, and the
  clinical model is frozen. OpenELIS was read for the sample-to-result shape, not for
  its schema.
- **No new dependency.**
- **No sample types, worklists, analyser interfaces, QC or barcodes** — the next
  slices, each needing a decision this one did not make.
- **Nothing in printing, reports, backup/restore or the archive tables.**
- **No version bump, no merge, no force-push.**
- **No "improvement" to files passed through** beyond the two named changes.

## Next
The `partial` rows are the cheapest movement: printing the prescriber's registration
number on the prescription and certificate is a client change against a field that
already exists, and collection detail on the accession is three columns.

The `absent` roadmap is not sequenced. PSQ.3's 32 organisational KPIs are the largest
item and are already planned as their own wave; consent capture and incident reporting
are the two gaps most likely to be asked for by an assessor.
