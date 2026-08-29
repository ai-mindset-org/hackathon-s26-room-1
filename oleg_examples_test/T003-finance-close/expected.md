# T003 — MERIDIAN-CLOSE finance close

## Evaluation frame

- Reference clock: `2028-04-06T12:00:00Z`.
- Default language: English. Source locale controls each quoted date and number.
- `controller-mail.eml`, `team-chat.txt`, and the US calendar view use `en-US`, `MM/DD/YYYY`, and `America/New_York`. These April and May timestamps are EDT (`UTC-04:00`).
- `reconciliation-minutes.txt`, `approval-log.txt`, and the EU invoice section use `en-IE`, `DD/MM/YYYY`, and `Europe/Paris`. These timestamps are CEST (`UTC+02:00`).
- Chronology follows the timestamp written in each source. File order does not override a later timestamp. A later authoritative controller message or approval transition overrides an earlier calendar snapshot or workflow state for the same exact object. A calendar event whose normalized start is after the reference clock remains an upcoming final record unless a later source cancels or supersedes it.
- Number examples remain source-specific: `$1,240.50` is one thousand two hundred forty US dollars and `1.240,50 EUR` is one thousand two hundred forty euros.

## Final register — 7 records

### 1. `MERIDIAN-CLOSE/ACCRUAL-IC/MAR-2028`

- Action: finish the March 2028 intercompany accrual review.
- Owner: Lena Hart. `LH` is the explicit alias.
- Original deadline: `04/04/2028 5:00 PM ET` = `2028-04-04T21:00:00Z`.
- Updated deadline: `04/05/2028 12:00 PM ET` = `2028-04-05T16:00:00Z`.
- Final state: completed at `04/05/2028 12:18 PM ET` = `2028-04-05T16:18:00Z`.
- Lifecycle: scheduled → rescheduled for this occurrence only → completed.
- Sources and exact quotes:
  - `close-calendar.txt`: `Occurrence key: MERIDIAN-CLOSE/ACCRUAL-IC/MAR-2028`
  - `close-calendar.txt`: `Due: 04/04/2028 5:00 PM ET`
  - `controller-mail.eml`: `Move only MERIDIAN-CLOSE/ACCRUAL-IC/MAR-2028 to 04/05/2028 12:00 PM ET.`
  - `controller-mail.eml`: `LH remains the owner of that March occurrence.`
  - `team-chat.txt`: `[04/05/2028 12:18 ET] Lena Hart: MERIDIAN-CLOSE/ACCRUAL-IC/MAR-2028 is complete; I filed the signed review at 12:18 PM ET.`
  - `approval-log.txt`: `05/04/2028 18:18 CEST | MERIDIAN-CLOSE/ACCRUAL-IC/MAR-2028 | LH | COMPLETED | signed review filed at 05/04/2028 12:18 ET`

### 2. `MERIDIAN-CLOSE/ACCRUAL-IC/APR-2028`

- Action: finish the April 2028 intercompany accrual review.
- Owner: Lena Hart (`LH`).
- Original and final deadline: `05/03/2028 5:00 PM ET` = `2028-05-03T21:00:00Z`.
- Final state: open and scheduled. It is a separate occurrence of the recurring control.
- Lifecycle: scheduled; unchanged by the March exception.
- Sources and exact quotes:
  - `close-calendar.txt`: `Occurrence key: MERIDIAN-CLOSE/ACCRUAL-IC/APR-2028`
  - `close-calendar.txt`: `Due: 05/03/2028 5:00 PM ET`
  - `controller-mail.eml`: `Do not move the April occurrence; MERIDIAN-CLOSE/ACCRUAL-IC/APR-2028 stays at 05/03/2028 5:00 PM ET.`

### 3. `MERIDIAN-CLOSE/BANK-EU-0441`

- Action: reconcile the EU payroll clearing account ending 0441.
- Owner: Owen Vale. `OV` is the explicit alias.
- Original and final deadline: `05/04/2028 16:00 CEST` = `2028-04-05T14:00:00Z`.
- Final state: completed and approved at `05/04/2028 15:42 CEST` = `2028-04-05T13:42:00Z`.
- Lifecycle: open match → submitted → returned → resubmitted → completed and approved.
- Sources and exact quotes:
  - `reconciliation-minutes.txt`: `MERIDIAN-CLOSE/BANK-EU-0441 concerns the payroll clearing account ending 0441.`
  - `reconciliation-minutes.txt`: `OV owns the reconciliation for MERIDIAN-CLOSE/BANK-EU-0441.`
  - `reconciliation-minutes.txt`: `Its deadline is 05/04/2028 16:00 CEST.`
  - `approval-log.txt`: `05/04/2028 15:03 CEST | MERIDIAN-CLOSE/BANK-EU-0441 | Celia Moss | RETURNED | attachment label lacked account suffix`
  - `approval-log.txt`: `05/04/2028 15:42 CEST | MERIDIAN-CLOSE/BANK-EU-0441 | Celia Moss | APPROVED | reconciliation complete`

### 4. `MERIDIAN-CLOSE/BANK-EU-0447`

- Action: investigate the EU benefits clearing difference of `2.104,60 EUR` for account ending 0447.
- Owner: unknown. Do not assign Owen Vale, Celia Moss, Rowan Pike, or another attendee.
- Original deadline: absent.
- Normalized deadline: absent.
- Final state: open and under investigation.
- This is the required meaningful absence. The input explicitly records that no participant accepted ownership and that the minutes record no deadline.
- Sources and exact quotes:
  - `reconciliation-minutes.txt`: `MERIDIAN-CLOSE/BANK-EU-0447 concerns the benefits clearing account ending 0447.`
  - `reconciliation-minutes.txt`: `The 0447 difference is 2.104,60 EUR and remains under investigation.`
  - `reconciliation-minutes.txt`: `No participant accepted ownership of MERIDIAN-CLOSE/BANK-EU-0447 during the meeting.`
  - `reconciliation-minutes.txt`: `The minutes record no deadline for MERIDIAN-CLOSE/BANK-EU-0447.`

### 5. `MERIDIAN-CLOSE/JE-APR-17`

- Action: post the April FX journal using rate set `MERIDIAN-CLOSE/RATE-APR-A`, revision 17.
- Original owner: Oliver Crane.
- Final owner: Priya Stone (`PS`).
- Original deadline: `04/05/2028 2:00 PM ET` = `2028-04-05T18:00:00Z`.
- Updated deadline: `04/06/2028 10:00 AM ET` = `2028-04-06T14:00:00Z`.
- Final state: completed and approved at `06/04/2028 15:31 CEST` = `2028-04-06T13:31:00Z`.
- Lifecycle: assigned to Oliver Crane → reassigned to Priya Stone → rescheduled → submitted → completed and approved.
- Sources and exact quotes:
  - `controller-mail.eml`: `MERIDIAN-CLOSE/JE-APR-17 was in Oliver Crane's queue with a 04/05/2028 2:00 PM ET deadline.`
  - `controller-mail.eml`: `Lena reassigned MERIDIAN-CLOSE/JE-APR-17 to me, Priya Stone (PS), at 04/05/2028 1:35 PM ET.`
  - `controller-mail.eml`: `The revised deadline is 04/06/2028 10:00 AM ET.`
  - `approval-log.txt`: `05/04/2028 19:35 CEST | MERIDIAN-CLOSE/JE-APR-17 | Lena Hart | REASSIGNED | Oliver Crane to Priya Stone (PS); effective 05/04/2028 13:35 ET`
  - `approval-log.txt`: `06/04/2028 15:31 CEST | MERIDIAN-CLOSE/JE-APR-17 | Lena Hart | APPROVED | journal posted; complete`

### 6. `MERIDIAN-CLOSE/INV-US-7742`

- Action: release the held invoice after tax validation.
- Owner: Mara Quill.
- Original and final deadline: `04/06/2028 3:00 PM ET` = `2028-04-06T19:00:00Z`.
- Final state: open. Tax validation and release are not yet recorded as complete.
- Sources and exact quotes:
  - `invoice-export.txt`: `MERIDIAN-CLOSE/INV-US-7742 | MERIDIAN-CLOSE/VENDOR-GLASS-05 | 04/02/2028 | 03/29/2028 | USD | 1,240.50 | HOLD | TAX-VALIDATE`
  - `controller-mail.eml`: `Mara Quill owns release of MERIDIAN-CLOSE/INV-US-7742 after tax validation.`
  - `controller-mail.eml`: `Complete that release by 04/06/2028 3:00 PM ET.`

### 7. `MERIDIAN-CLOSE/DASHBOARD-DEMO/0406`

- Type and action: attend the scheduled finance dashboard layout review.
- Owner/host: absent. The calendar owner names the calendar, not an owner or host for this event.
- Original and final interval: `04/06/2028 11:30 AM ET` to `04/06/2028 12:00 PM ET`.
- Normalized interval: `2028-04-06T15:30:00Z` to `2028-04-06T16:00:00Z`. `America/New_York` is EDT (`UTC-04:00`) on this date.
- Final state: upcoming and scheduled at the reference clock. No later source cancels or supersedes it.
- Lifecycle: scheduled; unchanged.
- Sources and exact quotes:
  - `close-calendar.txt`: `EVENT MERIDIAN-CLOSE/DASHBOARD-DEMO/0406`
  - `close-calendar.txt`: `Title: Finance dashboard layout review`
  - `close-calendar.txt`: `Start: 04/06/2028 11:30 AM ET`
  - `close-calendar.txt`: `End: 04/06/2028 12:00 PM ET`
  - `close-calendar.txt`: `Room: MERIDIAN-CLOSE/Virtual-Room-3`

## Required interactions and lifecycle checks

1. `M03 + M05 + M12`: merge the March calendar occurrence with the later controller mail, chat completion, and approval row. Move only `MERIDIAN-CLOSE/ACCRUAL-IC/MAR-2028`. Keep `MERIDIAN-CLOSE/ACCRUAL-IC/APR-2028` as another final record with its unchanged May deadline.
2. `M03 + M04 + M11`: merge the minutes and approval transitions for account 0441. Do not merge account 0447, even though both descriptions begin alike and both appear in the same meeting.
3. `M06 + M11`: the returned 0441 submission is not the final state. The later resubmission and approval make it completed.
4. `M08 + M11`: the cached old FX queue does not override the timestamped reassignment and live approval log. Final owner is Priya Stone (`PS`), not Oliver Crane.
5. `M09`: interpret `04/05/2028` in US sources as April 5, but `05/04/2028` in EU sources as April 5. Apply the named source zone before UTC normalization.
6. `M13`: preserve the missing owner and deadline on account 0447.
7. `M01 + M09`: retain `MERIDIAN-CLOSE/DASHBOARD-DEMO/0406` as a separate upcoming calendar event. Its `04/06/2028 11:30 AM ET` start normalizes to `2028-04-06T15:30:00Z`, which is after the reference clock.

## Exact positive assertions

1. The final register has exactly seven records.
2. The March and April accrual reviews are two period-specific records under one recurring control.
3. Only the March accrual deadline changes from April 4 to April 5.
4. The April accrual deadline remains May 3 at 5:00 PM ET.
5. The March accrual review ends completed under Lena Hart (`LH`).
6. The 0441 reconciliation ends approved under Owen Vale (`OV`) despite its earlier returned state.
7. The 0447 reconciliation remains open with no owner and no deadline.
8. Accounts 0441 and 0447 remain separate records.
9. `MERIDIAN-CLOSE/JE-APR-17` ends assigned to Priya Stone (`PS`), due April 6 at 10:00 AM ET, and completed.
10. Invoice 7742 is the held invoice that Mara Quill must release by April 6 at 3:00 PM ET.
11. Invoice 7743 stays a separate paid export row and is not merged with invoice 7742.
12. `MERIDIAN-CLOSE/DASHBOARD-DEMO/0406` remains a separate upcoming event from `2028-04-06T15:30:00Z` to `2028-04-06T16:00:00Z`.
13. All UTC values use the locale and zone declared by the relevant source.

## Specific negative checks

1. `N01` — `[04/02/2028 08:41 ET] Rowan Pike: Cash dashboard refreshed; bank coverage is 98.7%.` does not create a refresh task or a 98.7 deadline/value field on a record.
2. `N01` — `[04/03/2028 09:05 ET] Priya Stone: The controller pack is 71% complete; disclosure notes are the largest open section.` does not create a disclosure-note task.
3. `N02` — `Archive route: MERIDIAN-CLOSE/FIN-ARCHIVE/2028/Q1/MARCH.` does not create an archive action or assign Lena Hart to one.
4. `N02` — `Quarter-close mailbox: close-team@meridian-close.example` is a signature field, not an owner or action.
5. `N03` — `Please send the old consolidation cover by 03/31/2027 at noon ET.` is quoted 2027 history and does not create a current consolidation task.
6. `N03` — `"OV cleared the old account ending 0441 before 16:00 CEST."` describes 2027 history and does not complete or deadline the 2028 record by itself.
7. `N04` — `MERIDIAN-CLOSE/INV-US-7743 | MERIDIAN-CLOSE/VENDOR-GLASS-05 | 04/02/2028 | 03/29/2028 | USD | 1,240.50 | PAID | ACH-0404` does not create a payment task and must not merge into invoice 7742.
8. `N04` — `MERIDIAN-CLOSE/INV-EU-8814 | MERIDIAN-CLOSE/VENDOR-AMBER-34 | 05/04/2028 | 04/04/2028 | EUR | 118,08 | OPEN | NET15` does not make either date a task deadline.
9. `N04` — `Footer control total EU: 66.773,08 EUR.` does not create a reconciliation or payment record.
10. `N06` — `Enter reviewer initials after the reviewer decision.` is a standing procedure and does not create an assigned reviewer-initials task.
11. `N06` — `Confirm that preparer and reviewer are different people.` is a checklist template, not a new approval record.

## Allowed ambiguity

None for the seven records above. Account 0447 has explicit unknown fields, not an invitation to infer an owner or deadline. The dashboard event has no stated owner or host; this missing field does not remove the scheduled future event from the accepted final register.
