# AURORA-R7 distributed release

Reference time: `2026-11-20T15:10:00Z`.

Input locale and clock rules:

- English is the main language. Short Polish text uses `pl-PL`; short Japanese text uses `ja-JP`.
- `UTC` is `+00:00`. On these November dates, `CET` is `+01:00`. `JST` is `+09:00`.
- An offset in a source timestamp is authoritative. A plain time that names `UTC`, `CET`, or `JST` uses that named zone.
- The 10 input files contain 500 timestamped messages. Process them as one package in source chronology, not filename order alone.

## Required final registry

The final registry has exactly 6 records. `AURORA-R7/CHG-441` and
`AURORA-R7/CHG-447` are identity and lifecycle evidence for their release
records, not two additional commitments. Calendar objects and log runs are also
sources, not additional registry records.

### 1. `AURORA-R7/REL-204-EU`

- Type and action: release event; deploy the EU blue ring.
- Owner: `AURORA-R7/OWNER-MAYA-ITO`. The aliases `@maya` and `伊藤` resolve to this same owner.
- Original source time: `2026-11-18 21:00 UTC` = `2026-11-18 22:00 CET` = `2026-11-19 06:00 JST`.
- Original normalized time: `2026-11-18T21:00:00Z`.
- Final source time after the late reschedule: `2026-11-20 07:30 JST` = `2026-11-19 23:30 CET` = `2026-11-19 22:30 UTC`.
- Final normalized time: `2026-11-19T22:30:00Z`.
- Final state: completed at `2026-11-19T23:18:00Z`.
- Sources: `input/01-release-chat-utc.txt`, `input/03-release-chat-jst.txt`, `input/05-release-mailbox.txt`, `input/06-change-calendar.txt`, `input/07-deploy-log.txt`, `input/08-bridge-transcript.txt`, `input/09-shift-handoff.txt`, `input/10-ops-digest.txt`.
- Exact quote (`input/01-release-chat-utc.txt`): `2026-11-16T08:07:00Z | AURORA-R7/CHAT-UTC | AURORA-R7/OWNER-MAYA-ITO: AURORA-R7/REL-204-EU is booked for 2026-11-18 21:00 UTC, which is 22:00 CET and 2026-11-19 06:00 JST; I own the release window.`
- Exact quote (`input/03-release-chat-jst.txt`): `2026-11-18T21:04:00+09:00 | AURORA-R7/CHAT-JST | AURORA-R7/OWNER-MAYA-ITO: On this channel, 伊藤 and @maya both refer to AURORA-R7/OWNER-MAYA-ITO.`
- Exact quote (`input/03-release-chat-jst.txt`): `2026-11-19T07:14:00+09:00 | AURORA-R7/CHAT-JST | AURORA-R7/OWNER-MAYA-ITO: Partner confirms: move AURORA-R7/REL-204-EU, alias EU blue ring, to 2026-11-20 07:30 JST; this replaces the 2026-11-19 06:00 JST slot.`
- Exact quote (`input/05-release-mailbox.txt`): `2026-11-18T22:20:00Z | AURORA-R7/MAILBOX | AURORA-R7/MAIL-1045 from AURORA-R7/OWNER-MAYA-ITO: Confirmed new AURORA-R7/REL-204-EU window is 2026-11-19 22:30 UTC, 23:30 CET, and 2026-11-20 07:30 JST; it supersedes the 2026-11-18 21:00 UTC window.`
- Exact quote (`input/07-deploy-log.txt`): `2026-11-19T23:18:00Z | AURORA-R7/DEPLOY | AURORA-R7/REL-204-EU completed successfully; AURORA-R7/CHG-441 status closed by AURORA-R7/OWNER-MAYA-ITO.`

### 2. `AURORA-R7/REL-204-JP`

- Type and action: release event; deploy the separate JP green ring.
- Owner: `AURORA-R7/OWNER-KENJI-SATO`.
- Original and final source time: `2026-11-20 22:00 JST` = `2026-11-20 14:00 CET` = `2026-11-20 13:00 UTC`.
- Original and final normalized time: `2026-11-20T13:00:00Z`.
- Final state: completed at `2026-11-20T13:47:00Z`.
- Sources: `input/01-release-chat-utc.txt`, `input/03-release-chat-jst.txt`, `input/05-release-mailbox.txt`, `input/06-change-calendar.txt`, `input/07-deploy-log.txt`, `input/08-bridge-transcript.txt`, `input/09-shift-handoff.txt`, `input/10-ops-digest.txt`.
- Exact quote (`input/01-release-chat-utc.txt`): `2026-11-16T08:10:00Z | AURORA-R7/CHAT-UTC | AURORA-R7/OWNER-KENJI-SATO: AURORA-R7/REL-204-JP remains booked for 2026-11-20 22:00 JST, 13:00 UTC; I own that separate release window.`
- Exact quote (`input/03-release-chat-jst.txt`): `2026-11-19T07:16:00+09:00 | AURORA-R7/CHAT-JST | AURORA-R7/OWNER-MAYA-ITO: This update is for AURORA-R7/REL-204-EU and AURORA-R7/CHG-441; AURORA-R7/REL-204-JP and AURORA-R7/CHG-447 keep 2026-11-20 22:00 JST.`
- Exact quote (`input/07-deploy-log.txt`): `2026-11-20T13:47:00Z | AURORA-R7/DEPLOY | AURORA-R7/REL-204-JP completed successfully; AURORA-R7/CHG-447 status closed by AURORA-R7/OWNER-KENJI-SATO.`

### 3. `AURORA-R7/TKT-7811`

- Type and action: task; run the rollback rehearsal for `AURORA-R7/REL-204-EU`.
- Original owner: `AURORA-R7/OWNER-PIOTR-NOWAK`.
- Final owner: `AURORA-R7/OWNER-ELENA-PARK`, who explicitly accepted the reassignment.
- Original source deadline: `2026-11-18 16:00 CET`.
- Original normalized deadline: `2026-11-18T15:00:00Z`.
- Revised source deadline: `2026-11-19 12:00 CET`.
- Final normalized deadline: `2026-11-19T11:00:00Z`.
- Final state: completed at `2026-11-19T09:42:00Z`, before the revised deadline.
- Sources: `input/02-release-chat-cet.txt`, `input/04-tickets-export.txt`, `input/05-release-mailbox.txt`, `input/09-shift-handoff.txt`, `input/10-ops-digest.txt`.
- Exact quote (`input/04-tickets-export.txt`): `2026-11-16T10:00:00Z | AURORA-R7/TICKETS | AURORA-R7/TKT-7811 created: rollback rehearsal for AURORA-R7/REL-204-EU; assignee AURORA-R7/OWNER-PIOTR-NOWAK; due 2026-11-18 16:00 CET.`
- Exact quote (`input/04-tickets-export.txt`): `2026-11-18T08:04:00Z | AURORA-R7/TICKETS | AURORA-R7/TKT-7811 ownership changed from AURORA-R7/OWNER-PIOTR-NOWAK to AURORA-R7/OWNER-ELENA-PARK; Elena accepted the rehearsal.`
- Exact quote (`input/04-tickets-export.txt`): `2026-11-18T08:08:00Z | AURORA-R7/TICKETS | AURORA-R7/TKT-7811 due changed from 2026-11-18 16:00 CET to 2026-11-19 12:00 CET, 11:00 UTC.`
- Exact quote (`input/04-tickets-export.txt`): `2026-11-19T10:42:00+01:00 | AURORA-R7/TICKETS | AURORA-R7/TKT-7811 rehearsal completed successfully; final restore checksum matched AURORA-R7/FILE-RB-7811.`

### 4. `AURORA-R7/TKT-7824`

- Type and action: task; file the signed checksum attestation for `AURORA-R7/REL-204-EU`.
- Owner: explicitly absent. The assignee field is empty at the reference time. Watchers are not owners.
- Original and final source deadline: `2026-11-20 17:00 CET`.
- Original and final normalized deadline: `2026-11-20T16:00:00Z`.
- Final state: open and not yet due at the reference time.
- Sources: `input/04-tickets-export.txt`, `input/05-release-mailbox.txt`, `input/09-shift-handoff.txt`, `input/10-ops-digest.txt`.
- Exact quote (`input/04-tickets-export.txt`): `2026-11-16T10:15:00Z | AURORA-R7/TICKETS | AURORA-R7/TKT-7824 created: file the signed checksum attestation for AURORA-R7/REL-204-EU by 2026-11-20 17:00 CET; assignee remains unassigned.`
- Exact quote (`input/09-shift-handoff.txt`): `2026-11-20T00:20:00Z | AURORA-R7/HANDOFF | AURORA-R7/OWNER-LENA-KOVAC: AURORA-R7/TKT-7824 still has no assignee; its two watchers did not accept ownership.`
- Exact quote (`input/10-ops-digest.txt`): `2026-11-20T13:58:00Z | AURORA-R7/DIGEST | AURORA-R7/TKT-7824 remains open and unassigned ahead of its 17:00 CET due time.`

### 5. `AURORA-R7/CHG-448`

- Type and action: dependent task/event; run and record the thirty-minute telemetry watch after `AURORA-R7/REL-204-EU`.
- Owner: `AURORA-R7/OWNER-LENA-KOVAC`.
- Original source time: `2026-11-18 21:45 UTC`.
- Original normalized time: `2026-11-18T21:45:00Z`.
- Revised source time: `2026-11-19 23:30 UTC` = `2026-11-20 00:30 CET` = `2026-11-20 08:30 JST`.
- Final normalized time: `2026-11-19T23:30:00Z`.
- Final state: completed at `2026-11-20T00:02:00Z`.
- Sources: `input/04-tickets-export.txt`, `input/05-release-mailbox.txt`, `input/06-change-calendar.txt`, `input/07-deploy-log.txt`, `input/08-bridge-transcript.txt`, `input/09-shift-handoff.txt`, `input/10-ops-digest.txt`.
- Exact quote (`input/04-tickets-export.txt`): `2026-11-16T10:45:00Z | AURORA-R7/TICKETS | AURORA-R7/CHG-448 created: run and record the thirty-minute telemetry watch after AURORA-R7/REL-204-EU; owner AURORA-R7/OWNER-LENA-KOVAC; target 2026-11-18 21:45 UTC.`
- Exact quote (`input/06-change-calendar.txt`): `2026-11-18T22:42:00Z | AURORA-R7/CALENDAR | AURORA-R7/CAL-448 revision 448.3 supersedes revision 448.1: telemetry watch moves to 2026-11-19 23:30 UTC.`
- Exact quote (`input/07-deploy-log.txt`): `2026-11-20T00:02:00Z | AURORA-R7/DEPLOY | AURORA-R7/CHG-448 telemetry watch completed; final state closed by AURORA-R7/OWNER-LENA-KOVAC.`

### 6. `AURORA-R7/TKT-7852`

- Type and action: task; publish the regional release note.
- Owner: `AURORA-R7/OWNER-KASIA-WROBEL`.
- Original and final source deadline: `2026-11-20 10:00 CET`.
- Original and final normalized deadline: `2026-11-20T09:00:00Z`.
- Final state: completed at `2026-11-20T09:12:00Z`, twelve minutes after the deadline.
- Sources: `input/02-release-chat-cet.txt`, `input/04-tickets-export.txt`, `input/05-release-mailbox.txt`, `input/09-shift-handoff.txt`, `input/10-ops-digest.txt`.
- Exact quote (`input/02-release-chat-cet.txt`): `2026-11-17T09:00:00+01:00 | AURORA-R7/CHAT-CET | AURORA-R7/OWNER-KASIA-WROBEL: AURORA-R7/TKT-7852 is mine: publish the regional release note by 2026-11-20 10:00 CET, 09:00 UTC.`
- Exact quote (`input/05-release-mailbox.txt`): `2026-11-20T09:12:00Z | AURORA-R7/MAILBOX | AURORA-R7/MAIL-1060 from AURORA-R7/OWNER-KASIA-WROBEL: I published the regional release note for AURORA-R7/TKT-7852 at 10:12 CET; the ticket is complete.`

## Chronology and lifecycle changes

1. On 2026-11-16, the two release windows, three tasks, and the dependent telemetry watch are created or booked.
2. On 2026-11-18, `AURORA-R7/TKT-7811` is reassigned from Piotr to Elena and moved from `2026-11-18T15:00:00Z` to `2026-11-19T11:00:00Z`.
3. The original EU trigger at `2026-11-18T21:00:00Z` does not start because the partner route is held.
4. At `2026-11-18T22:14:00Z` (`2026-11-19 07:14 JST`), the late JST message moves only `AURORA-R7/REL-204-EU`. Mail confirms it at `22:20Z`; calendar revision 441.4 records it at `22:30Z`.
5. `AURORA-R7/TKT-7811` completes at `2026-11-19T09:42:00Z`.
6. `AURORA-R7/REL-204-EU` starts at `2026-11-19T22:30:00Z` and completes at `23:18Z`. Its dependent `AURORA-R7/CHG-448` starts at `23:30Z` and completes at `2026-11-20T00:02:00Z`.
7. `AURORA-R7/TKT-7852` completes at `2026-11-20T09:12:00Z`.
8. The independent `AURORA-R7/REL-204-JP` starts at `2026-11-20T13:00:00Z` and completes at `13:47Z`.

Lifecycle changes that must be applied include:

- `AURORA-R7/REL-204-EU`: scheduled -> missed original slot -> rescheduled -> completed.
- `AURORA-R7/TKT-7811`: open with Piotr -> open with Elena and a new deadline -> completed.
- `AURORA-R7/CHG-448`: scheduled -> rescheduled with its parent release -> completed.
- `AURORA-R7/TKT-7852`: open -> completed after its deadline.
- `AURORA-R7/REL-204-JP`: scheduled -> completed, without inheriting the EU reschedule.

## Mechanism coverage

- `M01`: extract six release, task, and dependent-watch records with their fields.
- `M03`: merge the EU release, the rollback rehearsal, and the telemetry watch across source files.
- `M04`: keep the EU blue ring and JP green ring separate despite the shared `204` build family and artifact count.
- `M05`: apply the EU window move, the rehearsal deadline move, and the dependent watch move.
- `M06`: apply completion evidence for both releases, the rehearsal, the watch, and the regional note.
- `M08`: resolve `@maya`/`伊藤` and apply the Piotr-to-Elena reassignment.
- `M09`: normalize UTC, CET, and JST and preserve the date change across midnight.
- `M11`: prefer the later explicit JST/mail/calendar revisions over the stale original calendar and archived quote.
- `M13`: preserve the empty assignee for `AURORA-R7/TKT-7824`.

## Required merge and required separation

- Cross-file merge: the original EU booking in `01-release-chat-utc.txt`, the late JST update in `03-release-chat-jst.txt`, the UTC/CET/JST confirmation in `05-release-mailbox.txt`, calendar revision 441.4, and the deployment log all update the single record `AURORA-R7/REL-204-EU`.
- The old and new EU times must not produce two release records. The newer, explicit, cross-zone update wins.
- Similar pair that stays separate: `AURORA-R7/REL-204-EU`/`AURORA-R7/CHG-441`/EU blue ring/Maya and `AURORA-R7/REL-204-JP`/`AURORA-R7/CHG-447`/JP green ring/Kenji are two release records. Matching build number `204`, matching artifact count `312`, and nearby times do not merge them.
- `AURORA-R7/TKT-7811` evidence also merges across CET chat, ticket export, email acceptance, handoff, and final digest. Reassignment updates its owner; it does not create a second task.

## Exact positive assertions

1. The registry contains exactly the six records listed above.
2. `AURORA-R7/REL-204-EU` has final normalized window `2026-11-19T22:30:00Z`, not its original `2026-11-18T21:00:00Z`.
3. `AURORA-R7/REL-204-EU` is completed and owned by `AURORA-R7/OWNER-MAYA-ITO`.
4. `@maya` and `伊藤` resolve to `AURORA-R7/OWNER-MAYA-ITO` only.
5. `AURORA-R7/REL-204-JP` remains a separate record at `2026-11-20T13:00:00Z` and is completed under `AURORA-R7/OWNER-KENJI-SATO`.
6. The EU reschedule does not change the JP time, owner, bridge, or change record.
7. `AURORA-R7/TKT-7811` has final owner `AURORA-R7/OWNER-ELENA-PARK`, final deadline `2026-11-19T11:00:00Z`, and final state completed.
8. `AURORA-R7/TKT-7824` is open, due `2026-11-20T16:00:00Z`, and has no owner.
9. The watcher list on `AURORA-R7/TKT-7824` does not fill its owner field.
10. `AURORA-R7/CHG-448` follows the EU reschedule to `2026-11-19T23:30:00Z` and ends completed.
11. `AURORA-R7/TKT-7852` is completed by `AURORA-R7/OWNER-KASIA-WROBEL` at `2026-11-20T09:12:00Z`, after its `09:00Z` deadline.
12. Evidence from later timestamps and explicit record identifiers overrides stale calendar and quoted-history text.

## Exact negative checks

Each check names the noise class, the exact input fragment, and the false output that must not appear.

1. `N01` ordinary metric. Source `input/01-release-chat-utc.txt`: `2026-11-16T08:03:00Z | AURORA-R7/CHAT-UTC | AURORA-R7/OWNER-OMAR-REED: AURORA-R7/METRIC-EDGE shows cache hit rate 97.4% and 42 cold keys.` This must not create a cache-remediation task, owner deadline, or release event.
2. `N01` ordinary status. Source `input/10-ops-digest.txt`: `2026-11-20T15:00:00Z | AURORA-R7/DIGEST | Partner route capacity is 79 percent.` This must not create a capacity commitment or a 79-unit deadline.
3. `N03` quoted history. Source `input/05-release-mailbox.txt`: `2026-11-16T07:59:00Z | AURORA-R7/MAILBOX | AURORA-R7/MAIL-1007 quoted body: > 2026-10-02: ship AURORA-R7/REL-188-EU by 18:00 UTC after approval AURORA-R7/CHG-390.` This must not create a current `AURORA-R7/REL-188-EU` record, and it must not merge into either 204 release.
4. `N04` version-like date. Source `input/02-release-chat-cet.txt`: `2026-11-17T08:48:00+01:00 | AURORA-R7/CHAT-CET | AURORA-R7/OWNER-PIOTR-NOWAK: The rollback script printed build 2026.11.19 as its version label.` This must not create a deadline on 2026-11-19.
5. `N04` document date. Source `input/02-release-chat-cet.txt`: `2026-11-17T11:24:00+01:00 | AURORA-R7/CHAT-CET | AURORA-R7/OWNER-KASIA-WROBEL: The footer date 17.11.2026 is the document revision date.` This must not create a task or event on 2026-11-17.
6. `N04` build identifier. Source `input/10-ops-digest.txt`: `2026-11-20T14:12:00Z | AURORA-R7/DIGEST | AURORA-R7/BUILD-204.7.19 is the active build label in both regions.` This must not merge the EU and JP release records and must not create a seventh release.
7. `N09` automated metadata. Source `input/07-deploy-log.txt`: `2026-11-18T21:33:00Z | AURORA-R7/DEPLOY | alert AURORA-R7/ALERT-ROUTE state=watch expires=2026-11-21T03:00:00Z.` The expiry is alert metadata, not a task deadline or event.
8. `N09` retry log. Source `input/06-change-calendar.txt`: `2026-11-18T21:14:00Z | AURORA-R7/CALENDAR | Calendar service retry 1 returned sync status 503 for AURORA-R7/CAL-441.` This must not create a repair ticket assigned to the calendar owner.
9. `N10` side conversation. Source `input/02-release-chat-cet.txt`: `2026-11-17T08:44:00+01:00 | AURORA-R7/CHAT-CET | AURORA-R7/OWNER-KASIA-WROBEL: Lunch at 12:30 CET? The small kitchen has pierogi today.` This must not create a lunch event or catering task.
10. `N10` lost-object chat. Source `input/01-release-chat-utc.txt`: `2026-11-16T11:20:00Z | AURORA-R7/CHAT-UTC | AURORA-R7/OWNER-NORA-VALE: Someone left a blue notebook in room AURORA-R7/ROOM-3.` This must not create a notebook-retrieval task.

## Meaningful absence and context ratio

- Meaningful absence: `AURORA-R7/TKT-7824` has an explicitly empty assignee at the reference time. Do not select Maya, Nora, Lena, or either watcher as owner.
- Conservative context count: 124 of 500 lines mention one of the six final record IDs or their linked `AURORA-R7/CHG-441`/`AURORA-R7/CHG-447` identities. Reserve the separate alias-mapping line as positive evidence too. The other 375 lines, or 75.0%, are natural operational context or noise that is not needed for the positive records. Redundant status lines among the 125 reserved lines make the true nonessential share larger, but the 75.0% lower bound is sufficient.
