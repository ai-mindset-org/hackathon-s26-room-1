# T004 — NORTHSTAR-INC support incident

Reference clock: `2027-08-19T18:30:00Z`.
Locale: `en-US`.
Zones: audit and system timestamps use `UTC`; customer commitments use US Pacific time. On these August dates, Pacific time is `PDT` (`UTC-07:00`).
Input order is not authority. Event time and explicit identity determine the chronology.
All names, addresses, organizations, tickets, and identifiers in this scenario are synthetic, fictional, and public-safe.

## Chronology

1. `NORTHSTAR-INC/7421` opened for `NORTHSTAR-INC/LumenBay-West` at `2027-08-18T14:10:00Z`. It was assigned to Mira Chen, whose agent alias is `M.C.`.
2. Mira created a next-day customer-summary action due `2027-08-19 11:00 PDT` (`2027-08-19T18:00:00Z`).
3. `NORTHSTAR-INC/7421` was resolved as mitigated at `2027-08-18T18:05:00Z` after a customer confirmation.
4. A separate `NORTHSTAR-INC/7422` opened for `NORTHSTAR-INC/LumenBay-East` at `2027-08-18T19:04:00Z` and was resolved at `2027-08-18T21:15:00Z` after an email-template rollback.
5. The customer sent `NORTHSTAR-INC/MAIL-IN-2048` at `2027-08-19T15:12:00Z` (`08:12 PDT`). The gateway imported it at `2027-08-19T16:42:37Z`. It names ticket `7421`, the West workspace, and a returned retry-worker symptom.
6. The explicit update at `2027-08-19T16:47:00Z` reopened `NORTHSTAR-INC/7421`. The alert clear at `16:01 UTC` is earlier metric evidence and cannot override this later customer evidence.
7. Diego Rios accepted ownership from `M.C.` at `16:49 UTC`. The handoff later moved the customer-summary deadline to `12:00 PDT` (`19:00 UTC`) and assigned it to Diego.
8. `NORTHSTAR-INC/Status-Desk` published the corrected `7421` status note at `11:20 PDT` (`18:20 UTC`).
9. The handoff at `18:25 UTC` is the latest explicit state summary before the reference clock.

## Required final records

### R1 — NORTHSTAR-INC/7421 West retry incident

- Type: incident.
- Identity/scope: `NORTHSTAR-INC/7421`, `NORTHSTAR-INC/LumenBay-West`, `NORTHSTAR-INC/Relay-Attachments`.
- Final owner: Diego Rios. Earlier owner/alias: Mira Chen / `M.C.`.
- Final state: reopened and active.
- Deadline: absent. Do not invent a resolution deadline from an alert window, SLA target, sample timestamp, or another task.
- Lifecycle: open → resolved at `2027-08-18T18:05:00Z` → reopened at `2027-08-19T16:47:00Z`; owner Mira Chen / `M.C.` → Diego Rios at `16:49 UTC`.
- Sources and exact quotes:
  - `input/01-support-ticket.txt`: `M.C. 18:05 UTC: Resolve NORTHSTAR-INC/7421 as mitigated at 2027-08-18 18:05 UTC.`
  - `input/03-late-customer-email.eml`: `“Los archivos adjuntos vuelven a quedarse en procesando para el espacio Oeste.”`
  - `input/03-late-customer-email.eml`: `“El espacio Este sigue funcionando; este correo corresponde a NORTHSTAR-INC/7421.”`
  - `input/02-agent-chat.log`: `[2027-08-19 16:47 UTC] Mira Chen: The delayed email names NORTHSTAR-INC/LumenBay-West and NORTHSTAR-INC/7421. Reopen NORTHSTAR-INC/7421; NORTHSTAR-INC/7422 stays resolved.`
  - `input/07-shift-handoff.md`: `NORTHSTAR-INC/7421 is reopened and assigned to Diego Rios.`

### R2 — NORTHSTAR-INC/7422 East email-preview incident

- Type: incident.
- Identity/scope: `NORTHSTAR-INC/7422`, `NORTHSTAR-INC/LumenBay-East`, `NORTHSTAR-INC/Relay-Email-Preview`.
- Owner: Priya Shah.
- Final state: resolved.
- Deadline: absent.
- This record is separate from R1 even though both reports use similar attachment symptom language.
- Sources and exact quotes:
  - `input/02-agent-chat.log`: `[2027-08-18 19:04 UTC] Priya Shah: Open NORTHSTAR-INC/7422 for NORTHSTAR-INC/LumenBay-East and assign it to Priya Shah.`
  - `input/02-agent-chat.log`: `[2027-08-18 21:15 UTC] Priya Shah: Resolve NORTHSTAR-INC/7422; its email-preview path is healthy after the template rollback.`
  - `input/07-shift-handoff.md`: `NORTHSTAR-INC/7422 remains resolved under Priya Shah.`

### R3 — Send the NORTHSTAR-INC/7421 next customer summary

- Type: action.
- Owner: Diego Rios. Original owner: Mira Chen / `M.C.`.
- Final state: open.
- Original deadline: `August 19 at 11:00 PDT` → `2027-08-19T18:00:00Z`.
- Final deadline: `12:00 PDT today` → `2027-08-19T19:00:00Z`.
- Sources and exact quotes:
  - `input/01-support-ticket.txt`: `M.C. 17:27 UTC: M.C. will send the next-day customer summary by August 19 at 11:00 PDT.`
  - `input/07-shift-handoff.md`: `The next customer summary moved from 11:00 PDT to 12:00 PDT today; Diego Rios owns it.`

### R4 — Correct the NORTHSTAR-INC/7421 public status note

- Type: action.
- Owner: `NORTHSTAR-INC/Status-Desk`.
- Final state: completed at `2027-08-19T18:20:00Z`.
- Original deadline: `August 19 at 10:30 PDT` → `2027-08-19T17:30:00Z`.
- Sources and exact quotes:
  - `input/02-agent-chat.log`: `[2027-08-18 18:22 UTC] Mira Chen: NORTHSTAR-INC/Status-Desk owns a corrected NORTHSTAR-INC/7421 status note by August 19 at 10:30 PDT.`
  - `input/04-status-page.md`: `Published the corrected NORTHSTAR-INC/7421 status note at 11:20 PDT.`

### R5 — NORTHSTAR-INC/7421 learning review

- Type: event.
- Final state: scheduled.
- Original time: `August 21 at 10:00 PDT`.
- Normalized time: `2027-08-21T17:00:00Z`.
- Owner/facilitator: absent and unknown. The participant list and Diego’s act of scheduling do not assign the role.
- Sources and exact quotes:
  - `input/06-postmortem-transcript.txt`: `Diego 17:24: The NORTHSTAR-INC/7421 learning review is scheduled for August 21 at 10:00 PDT.`
  - `input/06-postmortem-transcript.txt`: `Mira 17:25: A facilitator has not been assigned for that review.`

### R6 — Deliver the NORTHSTAR-INC/7421 retry-key comparison

- Type: preparation action for R5, not the review event itself.
- Owner: Leena Park.
- Final state: open.
- Original deadline: `August 20 at 16:00 PDT`.
- Normalized deadline: `2027-08-20T23:00:00Z`.
- Source and exact quote:
  - `input/06-postmortem-transcript.txt`: `Leena 17:26: Leena Park will deliver the retry-key comparison by August 20 at 16:00 PDT.`

### R7 — Validate the NORTHSTAR-INC/7421 retry backlog

- Type: action.
- Owner: `NORTHSTAR-INC/SRE-West` group.
- Final state: open.
- Original deadline: `August 20 at 09:00 PDT`.
- Normalized deadline: `2027-08-20T16:00:00Z`.
- The alert log supplies the metric context, while the handoff creates the owned action.
- Sources and exact quotes:
  - `input/05-alert-log.txt`: `2027-08-19T16:01:04Z level=info alert=NORTHSTAR-INC/AL-991 state=cleared queue_depth=11 oldest_age_s=37`
  - `input/07-shift-handoff.md`: `NORTHSTAR-INC/SRE-West owns the backlog validation for NORTHSTAR-INC/7421 by August 20 at 09:00 PDT.`

## Lifecycle changes and interaction checks

1. R1 changes from resolved to reopened because the later imported email explicitly identifies `7421`, West, and the retry path.
2. R1 changes owner from Mira Chen / `M.C.` to Diego Rios.
3. R3 changes owner from Mira Chen / `M.C.` to Diego Rios and moves from `11:00 PDT` to `12:00 PDT`.
4. R4 changes from open to completed after the status-page publication.
5. `M03+M06+M11`: merge the ticket, late email, chat, alert, and handoff into R1. The late email reopens R1 after the earlier resolution and after the alert clear.
6. `M04`: R2 stays a separate resolved incident. East uses a preview renderer and West uses a retry worker.
7. `M02`: R5 is the scheduled review at `2027-08-21T17:00:00Z`; R6 is a separate preparation action due `2027-08-20T23:00:00Z`.
8. `M13`: keep R1 and R2 deadlines absent and keep R5’s facilitator absent.

## Exact positive assertions

1. Produce exactly seven final records, R1–R7.
2. Merge all explicit `7421` state evidence into one incident record, not one record per file.
3. Set R1 to reopened, not resolved, from the `16:47 UTC` explicit update.
4. Set R1’s final owner to Diego Rios and resolve `M.C.` to Mira Chen as the earlier owner.
5. Keep R1’s incident deadline absent.
6. Keep R2 separate, resolved, and owned by Priya Shah.
7. Update R3’s owner and deadline to Diego Rios and `2027-08-19T19:00:00Z`.
8. Mark R4 completed at `2027-08-19T18:20:00Z`.
9. Normalize R5 to `2027-08-21T17:00:00Z` and keep its facilitator unknown.
10. Keep R6 separate from R5, with Leena Park and `2027-08-20T23:00:00Z`.
11. Create R7 with group owner `NORTHSTAR-INC/SRE-West` and deadline `2027-08-20T16:00:00Z`.
12. Treat the alert clear as a metric-window change that predates the late email, not as the final incident state.

## Specific negative checks

1. **N03 forwarded history:** From `input/01-support-ticket.txt`, the quoted `NORTHSTAR-INC/7310` checksum comparison must not become a current task or merge with R1.
2. **N03 forwarded history:** From `input/03-late-customer-email.eml`, the quoted 2027-08-18 resolution must not override the later email body or leave R1 resolved.
3. **N03 forwarded history:** From `input/06-postmortem-transcript.txt`, the 2026 `NORTHSTAR-INC/Legacy-55` cache-key chart must not become a current record.
4. **N04 numeric/version noise:** `4.18.7-r2`, `9.6.1`, `9.6.0`, `2.4 MB`, `3.1 MB`, and `864 KB` must not become deadlines, owners, or standalone records.
5. **N04 numeric noise:** `38 active seats`, `27 documents`, `19 remaining documents`, and `4,812 views` must not become obligations or event times.
6. **N09 alert metadata:** `queue_depth=481`, `retention_days=30`, and the `16:01:04Z` alert clear must not create standalone actions or resolve R1.
7. **N09 alert metadata:** Alert `NORTHSTAR-INC/AL-988` and digest `NORTHSTAR-INC/DIGEST-119` must not merge R2 into R1.
8. **N01 ordinary status:** Fresh-upload latency, page-render latency, satisfaction ratings, queue counts, and CPU/memory readings must not create actions.
9. **N01 ordinary status:** The automatic queue snapshot at `18:30 UTC` in `input/07-shift-handoff.md` must not become an owned event or deadline.
10. **N10 side discussion:** The café soup, blue rain jacket, lunch order, floor map, and refrigerator temperature must not create records.
11. The question `Could your team review why the retry keys are being accepted twice?` must not create an owner or deadline; R7 comes only from the later explicit handoff assignment.
12. The participant list in `input/06-postmortem-transcript.txt` must not assign a facilitator or owner to R5.

## Natural-context accounting

Count all nonblank physical lines in the seven input files. Direct positive evidence is limited to the explicit creation, update, assignment, completion, event, and deadline lines cited above plus their immediate identity headers. A conservative manual classification counts 44 direct positive-evidence lines and 233 natural context or negative-test lines out of 277 nonblank lines. The natural non-evidence share is therefore `233 / 277 = 84.1%`.
