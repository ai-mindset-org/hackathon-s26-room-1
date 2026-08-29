# Expected result — T011 construction/facilities

## Interpretation clock and calendar

- Reference clock: **Friday 18 September 2026, 18:00:00 Europe/Warsaw**.
- Locale: **pl-PL** for Warsaw business-day expressions; English and Polish text are authoritative together.
- Time zone: **Europe/Warsaw**, which is CEST (UTC+02:00) throughout this scenario.
- Business calendar: Monday through Friday. No scenario holiday changes the interval from 7 to 25 September 2026.
- `next Tuesday, 15 September` in the request opened on Monday 7 September means **Tuesday 15 September 2026**. The later phrase `three Warsaw business days after Tuesday 15 September` counts Wednesday 16, Thursday 17, and Friday 18 September.

## Chronology and lifecycle

1. On 7 September, `STONEBRIDGE-FM/WR-418` is opened for `ZONE-E17A`, owned by Piotr Malec, due next Tuesday at 16:00. `WR-481` is opened separately for `ZONE-E17B`, owned by Karol Bednar, due 15 September at 16:00.
2. The 7 September calendar export creates recurring series `VISIT-E17A` for 9, 16, and 23 September. It also links permit request `PERMIT-E17A-0916` to only the 16 September occurrence.
3. On 8 September, Piotr reassigns `WR-418` to Lena Nowak. Lena accepts it and moves its due date three Warsaw business days after 15 September, to 18 September at 16:00.
4. On 9 September, the first `VISIT-E17A` occurrence is completed. The safety meeting creates `SAMPLE-GR18`, due 18 September at 12:00, with no owner.
5. On 10 September, Alicja cancels only the 16 September occurrence and withdraws its linked permit. The 9 September history and the 23 September occurrence remain. `ZONE-E17B` work remains separate and active.
6. On 11 September, Marta Zielinska completes the intake-bay preparation before its 16:00 deadline.
7. On 14 September, delivery `DELIVERY-VK27` occurs and closes. No unloading marshal is ever identified in the sources.
8. On 15 September, Karol completes `WR-481` in `ZONE-E17B`.
9. On 18 September at 12:05, `SAMPLE-GR18` has no owner and no carrier booking, so it is open and overdue at the reference clock. At 14:20 Lena completes `WR-418`. The next active inspection occurrence remains 23 September at 09:00.

## Final register: 7 records

### SB-01 — recurring inspection `STONEBRIDGE-FM/VISIT-E17A`

- Type/action: recurring east plant-room drainage inspection in `STONEBRIDGE-FM/ZONE-E17A`.
- Owner/coordinator: Alicja Krawiec.
- Original dates: `Wednesday 9 September 2026, 09:00-10:30 Europe/Warsaw`; `Wednesday 16 September 2026, 09:00-10:30 Europe/Warsaw`; `Wednesday 23 September 2026, 09:00-10:30 Europe/Warsaw`.
- Normalized dates: `2026-09-09T09:00:00+02:00/2026-09-09T10:30:00+02:00`; `2026-09-16T09:00:00+02:00/2026-09-16T10:30:00+02:00`; `2026-09-23T09:00:00+02:00/2026-09-23T10:30:00+02:00`.
- Final state: series active; 9 September occurrence completed; 16 September occurrence cancelled; 23 September occurrence scheduled. Next occurrence is `2026-09-23T09:00:00+02:00`.
- Sources and exact quotes:
  - `input/04-inspection-calendar.txt`: `Pattern: weekly on Wednesday, three occurrences`
  - `input/04-inspection-calendar.txt`: `Occurrence 2: Wednesday 16 September 2026, 09:00-10:30 Europe/Warsaw`
  - `input/03-contractor-chat.txt`: `[2026-09-10 15:42] Alicja Krawiec: Cancel only the Wednesday 16 September visit in STONEBRIDGE-FM/VISIT-E17A and withdraw STONEBRIDGE-FM/PERMIT-E17A-0916.`
  - `input/03-contractor-chat.txt`: `[2026-09-10 15:46] Alicja Krawiec: Keep the Wednesday 23 September occurrence at 09:00; the 9 September occurrence is already closed.`
  - `input/07-shift-summary.txt`: `16:28 — Calendar desk retained the next STONEBRIDGE-FM/VISIT-E17A occurrence for Wednesday 23 September at 09:00.`

### SB-02 — access permit `STONEBRIDGE-FM/PERMIT-E17A-0916`

- Type/action: prepare the visitor access permit for the 16 September `VISIT-E17A` occurrence.
- Owner: Jakub Wrona.
- Original deadline: `Tuesday 15 September 2026, 12:00 Europe/Warsaw`.
- Normalized deadline: `2026-09-15T12:00:00+02:00`.
- Final state: cancelled/withdrawn on 10 September before issue; no visitor card was printed.
- Sources and exact quotes:
  - `input/04-inspection-calendar.txt`: `Linked access request for occurrence 2: STONEBRIDGE-FM/PERMIT-E17A-0916; preparation cut-off Tuesday 15 September 2026, 12:00 Europe/Warsaw; coordinator Jakub Wrona.`
  - `input/03-contractor-chat.txt`: `[2026-09-10 16:04] Jakub Wrona: Wycofam wniosek 0916 przed wydrukiem karty gościa.`
  - `input/07-shift-summary.txt`: `08:17 — Security confirmed that no visitor card had been printed for STONEBRIDGE-FM/PERMIT-E17A-0916.`

### SB-03 — joint repair `STONEBRIDGE-FM/WR-418`

- Type/action: seal the expansion joint beside drain channel E-4 in `STONEBRIDGE-FM/ZONE-E17A` and record the cured surface.
- Original owner: Piotr Malec. Final owner: Lena Nowak.
- Original deadline: `next Tuesday, 15 September, before the 16:00 shift handover`, written Monday 7 September 2026.
- Original normalized deadline: `2026-09-15T16:00:00+02:00`.
- Updated deadline: `three Warsaw business days after Tuesday 15 September`.
- Updated normalized deadline: `2026-09-18T16:00:00+02:00`.
- Final state: completed by Lena Nowak at `2026-09-18T14:20:00+02:00`, before the updated deadline.
- Sources and exact quotes:
  - `input/02-work-requests.txt`: `Requested work: Seal the expansion joint beside drain channel E-4 and record the cured surface condition.`
  - `input/02-work-requests.txt`: `Requested finish: next Tuesday, 15 September, before the 16:00 shift handover.`
  - `input/03-contractor-chat.txt`: `[2026-09-08 08:12] Piotr Malec: Przekazuję STONEBRIDGE-FM/WR-418 Lenie Nowak; ona przejmuje uszczelnienie w STONEBRIDGE-FM/ZONE-E17A.`
  - `input/03-contractor-chat.txt`: `[2026-09-08 08:16] Lena Nowak: Przyjmuję STONEBRIDGE-FM/WR-418. Przesuńcie termin o trzy warszawskie dni robocze po wtorku 15 września.`
  - `input/07-shift-summary.txt`: `14:20 — Lena Nowak sealed the expansion joint under STONEBRIDGE-FM/WR-418 in STONEBRIDGE-FM/ZONE-E17A; work closed.`

### SB-04 — occupancy sensor `STONEBRIDGE-FM/WR-481`

- Type/action: replace the occupancy sensor above door E17B-2 in `STONEBRIDGE-FM/ZONE-E17B` and record the final switch-off delay.
- Owner: Karol Bednar.
- Original deadline: `Tuesday 15 September 2026 at 16:00 Europe/Warsaw`.
- Normalized deadline: `2026-09-15T16:00:00+02:00`.
- Final state: completed at `2026-09-15T15:35:00+02:00`; measured switch-off delay is 42 seconds.
- Sources and exact quotes:
  - `input/02-work-requests.txt`: `Requested work: Replace the occupancy sensor above door E17B-2 and record the final switch-off delay.`
  - `input/02-work-requests.txt`: `Required finish: Tuesday 15 September 2026 at 16:00 Europe/Warsaw.`
  - `input/07-shift-summary.txt`: `15:35 — Karol Bednar replaced and tested the occupancy sensor under STONEBRIDGE-FM/WR-481 in STONEBRIDGE-FM/ZONE-E17B; work closed.`

### SB-05 — valve-kit delivery `STONEBRIDGE-FM/DELIVERY-VK27`

- Type/event: delivery of twelve valve kits and four gasket boxes to intake bay 2.
- Owner: **unknown**. The supplier is the sender, but the receiving/unloading marshal is not named.
- Original date: `Monday, 14 September 2026 at 10:30 CEST`.
- Normalized date: `2026-09-14T10:30:00+02:00`.
- Final state: completed/received at `2026-09-14T10:42:00+02:00`.
- Sources and exact quotes:
  - `input/05-supplier-email.eml`: `Delivery STONEBRIDGE-FM/DELIVERY-VK27 is confirmed for Monday, 14 September 2026 at 10:30 CEST.`
  - `input/05-supplier-email.eml`: `The unloading marshal has not yet been named by Stonebridge.`
  - `input/07-shift-summary.txt`: `10:42 — STONEBRIDGE-FM/DELIVERY-VK27 was received at intake bay 2; the event is closed.`

### SB-06 — intake-bay preparation `STONEBRIDGE-FM/PREP-BAY2`

- Type/action: clear intake bay 2 before `DELIVERY-VK27`.
- Owner: Marta Zielinska, also written as `M. Zielinska`.
- Original deadline: `16:00 on the previous Warsaw business day` before Monday 14 September 2026.
- Normalized deadline: `2026-09-11T16:00:00+02:00` (Friday, not Sunday).
- Final state: completed at `2026-09-11T15:45:00+02:00`.
- Sources and exact quotes:
  - `input/05-supplier-email.eml`: `Please have intake bay 2 cleared by 16:00 on the previous Warsaw business day; M. Zielinska confirmed she will own that preparation.`
  - `input/05-supplier-email.eml`: `Monday morning works for the bay team. I can clear bay 2 on the prior working day.`
  - `input/07-shift-summary.txt`: `15:45 — M. Zielinska cleared intake bay 2 for STONEBRIDGE-FM/DELIVERY-VK27; preparation STONEBRIDGE-FM/PREP-BAY2 is complete.`

### SB-07 — grout sample collection `STONEBRIDGE-FM/SAMPLE-GR18`

- Type/action: book collection of the cured grout sample from `ZONE-E17A`.
- Owner: **unknown/unassigned**. Do not guess Facilities, Vistula Build, Alicja Krawiec, or Ewa Borowska.
- Original deadline: `Friday 18 September 2026 at 12:00 CEST`.
- Normalized deadline: `2026-09-18T12:00:00+02:00`.
- Final state: open and overdue at the reference clock; no carrier booking is recorded.
- Sources and exact quotes:
  - `input/06-safety-minutes.txt`: `Book collection of sample STONEBRIDGE-FM/SAMPLE-GR18 for Friday 18 September 2026 at 12:00 CEST.`
  - `input/06-safety-minutes.txt`: `Neither Facilities nor Vistula Build accepted ownership; the owner field remains blank pending the next coordination call.`
  - `input/07-shift-summary.txt`: `12:05 — STONEBRIDGE-FM/SAMPLE-GR18 still had no assigned collection owner and no carrier booking was logged.`

## Required cross-file resolutions

- Merge the work-request, contractor-chat, diary, and shift-summary evidence for `WR-418` into SB-03. This produces one reassigned, rescheduled, then completed record.
- Merge the supplier email and shift summary for `DELIVERY-VK27`; keep its preparation as separate SB-06 because it is an action with an earlier business-day deadline.
- Apply the 10 September cancellation to the 16 September occurrence of SB-01 and to linked SB-02. Keep the recurring series, its completed 9 September occurrence, and its scheduled 23 September occurrence.
- Keep `WR-418` in `ZONE-E17A` and `WR-481` in `ZONE-E17B` as two records despite the similar request numbers and zone labels.

## Exact positive assertions

1. The final register contains exactly seven records SB-01 through SB-07.
2. SB-01 is one recurring series with three dated occurrences, not three unrelated series.
3. Only SB-01's 16 September occurrence is cancelled; its 23 September occurrence remains scheduled.
4. SB-02 is cancelled with SB-01's 16 September occurrence and was never issued as a visitor card.
5. SB-03 has final owner Lena Nowak, normalized deadline `2026-09-18T16:00:00+02:00`, and final state completed.
6. SB-03 merges `WR-418` evidence from at least the work request, contractor chat, and shift summary.
7. SB-04 remains separate from SB-03 and is completed by Karol Bednar in `ZONE-E17B`.
8. SB-05 is the 14 September 10:30 delivery event and closes at 10:42 with owner unknown.
9. SB-06 is a separate preparation action due Friday 11 September at 16:00, not the delivery event date.
10. `M. Zielinska` in the supplier email and shift summary resolves to Marta Zielinska for SB-06.
11. SB-07 keeps owner unknown and is open/overdue at the reference clock.
12. The final next occurrence for SB-01 is `2026-09-23T09:00:00+02:00`.

## Exact negative assertions

1. **N01 status/metrics:** `The monthly target printed on the dashboard is 92 percent closed within the planned week.` does not create a deadline, target task, or owner record.
2. **N01 status/metrics:** `Generator fuel showed 71 percent; the weekly test is recorded in the utilities register.` does not create a refuelling or generator-test record.
3. **N02 footer/routing:** `Routing: Facilities Desk -> discipline lead -> site diary archive` does not assign either work request to the Facilities Desk or discipline lead.
4. **N02 signature/routing:** the supplier signature and `Delivery issues route to dispatch@bluequarry-supply.example and the Facilities Desk.` do not make Irena Pawlik or the mailbox the owner of SB-05 or SB-06.
5. **N03 quoted history:** `Cytuję wczorajszy wpis: "east joint about 1.8 m". Zostawcie zapas na narożnik.` is context for SB-03 and does not create another joint-repair record.
6. **N03 quoted history:** the quoted email `Monday morning works for the bay team. I can clear bay 2 on the prior working day.` supports SB-06 but does not create a second bay-clearing task.
7. **N04 numbers/versions/dates:** lot `STONEBRIDGE-FM/LOT-VK27`, packing-list version `2.3`, value `PLN 28,640.00`, and use-by date `2029` do not become records or deadlines.
8. **N04 similar identifiers:** request `STONEBRIDGE-FM/WR-481` and zone `ZONE-E17B` must not merge with `WR-418` or `ZONE-E17A`.
9. **N06 procedure/checklist:** `Confirm the sign-in point and the active work zone.` and the other routine checklist lines do not create per-line actions.
10. **N07 agenda/calendar:** `Monday 7 September, 11:30-12:00 — canteen stock count, service kitchen.`, `Tuesday 8 September, 14:00-15:00 — archive shelving walk-through, level B1.`, `Thursday 17 September, 10:00-10:20 — washroom consumables count, stores.`, and `Next month's evacuation drill remains on the annual programme for October.` do not become final register records.

## Coverage and allowed absence

- Mechanisms covered: `M01 M02 M03 M04 M05 M07 M08 M09 M12 M13`.
- Interaction: `M03+M07+M12` resolves a series-level identity across calendar, chat, diary, and handover, cancels one occurrence and its access permit, and preserves the rest of the series and `ZONE-E17B`.
- Noise classes covered: `N01 N02 N03 N04 N06 N07`.
- Meaningful absence is mandatory for SB-05's unloading owner and SB-07's action owner. The evidence permits `unknown/unassigned`; it does not permit an inferred person or team.
- No ambiguity remains in the record identity, date normalization, lifecycle state, or similar-pair separation. The missing owners above are known absences, not ambiguity to resolve.
- All people, organizations, addresses, and identifiers in this scenario are synthetic. The `.example` domains cannot resolve on the public internet.
