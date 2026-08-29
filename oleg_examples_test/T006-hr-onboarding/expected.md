# T006 — LANTERN-HR HR onboarding

## Reference frame

- Reference clock: `2028-09-10T16:00:00Z`.
- Input locales: `en-GB` and `fr-FR`.
- Business zones: `Europe/London` and `Europe/Paris`.
- On the dates in this scenario, London uses BST (`UTC+01:00`) and Paris uses CEST (`UTC+02:00`).
- All people, organizations, identifiers, domains, and events in this scenario are synthetic.

## Source chronology

1. `input/01-hr-email.eml`, 4 September: HR creates the first orientation holds, the HRIS task, and the emergency-contact task.
2. `input/02-manager-chat.txt`, 5 September: Camille states a conditional welcome-pack commitment for Claire and names `A. Durand` as its owner if Claire confirms 18 September.
3. `input/05-access-request.txt`, 5 September: the London access request for Louis is opened with Marc and a 14 September deadline.
4. `input/06-candidate-email.eml`, 6 September: Claire identifies `LANTERN-HR/PEOPLE/CM-42` and confirms 18 September in French.
5. `input/03-orientation-calendar.txt`, 7 September export: Claire's old event is cancelled, her replacement event is confirmed, and Louis's separate London event remains confirmed.
6. `input/02-manager-chat.txt`, 8 September: Louis's access request is reassigned to Priya and rescheduled to 15 September.
7. `input/04-onboarding-checklist.md`, 8 September: Claire's HRIS profile is complete; the emergency-contact task stays open with no owner.
8. `input/07-handoff-minutes.md`, 10 September: the handoff resolves the alias, records two completions, and confirms the remaining open states.

## Final register: 6 records

### R1 — Claire Marot Paris orientation

- Identity: event `LANTERN-HR/ORIENT/CM-42-B` for `LANTERN-HR/PEOPLE/CM-42`.
- Type: orientation event, separate from all preparation actions.
- Owner/host: Camille Laurent.
- Original date text: `12 September 2028 from 09:30 to 12:00 CEST`.
- Original normalized interval: `2028-09-12T07:30:00Z` to `2028-09-12T10:00:00Z` (`Europe/Paris`).
- Final date text: `le lundi 18 septembre 2028 à 9 h 30`; calendar end is 12:00 CEST.
- Final normalized interval: `2028-09-18T07:30:00Z` to `2028-09-18T10:00:00Z` (`Europe/Paris`).
- Final state: confirmed after reschedule; the 12 September event `LANTERN-HR/ORIENT/CM-42-A` is cancelled.
- Sources and exact quotes:
  - `input/01-hr-email.eml`: `For LANTERN-HR/PEOPLE/CM-42, please hold Claire Marot's Paris orientation on 12 September 2028 from 09:30 to 12:00 CEST.`
  - `input/01-hr-email.eml`: `Camille Laurent will host Claire's Paris orientation in LANTERN-HR/PARIS/ROOM-LILAC.`
  - `input/06-candidate-email.eml`: `Je confirme ma présence à l'orientation de Paris le lundi 18 septembre 2028 à 9 h 30.`
  - `input/03-orientation-calendar.txt`: `UID:LANTERN-HR/ORIENT/CM-42-B`
  - `input/03-orientation-calendar.txt`: `DTSTART;TZID=Europe/Paris:20280918T093000`
  - `input/03-orientation-calendar.txt`: `STATUS:CONFIRMED`

### R2 — Claire Marot bilingual welcome-pack preparation

- Identity: one preparation action for `LANTERN-HR/PEOPLE/CM-42`; it is not an event and is not for Louis Marot.
- Owner: Amélie Durand; `A. Durand` is her cross-file alias.
- Original date text: `Friday 15 September at 16:00 Paris time`.
- Normalized deadline: `2028-09-15T14:00:00Z` (`Europe/Paris`).
- Final state: open. It becomes an active commitment only after Claire's 6 September confirmation satisfies the stated condition.
- Sources and exact quotes:
  - `input/02-manager-chat.txt`: `[2028-09-05 08:57 CEST] Camille Laurent: If Claire confirms Monday 18 September, A. Durand will assemble the bilingual welcome pack and leave it with Paris reception by Friday 15 September at 16:00 Paris time.`
  - `input/06-candidate-email.eml`: `Mon dossier est LANTERN-HR/PEOPLE/CM-42 et mon lieu d'arrivée est le bureau de Paris.`
  - `input/07-handoff-minutes.md`: `A. Durand on the manager chat is Amélie Durand in LANTERN-HR/PARIS.`
  - `input/07-handoff-minutes.md`: `The condition is now met; Amélie Durand's bilingual welcome-pack preparation for Claire is open and due 15 September at 16:00 CEST.`

### R3 — Claire Marot HRIS starter profile

- Identity: action for `LANTERN-HR/PEOPLE/CM-42`.
- Owner: Hugo Perrin.
- Original date text: `by 8 September at 17:00 Paris time`.
- Normalized deadline: `2028-09-08T15:00:00Z` (`Europe/Paris`).
- Completion text and time: `8 September 2028 at 16:42 CEST`, normalized as `2028-09-08T14:42:00Z`.
- Final state: completed before its deadline.
- Sources and exact quotes:
  - `input/01-hr-email.eml`: `Hugo Perrin will create Claire Marot's HRIS starter profile by 8 September at 17:00 Paris time.`
  - `input/04-onboarding-checklist.md`: `- HRIS starter profile: completed by Hugo Perrin on 8 September 2028 at 16:42 CEST.`
  - `input/07-handoff-minutes.md`: `Hugo Perrin completed Claire's HRIS starter profile on 8 September at 16:42 CEST.`

### R4 — Louis Marot London orientation

- Identity: event `LANTERN-HR/ORIENT/LM-88` for `LANTERN-HR/PEOPLE/LM-88`.
- Type: orientation event, distinct from Claire's Paris event despite the shared surname.
- Owner/host: Eleanor Shaw.
- Original/final date text: `20 September 2028 from 10:00 to 12:00 BST`.
- Normalized interval: `2028-09-20T09:00:00Z` to `2028-09-20T11:00:00Z` (`Europe/London`).
- Final state: confirmed; no reschedule.
- Sources and exact quotes:
  - `input/01-hr-email.eml`: `For LANTERN-HR/PEOPLE/LM-88, Louis Marot's London orientation remains on 20 September 2028 from 10:00 to 12:00 BST.`
  - `input/01-hr-email.eml`: `Eleanor Shaw will host Louis's London orientation in LANTERN-HR/LONDON/ROOM-ASH.`
  - `input/03-orientation-calendar.txt`: `UID:LANTERN-HR/ORIENT/LM-88`
  - `input/03-orientation-calendar.txt`: `DTSTART;TZID=Europe/London:20280920T100000`
  - `input/07-handoff-minutes.md`: `Louis Marot remains booked for the London orientation on 20 September at 10:00 BST.`

### R5 — Louis Marot standard access bundle

- Identity: action `LANTERN-HR/ACCESS/LM-88` for `LANTERN-HR/PEOPLE/LM-88`.
- Original owner: Marc Vidal.
- Final owner: Priya Nair.
- Original date text: `14 September 2028 at 16:00 London time`.
- Original normalized deadline: `2028-09-14T15:00:00Z` (`Europe/London`).
- Final date text: `15 September at noon, London time`.
- Final normalized deadline: `2028-09-15T11:00:00Z` (`Europe/London`).
- Completion text and time: `10 September at 10:18 BST`, normalized as `2028-09-10T09:18:00Z`.
- Final state: completed after reassignment and reschedule.
- Sources and exact quotes:
  - `input/05-access-request.txt`: `Create the standard London analytics access bundle for Louis Marot.`
  - `input/05-access-request.txt`: `Marc Vidal owns LANTERN-HR/ACCESS/LM-88 with an original deadline of 14 September 2028 at 16:00 London time.`
  - `input/02-manager-chat.txt`: `[2028-09-08 10:08 BST] Eleanor Shaw: For LANTERN-HR/ACCESS/LM-88, Priya Nair takes over from Marc Vidal; move the deadline from 14 September at 16:00 to 15 September at noon, London time.`
  - `input/07-handoff-minutes.md`: `Priya Nair completed LANTERN-HR/ACCESS/LM-88 on 10 September at 10:18 BST after the owner and deadline change.`

### R6 — Claire Marot emergency-contact upload

- Identity: action for `LANTERN-HR/ONB/CM-42` and `LANTERN-HR/PEOPLE/CM-42`.
- Owner: absent/unknown. Keep the owner field empty; do not assign Camille, Hugo, Amélie, or Claire.
- Original/final date text: `15 September at noon Paris time`.
- Normalized deadline: `2028-09-15T10:00:00Z` (`Europe/Paris`).
- Final state: open.
- Sources and exact quotes:
  - `input/01-hr-email.eml`: `Claire's emergency-contact upload remains due on 15 September at noon Paris time.`
  - `input/01-hr-email.eml`: `The owner field for Claire's emergency-contact upload is still blank on LANTERN-HR/ONB/CM-42.`
  - `input/04-onboarding-checklist.md`: `- Emergency-contact upload: open; due 15 September 2028 at 12:00 CEST; owner field blank.`
  - `input/07-handoff-minutes.md`: `Claire's emergency-contact upload remains open for 15 September at 12:00 CEST, and its owner field remains blank.`

## Lifecycle changes

1. R1 moves from the 12 September Paris event to the confirmed 18 September event; the old event is cancelled.
2. R2 changes from a conditional statement to an open action only when Claire confirms the named date.
3. R3 changes from open to completed on 8 September.
4. R5 changes owner from Marc Vidal to Priya Nair.
5. R5 moves from 14 September at 16:00 BST to 15 September at 12:00 BST.
6. R5 changes from open to completed on 10 September.

## Required merge and required separation

- Cross-file merge: R2 requires the conditional statement in `input/02-manager-chat.txt`, Claire's French confirmation and personnel reference in `input/06-candidate-email.eml`, and the alias resolution in `input/07-handoff-minutes.md`. No one file proves the final action, owner, person, and active state.
- Similar pair stays separate: R1 is Claire Marot, `LANTERN-HR/PEOPLE/CM-42`, Paris, 18 September, Camille Laurent. R4 is Louis Marot, `LANTERN-HR/PEOPLE/LM-88`, London, 20 September, Eleanor Shaw. Shared surname and onboarding vocabulary do not merge them.
- Event/action boundary: R1's orientation time is not R2's preparation deadline. The welcome pack remains its own action due before the event.

## Exact positive assertions

1. Extract exactly six final records, R1-R6.
2. Normalize Claire's final orientation start to `2028-09-18T07:30:00Z`.
3. Keep Claire's cancelled 12 September slot as R1 history, not a seventh final record.
4. Activate R2 only after the 6 September candidate email confirms 18 September.
5. Resolve `A. Durand` to Amélie Durand and assign only R2 to her.
6. Keep R2's deadline at `2028-09-15T14:00:00Z`, distinct from R1's event time.
7. Mark R3 completed at `2028-09-08T14:42:00Z`.
8. Keep R4 separate from R1 and normalize its start to `2028-09-20T09:00:00Z`.
9. Reassign R5 from Marc Vidal to Priya Nair.
10. Reschedule R5 from `2028-09-14T15:00:00Z` to `2028-09-15T11:00:00Z`.
11. Mark R5 completed at `2028-09-10T09:18:00Z`.
12. Keep R6 open with an unknown owner and deadline `2028-09-15T10:00:00Z`.

## Specific negative checks

1. `N01`, `input/01-hr-email.eml`: the line `The September intake board now shows six Paris starters and five London starters.` must not create a task to change the board or create eleven starter records.
2. `N01`, `input/02-manager-chat.txt`: `[2028-09-05 09:16 CEST] Camille Laurent: The survey completion rate for the August intake was 72 percent.` must not create a survey deadline or assign Camille a survey task.
3. `N02`, `input/01-hr-email.eml`: `Internal routing: LANTERN-HR/MAIL/PEOPLE-OPS` must not create a routing action or owner.
4. `N02`, `input/01-hr-email.eml`: `Replies are retained under the LANTERN-HR/RECORDS schedule.` must not create a retention task with Camille as owner.
5. `N03`, `input/01-hr-email.eml`: the quoted line `> Reserve LANTERN-HR/PARIS/ROOM-ROSE for the June cohort on 7 June at 14:00.` must not create a current room-reservation record.
6. `N03`, `input/06-candidate-email.eml`: the quoted line `> Nous avons réservé provisoirement le 12 septembre à 9 h 30 pour votre accueil à Paris.` must not reinstate Claire's superseded 12 September event.
7. `N05`, `input/02-manager-chat.txt`: `[2028-09-05 09:05 BST] Priya Nair: Could the welcome tables use the same signs in both offices next month?` must not create a signage task or assign it to Priya.
8. `N05`, `input/06-candidate-email.eml`: `Une courte visite du quartier serait agréable si le groupe en a envie.` must not create a neighbourhood-walk event or assign it to Claire.
9. `N06`, `input/04-onboarding-checklist.md`: `- Send the standard arrival note after the start date is settled.` is a generic template row and must not create a seventh action for Claire or Louis.
10. `N06`, `input/04-onboarding-checklist.md`: `- Close temporary visitor badges after the permanent badge activates.` must not create a badge-closing action for either starter without an instance-specific statement.
11. `N07`, `input/03-orientation-calendar.txt`: `SUMMARY:Possible October content changes` must not create an October change task or alter either orientation.
12. `N07`, `input/03-orientation-calendar.txt`: `DESCRIPTION:The café opens at 08:00 during orientation week and closes its hot counter at 14:30.` must not create café-opening or café-closing actions for Camille, Claire, or Louis.

## Mechanism and noise coverage

- Mechanisms: `M01` records R1-R6; `M02` keeps R1/R4 events separate from R2 preparation; `M03` merges R1, R2, R3, and R5 across sources; `M04` separates Claire and Louis; `M05` reschedules R1 and R5; `M06` completes R3 and R5; `M08` resolves Amélie's alias and reassigns R5; `M10` activates R2 only when its condition becomes true; `M13` preserves R6's missing owner.
- Required interaction `M03+M08+M10`: R2 exists only after the candidate email is merged with the manager chat and the handoff resolves `A. Durand`; the result belongs to Claire, not Louis.
- Noise: `N01`, `N02`, `N03`, `N05`, `N06`, and `N07` are each covered by the numbered negative checks above.

## Context accounting

The inputs contain 364 nonblank lines. The author classification marks 75 lines as positive evidence and 289 as natural context, so natural context is `79.40%`. The evidence set includes every nonblank line that names Claire, Louis, `CM-42`, `LM-88`, `A. Durand`, a record-specific action phrase, or a relevant lifecycle phrase, plus every nonblank line in the three candidate-specific calendar event blocks. This deliberately counts whole relevant calendar blocks and incidental person mentions as evidence. Lines used only in negative checks remain context.
