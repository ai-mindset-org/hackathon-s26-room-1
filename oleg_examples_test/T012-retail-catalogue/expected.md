# T012 — MOSAIC-CAT retail catalogue

All organizations, identifiers, people, messages, products, and operational data in this scenario are synthetic and public-safe.

## Evaluation context

- Reference clock: 2027-04-21T01:00:00Z.
- Locales: ja-JP for Japanese dates and text; English sources use explicit ISO dates.
- Time zones: JST means Asia/Tokyo at UTC+09:00. A trailing Z means UTC.
- Package rule: use event timestamps inside the sources. File names and file order do not define chronology.
- Calendar rule: the higher SEQUENCE for the same UID is the later event state.
- Calendar timing rule: DTSTART and DTEND define an event's start and end. DESCRIPTION prose does not override those structured fields.
- Allowed ambiguity: none.
- Final registry size: exactly 8 records.

## Source chronology

1. 2027-04-16T23:40:00Z — Haru Nakata initially owns the GL-220 price approval with a 2027-04-20T02:00:00Z deadline.
2. 2027-04-17T01:30:00Z — the first calendar places the catalogue review at 2027-04-21T05:00:00Z, the confirmed feed window at 2027-04-21T07:00:00Z, and the tentative store briefing at 2027-04-23T01:00:00Z.
3. 2027-04-17T04:20:00Z — the KN-410 bilingual rename is assigned to Aiko Mori with a Japanese deadline.
4. 2027-04-18T00:20:00Z — the later price email assigns GL-220 to Naomi Seki and moves its deadline.
5. 2027-04-18T01:15:00Z — the later rename email moves the KN-410 deadline and keeps Aiko as owner.
6. 2027-04-18T02:05:00Z — image QA finds that CT-305 uses the back view and records no owner or deadline.
7. 2027-04-18T04:57:00Z — Ren Ito accepts the KN-401 capacity correction with a Japanese deadline.
8. 2027-04-19T08:12:00Z — the import log confirms that the KN-410 bilingual copy is published and completed.
9. 2027-04-20T01:30:00Z — the later calendar moves the sequence-1 campaign review to 2027-04-22 11:30 JST and the sequence-1 confirmed feed window to 2027-04-22T04:30:00Z; the sequence-0 store briefing remains tentative at 2027-04-23T01:00:00Z.
10. 2027-04-20T23:45:00Z — the campaign report completes the separate image-and-copy checklist.
11. 2027-04-21T01:00:00Z — reference clock; the price approval, capacity correction, campaign review, confirmed feed window, tentative store briefing, and CT-305 correction remain open or scheduled.

## Required final registry

### R1 — Publish renamed bilingual copy for MOSAIC-CAT/SKU-KN-410

- Kind: action.
- Identity: one action for stable SKU MOSAIC-CAT/SKU-KN-410 and barcode MOSAIC-CAT/JAN-4580000410410.
- Final names: Japanese 青磁釉マグ 410; English Celadon Glaze Mug 410.
- Owner: Aiko Mori, also written 森愛子.
- Final state: completed at 2027-04-19T08:12:00Z.
- Initial deadline text: 2027年4月18日16:00 JST.
- Initial deadline normalized: 2027-04-18T07:00:00Z.
- Final deadline text: 2027-04-19T08:30:00Z.
- Final deadline normalized: 2027-04-19T08:30:00Z.
- Sources: input/01-sku-card-kn410-ja.md, input/02-sku-card-kn410-en.md, input/06-merch-rename-thread.eml, input/10-chat-localization-20270418.txt, input/17-import-log-20270419.log, input/18-localization-notes-ja.md, input/19-localization-handoff-en.md.
- Source: input/06-merch-rename-thread.eml
- Exact quote: "MOSAIC-CAT/SKU-KN-410の英語名を「Celadon Glaze Mug 410」、日本語名を「青磁釉マグ 410」に変更します。"
- Source: input/10-chat-localization-20270418.txt
- Exact quote: "MOSAIC-CAT/SKU-KN-410 is the same item as Japanese 青磁釉マグ 410 and English Celadon Glaze Mug 410."
- Source: input/06-merch-rename-thread.eml
- Exact quote: "MOSAIC-CAT/SKU-KN-410の新しい締切は2027-04-19T08:30:00Zです。"
- Source: input/17-import-log-20270419.log
- Exact quote: "2027-04-19T08:12:00Z RESULT MOSAIC-CAT/SKU-KN-410 bilingual_copy=published state=completed"

### R2 — Correct Japanese capacity for MOSAIC-CAT/SKU-KN-401

- Kind: action.
- Identity: stable SKU MOSAIC-CAT/SKU-KN-401 and barcode MOSAIC-CAT/JAN-4580000410401.
- Action: change the Japanese capacity display from 410 mL to 401 mL and resubmit it.
- Owner: Ren Ito, also written 伊藤蓮.
- Final state: open.
- Deadline text: 2027年4月22日15:00 JST.
- Deadline normalized: 2027-04-22T06:00:00Z.
- Sources: input/03-sku-card-kn401-ja.md, input/11-chat-qa-20270418.txt, input/18-localization-notes-ja.md, input/21-quality-copy-report.txt.
- Source: input/11-chat-qa-20270418.txt
- Exact quote: "伊藤蓮がMOSAIC-CAT/SKU-KN-401の容量表記を「401 mL」に修正し、2027年4月22日15:00 JSTまでに再提出します。"

### R3 — Approve campaign price for MOSAIC-CAT/SKU-GL-220

- Kind: action.
- Action: approve JPY 3,240 as the campaign price.
- Owner: Naomi Seki. Haru Nakata is the superseded owner.
- Final state: open.
- Initial deadline text: 2027-04-20T02:00:00Z.
- Initial deadline normalized: 2027-04-20T02:00:00Z.
- Final deadline text: 2027年4月21日14:00 JST.
- Final deadline normalized: 2027-04-21T05:00:00Z.
- Sources: input/04-sku-card-gl220.md, input/07-merch-price-thread.eml, input/12-price-list-draft.txt, input/13-price-list-approved.txt.
- Source: input/07-merch-price-thread.eml
- Exact quote: "Haru Nakata owns approval of the MOSAIC-CAT/SKU-GL-220 campaign price by 2027-04-20T02:00:00Z."
- Source: input/07-merch-price-thread.eml
- Exact quote: "Naomi Seki replaces Haru Nakata as owner of MOSAIC-CAT/SKU-GL-220 campaign price approval."
- Source: input/07-merch-price-thread.eml
- Exact quote: "The revised deadline is 2027年4月21日14:00 JST."

### R4 — Attend the MOSAIC-CAT/CAM-SPR-27 catalogue review

- Kind: event.
- Identity: UID MOSAIC-CAT/EV-CAM-SPR-27-REVIEW.
- Owner/organizer: Yui Kondo.
- Final state: scheduled.
- Initial event text: DTSTART:20270421T050000Z.
- Initial event normalized: 2027-04-21T05:00:00Z.
- Final event text: DTSTART;TZID=Asia/Tokyo:20270422T113000.
- Final event normalized: 2027-04-22T02:30:00Z.
- Sources: input/08-merch-campaign-handoff.eml, input/14-campaign-calendar-initial.ics, input/15-campaign-calendar-revised.ics, input/22-quality-campaign-report.txt.
- Source: input/14-campaign-calendar-initial.ics
- Exact quote: "DTSTART:20270421T050000Z"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "DTSTART;TZID=Asia/Tokyo:20270422T113000"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "ORGANIZER;CN=Yui Kondo:mailto:yui.kondo@mosaic-cat.example"

### R5 — Finish the MOSAIC-CAT/CHK-SPR-27-IC image-and-copy checklist

- Kind: action that prepares R4. It is not the review event itself.
- Owner: Kota Endo.
- Final state: completed at 2027-04-20T23:45:00Z.
- Deadline text: 2027-04-21 09:00 JST.
- Deadline normalized: 2027-04-21T00:00:00Z.
- Sources: input/08-merch-campaign-handoff.eml, input/22-quality-campaign-report.txt.
- Source: input/08-merch-campaign-handoff.eml
- Exact quote: "Kota Endo will finish MOSAIC-CAT/CHK-SPR-27-IC by 2027-04-21 09:00 JST."
- Source: input/22-quality-campaign-report.txt
- Exact quote: "MOSAIC-CAT/CHK-SPR-27-IC was completed at 2027-04-20T23:45:00Z by Kota Endo."

### R6 — Replace the main image for MOSAIC-CAT/SKU-CT-305

- Kind: action.
- Action: replace the selected back view with the available front view.
- Owner: unknown. The source explicitly has no registered owner.
- Final state: open.
- Deadline text: absent.
- Deadline normalized: unknown.
- Sources: input/05-sku-card-ct305.md and input/20-quality-image-report.txt.
- Source: input/20-quality-image-report.txt
- Exact quote: "MOSAIC-CAT/SKU-CT-305のメイン画像は背面写真です。正面画像への差し替えが必要です。"
- Source: input/20-quality-image-report.txt
- Exact quote: "担当: 未登録"
- Source: input/20-quality-image-report.txt
- Exact quote: "修正期限: 未登録"

### R7 — MOSAIC-CAT/CAM-SPR-27 scheduled feed window

- Kind: event.
- Identity: UID MOSAIC-CAT/EV-FEED-WINDOW-27.
- Owner/organizer: unknown. Neither calendar source states one.
- Final state: confirmed; calendar STATUS is CONFIRMED.
- Initial event text: DTSTART:20270421T070000Z through DTEND:20270421T073000Z.
- Initial event normalized: 2027-04-21T07:00:00Z through 2027-04-21T07:30:00Z.
- Final event text: DTSTART:20270422T043000Z through DTEND:20270422T050000Z.
- Final event normalized: 2027-04-22T04:30:00Z through 2027-04-22T05:00:00Z.
- Sources: input/14-campaign-calendar-initial.ics and input/15-campaign-calendar-revised.ics.
- Source: input/14-campaign-calendar-initial.ics
- Exact quote: "UID:MOSAIC-CAT/EV-FEED-WINDOW-27"
- Source: input/14-campaign-calendar-initial.ics
- Exact quote: "DTSTART:20270421T070000Z"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "DTSTART:20270422T043000Z"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "DTEND:20270422T050000Z"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "STATUS:CONFIRMED"

### R8 — MOSAIC-CAT/CAM-SPR-27 store preview briefing

- Kind: event.
- Identity: UID MOSAIC-CAT/EV-STORE-BRIEF-27.
- Owner/organizer: unknown. Neither calendar source states one.
- Final state: tentative; calendar STATUS is TENTATIVE.
- Event text: DTSTART:20270423T010000Z through DTEND:20270423T013000Z.
- Event normalized: 2027-04-23T01:00:00Z through 2027-04-23T01:30:00Z.
- Sequence: 0 in both calendar sources; the later calendar repeats the same tentative state and time.
- Sources: input/14-campaign-calendar-initial.ics and input/15-campaign-calendar-revised.ics.
- Source: input/14-campaign-calendar-initial.ics
- Exact quote: "UID:MOSAIC-CAT/EV-STORE-BRIEF-27"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "DTSTART:20270423T010000Z"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "DTEND:20270423T013000Z"
- Source: input/15-campaign-calendar-revised.ics
- Exact quote: "STATUS:TENTATIVE"

## Lifecycle changes

1. R1: rename from 青磁マグ 410 / Celadon Mug 410 to 青磁釉マグ 410 / Celadon Glaze Mug 410.
2. R1: deadline moves from 2027年4月18日16:00 JST to 2027-04-19T08:30:00Z.
3. R1: open work becomes completed through the later import result.
4. R3: owner changes from Haru Nakata to Naomi Seki.
5. R3: deadline moves from 2027-04-20T02:00:00Z to 2027年4月21日14:00 JST.
6. R4: event moves from 2027-04-21T05:00:00Z to 2027年4月22日11:30 JST.
7. R5: open preparation becomes completed.
8. R7: confirmed feed window moves from 2027-04-21T07:00:00Z to 2027-04-22T04:30:00Z.

## Required merge and required separation

- Merge: all KN-410 evidence listed under R1 is one record. Stable SKU MOSAIC-CAT/SKU-KN-410 and barcode MOSAIC-CAT/JAN-4580000410410 connect the Japanese old name, English old name, two new names, Aiko/森愛子, later deadline, and import completion.
- Keep separate: R1 and R2 remain different records. MOSAIC-CAT/SKU-KN-410 and MOSAIC-CAT/SKU-KN-401 have visually similar images, adjacent bilingual names, and the same colour profile, but their SKUs, barcodes, capacities, dimensions, actions, owners, and deadlines differ.
- Keep separate: R4 is the meeting event. R5 is its preparation action with an earlier deadline and a different owner.
- Keep separate: R4, R7, and R8 are three events with distinct UIDs, purposes, times, locations, and statuses. Their shared MOSAIC-CAT/CAM-SPR-27 campaign identity does not merge them.

## Exact positive assertions

1. The final registry has exactly eight records.
2. R1 uses stable SKU MOSAIC-CAT/SKU-KN-410, not a display-name-only identity.
3. R1 merges Japanese and English rename evidence into one record.
4. R1 owner is Aiko Mori / 森愛子.
5. R1 final deadline is 2027-04-19T08:30:00Z.
6. R1 final state is completed.
7. R2 remains separate from R1.
8. R2 owner is Ren Ito / 伊藤蓮.
9. R2 deadline is 2027-04-22T06:00:00Z.
10. R3 final owner is Naomi Seki, not Haru Nakata.
11. R3 final deadline is 2027-04-21T05:00:00Z.
12. R4 final event time is 2027-04-22T02:30:00Z.
13. R4 organizer is Yui Kondo.
14. R5 is a separate preparation action and is completed.
15. R6 is open with unknown owner and unknown deadline.
16. R7 is a separate confirmed event from 2027-04-22T04:30:00Z through 2027-04-22T05:00:00Z.
17. R8 is a separate tentative event from 2027-04-23T01:00:00Z through 2027-04-23T01:30:00Z.
18. Later timestamps and calendar SEQUENCE override earlier states.

## Exact negative checks

1. N01, input/03-sku-card-kn401-ja.md: the fragment "West shelf count remained 72 units after the noon recount." does not create a stock-count or replenishment action.
2. N02, input/06-merch-rename-thread.eml: the footer "Standard routing: catalogue -> localization -> QA -> publish." does not create four workflow actions.
3. N03, input/10-chat-localization-20270418.txt: the quoted line "Quoted from 2026: retire the navy wrap after Golden Week." does not create a current packaging-retirement action.
4. N04, input/12-price-list-draft.txt: "March FX snapshot: 2027-03-31, rate column 149.80." does not create a 2027-03-31 deadline or an approval at 149.80.
5. N04, input/09-chat-merch-20270417.txt: "staging themeは昨夜のbuild 2027.107です。" does not create a date, deadline, campaign, or SKU numbered 2027.107.
6. N06, input/20-quality-image-report.txt: "If an image checksum changes, the reviewer compares both thumbnails." does not create a current thumbnail-comparison action.
7. N08, input/20-quality-image-report.txt: the damaged fragment "Broken preview row: MOSAIC-CAT/SKU-KN-4I0 | ?? | 4/19" does not create a SKU, deadline, or alias, and it does not merge with KN-410.
8. N09, input/16-import-log-20270418.log: "2027-04-18T00:58:10Z WARN retry_at=2027-04-18T01:20:00Z queue=MOSAIC-CAT/Q-CAT-4" does not create an operator task with a 2027-04-18T01:20:00Z deadline.
9. N09, input/21-quality-copy-report.txt: "The next scheduled preview refresh is 2027-04-20T03:00:00Z." does not create a person-owned action or campaign deadline.
10. N04, input/01-sku-card-kn410-ja.md: "入荷予定日: 2027年5月8日" does not become the deadline for R1 or a separate publishing action.
11. N01, input/22-quality-campaign-report.txt: "The review deck remains revision 6." does not create a deck revision action.
12. N03, input/21-quality-copy-report.txt: "Quoted old subject: MOSAIC-CAT/SKU-KN-410 spring name alignment." does not create a second rename record.

## Mechanism coverage

- M01: eight actions or events and their fields.
- M02: R4 event versus R5 preparation action, plus R4, R7, and R8 as separate campaign events.
- M03: R1 merges evidence across cards, email, chat, localization, and import.
- M04: KN-410 and KN-401 remain separate.
- M05: R1 and R3 deadlines, plus the R4 and R7 event times, change.
- M06: R1 and R5 complete.
- M08: Aiko/森愛子 alias and Haru-to-Naomi reassignment.
- M09: Japanese dates, ISO UTC dates, JST, and UTC normalize together.
- M11: later email timestamps, later import result, and calendar SEQUENCE win.
- M13: R6 owner and deadline remain unknown.
- M15: Japanese and English names connect through stable identifiers.
