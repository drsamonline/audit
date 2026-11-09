# lan-kit — every reconnect replayed the room

Date: 2026-11-09 · Repo `drsamonline/lan-kit` · PR #3 (open, not merged)
Links taken: none

## What I looked at
`lan-host.js` (98 lines), `lan-kit.js` (54), `test-node.js`.

## What was wrong
The host sent `retry: 2000` and replayed its whole history to every connection,
and never sent an `id:` — so EventSource's automatic reconnect had nothing to
resume from. After any blip, `onMessage` fired again for up to 50 messages the app
had already shown.

## What I changed
Each broadcast carries `id: <n>`; `/events` reads `Last-Event-ID` and replays
only newer entries; no header still gets the full history (a first connection).
The client is untouched — EventSource sends the header itself, which is why ids
beat a `?since=` parameter.

## Evidence
    node test-resume.js     3 PASS, "resume: OK"
    before                  FAIL "every broadcast carries an id",
                            FAIL "a reconnect after Last-Event-ID replays
                            nothing it has seen (no ids to resume from)" — 2 failed
    node test-node.js       8 passed, 0 failed
CI run 42653700983: success, log lines `8 passed, 0 failed` and `resume: OK`.

## What I deliberately did not do
- No change to history size, the ping, CORS, or the 1 MB body cap.
- No link work: yjs/automerge/gun/json-joy/hypercore/sqlsync/berty are CRDT or
  p2p sync engines; this is a LAN room with SSE and POST and no merge semantics.
- No version bump, no merge.

## Next
Decide on PR #3.
