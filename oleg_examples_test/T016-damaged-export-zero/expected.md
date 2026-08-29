# T016 — FRACTURE-ZERO damaged-export zero

## Evaluation frame

- Reference clock: `2026-09-30T12:00:00Z`.
- Final result: exactly **0 records**. There is no current action, event, owner, deadline, or state transition to add to the register.
- All input material is synthetic and public-safe. Names, addresses, objects, IDs, and domains belong only to the fictional `FRACTURE-ZERO/*` namespace.
- Locale and zone are source-local. Do not propagate a locale or zone from one file to another.
- `02-broken-text-table.txt` naturally declares `es-ES`, `dd/MM/yyyy`, and `Europe/Madrid`. These settings apply only to that archived table export.
- `04-duplicated-email-headers.eml` declares the archive site as `America/Chicago`. Its 2025 `-0500`, 2022 `-0500`, and 2019 `-0600` header offsets are consistent with that site. They apply only to the corresponding mail headers.
- `05-partial-log.txt` uses timestamps with `Z`; those log timestamps and its scheduler timestamp are UTC.
- `07-calendar-fragments.ics.txt` declares `Europe/Madrid`; apply that zone only to complete `TZID` values in the calendar fragments.
- The chat, OCR scan, and quotation catalog do not establish a locale or zone. Their mixed English and Spanish text does not supply one. The chat value `14/09` therefore stays an unresolved fragment.

## Chronology and damaged-source reading

Chronology follows the time inside each source, not the filename order:

1. The quotation catalog contains printed examples dated 2018–2021.
2. The broken table identifies its field dictionary as a 2019 archive artifact.
3. The OCR source is a damaged copy of 2021 minutes and older manual text.
4. The visible mail quote is from 2022; the duplicated outer capture is from 2025.
5. The calendar blocks describe 2023–2024 items and were captured in 2025.
6. The truncated chat is from 2025.
7. The partial parser log is from 2026. Its `next_run` value is a service schedule after the reference clock, not a human commitment.

Readable structure can be recovered, but missing content stays missing:

- In `01-truncated-chat.txt`, speaker labels and visible messages are readable. The missing opening block, final timestamp, final speaker, and final message are unknown.
- In `02-broken-text-table.txt`, the export profile, field-dictionary purpose, visible labels, and sample rows are readable. Shifted columns and question-mark semantics are not reconstructed.
- In `03-ocr-scan.txt`, `ENVI` plus `AR UNA COPIA` is a same-page OCR line join for the procedural phrase `ENVIAR UNA COPIA`. The missing preceding page, damaged accent, paragraph edges, and footer remain unknown.
- In `04-duplicated-email-headers.eml`, the repeated outer header is one archived message envelope, not two new messages. The missing MIME boundary and missing second body remain unknown.
- In `05-partial-log.txt`, complete log fields remain system metadata. The final JSON object is incomplete, so its absent owner value and all later fields remain unknown.
- In `07-calendar-fragments.ics.txt`, known properties can be read inside their own blocks. The final block lacks a complete start time, status, duration, and closing marker; none can be supplied from another file.

This is the required `M16 + M17` interaction: repair only local readable structure, then keep unrelated sources separate. Local repair never licenses a cross-file action, owner, date, or event assembly.

## Final register — 0 records

The register is empty. Historical quotations, questions, options, refusals, procedures, table samples, old calendar entries, and system metadata do not establish a current commitment or upcoming event.

No lifecycle change applies. No cross-file merge is valid. No similar pair becomes a record.

## Specific false-positive checks

Each item names the source and an exact input quote.

1. `N05 / M10` — `01-truncated-chat.txt`: `Could Noelia send the recovered index by Friday, or should it stay inside FRACTURE-ZERO/VAULT-2?` is a question with alternatives. It does not create an action, owner, or Friday deadline.
2. `N05 / M10` — `01-truncated-chat.txt`: `¿Y si revisamos FRACTURE-ZERO/ARC-17 el 14/09?` is a hypothetical question. It does not create a review action or normalize `14/09`.
3. `N05 / M10` — `01-truncated-chat.txt`: `I cannot take ownership of the checksum review.` is a refusal. It does not assign Noelia or create the refused review.
4. `N06 / M10` — `01-truncated-chat.txt`: `We should not email the raw scan outside FRACTURE-ZERO/VAULT-2.` is a prohibition about handling. It does not create a send action or recipient.
5. `N08 / M13 / M16` — `02-broken-text-table.txt`: `FRACTURE-ZERO/ARC-17 || REVISAR || 14/09 || Noelia? || ejemplo_de_columna` is a shifted sample row in an archived field dictionary. It does not assign Noelia, create a review, or supply a deadline.
6. `N04 / N08` — `02-broken-text-table.txt`: `FRACTURE-ZERO/LABEL-23 || MAÑANA || palabra_de_prueba || casilla 12` is a vocabulary sample. It does not create a tomorrow action.
7. `N04 / N08` — `02-broken-text-table.txt`: `row 021 | 4.11 | FRACTURE-ZERO/READER | release label | build 906` contains a version and build number. It does not create a release action or date.
8. `N08 / M16` — `03-ocr-scan.txt`: `CONFIRMO? el lector antiguo mostraba esa palabra con una mancha sobre la O.` is damaged historical OCR. It does not establish a present confirmation, speaker, or event.
9. `N06` — `03-ocr-scan.txt`: `Review each recovered row before export.` is copied manual text. It does not create an assigned review action.
10. `N03 / N08 / M16` — `03-ocr-scan.txt`: `old line: Mateo will send ...` and `old line: by Friday ...` are two clipped historical paragraphs. They do not combine into a current promise or deadline.
11. `N05 / M10` — `04-duplicated-email-headers.eml`: `Could someone send the checksum on Friday if the second body appears?` is a conditional question. It does not create an action, owner, or date.
12. `N03` — `04-duplicated-email-headers.eml`: `> I will send FRACTURE-ZERO/BOARD-4 on Friday after the board review.` is a quoted 2022 promise. It does not create a current record.
13. `N03 / N08 / M16` — `04-duplicated-email-headers.eml`: `Date: Mon, 22 Sep 2025 08:14:03 -0500` occurs exactly twice because one outer header was duplicated. It does not create two messages, events, or deadlines.
14. `N09 / M14` — `05-partial-log.txt`: `parser.candidate.action="send index" source_key=FRACTURE-ZERO/CHAT-004 confidence=0.31` is parser telemetry. It does not create a send action.
15. `N09 / M02` — `05-partial-log.txt`: `event=scheduler next_run=2026-10-02T02:00:00Z schedule=FRACTURE-ZERO/NIGHTLY-SCAN` is a service schedule. It does not create a human action or preparation deadline.
16. `N03` — `06-old-quotations.txt`: `FRACTURE-ZERO/QUOTE-02 | 2018 | Español | “Mañana preparo el resumen.”` is a cataloged 2018 quotation. It does not create a current preparation action.
17. `N03 / N06` — `06-old-quotations.txt`: `FRACTURE-ZERO/QUOTE-07 | 2019 | English | “Review each row before export.”` is a quoted procedure-card line. It does not create an action.
18. `N07 / M02` — `07-calendar-fragments.ics.txt`: `DESCRIPTION:Doors at 08:30; review at 09:00. Bring the draft index for the old tab comparison.` belongs to a cancelled 2023 event. It does not create either a current event or a separate preparation action.
19. `N05 / N07 / M10` — `07-calendar-fragments.ics.txt`: `DESCRIPTION:Question panel: Could Lina send the index by Friday? Option panel: maybe after review.` is demonstration text inside a damaged 2024 calendar fragment. It does not create an action, owner, or deadline.

## Non-action text types

At least these seven types remain outside the register:

1. Question — `01-truncated-chat.txt`: `What if we compare only the page counts before choosing a route?`
2. Hypothesis — `01-truncated-chat.txt`: `Suppose FRACTURE-ZERO/ARC-17 and FRACTURE-ZERO/BOX-17 only share the suffix by chance.`
3. Refusal — `01-truncated-chat.txt`: `I cannot take ownership of the checksum review.`
4. Procedure — `03-ocr-scan.txt`: `Keep the original page number beside every recovered row.`
5. Old quotation — `06-old-quotations.txt`: `FRACTURE-ZERO/QUOTE-01 | 2018 | English | “I will send the blue index tomorrow.”`
6. System metadata — `05-partial-log.txt`: `event=cache entries=144 hit_ratio=0.93`
7. Past calendar material — `07-calendar-fragments.ics.txt`: `SUMMARY:FRACTURE-ZERO/READER-4.11 demonstration`

## Required cross-file non-merges

1. Do not combine the chat question `Could Noelia send the recovered index by Friday, or should it stay inside FRACTURE-ZERO/VAULT-2?`, the table sample `FRACTURE-ZERO/ARC-17 || REVISAR || 14/09 || Noelia? || ejemplo_de_columna`, and the log field `parser.candidate.date="14/09" source_key=FRACTURE-ZERO/TABLE-017 locale_hint=absent`. These are different source objects and do not form an action, owner, and deadline.
2. Do not combine OCR token `ENVI`, mail identity `From: Noelia Rios <noelia.rios@fracture-zero.example>`, and calendar property `DTSTART;TZID=Europe/Madrid:20230914T090000`. The OCR token joins only to the next OCR line as procedural text; the sender and old calendar time are unrelated.
3. Do not merge `FRACTURE-ZERO/ARC-17`, `FRACTURE-ZERO/BOX-17`, `FRACTURE-ZERO/CAL-17`, `FRACTURE-ZERO/RUN-17`, or `FRACTURE-ZERO/BOARD-17` because they share suffix `17`. Their prefixes and source roles identify different archive objects.
4. Do not combine the words `Friday`, `SEND`, `OWNER`, `Noelia`, or `14/09` across the chat, table dictionary, OCR manual, quoted mail, quotation catalog, parser log, and calendar demonstration. Repetition is caused by archived vocabulary and examples, not one entity.

## Meaningful absences

- Current action: absent. Visible verbs occur in questions, hypotheses, refusals, prohibitions, procedures, old quotations, field samples, demonstration text, or parser telemetry.
- Current owner: absent. Noelia, Mateo, Lina, and Ari appear as speakers, examples, senders, quoted people, or candidate values. No current acceptance or assignment exists.
- Human deadline: absent. `Friday`, `tomorrow`, `14/09`, `09:00`, version numbers, weights, past dates, and `next_run` do not establish one.
- Upcoming event: absent. The calendar material is from 2023–2024, includes damaged blocks, and does not describe a current event at the reference clock.
- Confirmation: absent. The OCR `CONFIRMO?` line is damaged and historical; no current confirmation source exists.
- Cross-file identity: absent. Similar terms and suffixes do not prove that objects from different files are the same.
- Locale and zone for chat, OCR, and quotation fragments: absent. Do not borrow `es-ES`, `America/Chicago`, UTC, or `Europe/Madrid` from another source.
- Missing fragment content: absent. Do not complete the chat ending, MIME body, OCR edges, log JSON, or final calendar block.

## Mechanism and noise coverage

- `M02`: separates old/cancelled calendar events and system schedules from human preparation actions.
- `M10`: preserves questions, options, conditions, refusals, and prohibitions as their actual modalities.
- `M13`: preserves unknown owner, deadline, confirmation, locale, zone, and cross-file identity.
- `M14`: returns exactly zero records despite dense action-like vocabulary, names, and dates.
- `M16`: recovers only readable local structure from truncation, shifted tables, OCR splits, duplicated headers, partial JSON, and calendar folding.
- `M17`: blocks all proposed cross-file assemblies.
- Noise coverage: `N03`, `N04`, `N05`, `N06`, `N07`, `N08`, and `N09` all appear in the checks above.

## Measured package properties

- Input files: `7`.
- Input bytes: `17,741` bytes (`17.325 KiB`, with `1 KiB = 1,024 bytes`).
- Nonblank input lines: `292`.
- Conservative natural non-evidence context count: `268 / 292` nonblank lines (`91.78%`). The author excluded 24 action-like trap lines from the numerator even though they occur inside natural operational material.
- Final records: `0`.

These measurements cover only this T016 input package. They do not establish corpus-wide behavior, production accuracy, or performance. Semantic extraction itself is not executed in this fixture-building task.

## Allowed ambiguity

Damage can leave multiple literal readings of `14/09`, `CONFIRMO?`, broken table cells, and clipped sentence edges. Every allowed reading still yields zero records. Ambiguity preserves missing fields; it does not authorize a guessed owner, action, date, event, locale, zone, confirmation, or cross-file link.
