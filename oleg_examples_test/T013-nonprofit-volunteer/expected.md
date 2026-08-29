# T013 — Некоммерческая организация и волонтёры

Опорное время: `2027-09-19T08:30:00-04:00`.

- Локали источников: `en-CA` и `fr-CA`.
- Пояс: `America/Toronto` (`UTC-04:00` на всех датах сценария).
- Место: Montréal.
- Все организации, места, идентификаторы, домены и люди синтетические.

## Хронология

1. 13 сентября в реестре смен `COMMON-GOOD/VOL-214` условно запланирована на субботнее утро. Первичный руководитель — Amélie Nadeau. Подтверждение четырёх волонтёров тоже условно и зависит от открытия смены.
2. 13 сентября Roxane Gervais передаёт руководство сменой Malik Benali. Malik принимает только условное назначение.
3. 14 сентября партнёр переносит срок `COMMON-GOOD/SIGN-441` со старого, процитированного срока 15 сентября 17:00 на 16 сентября 14:00. Leïla Roy принимает новый срок.
4. 16 сентября в 16:00 погодный бюллетень сохраняет оранжевый уровень. Это запускает проверку, но не само решение по смене.
5. 16 сентября в 16:10 координатор Roxane отменяет `COMMON-GOOD/VOL-214` и связанное подтверждение волонтёров. Протокол в 16:20 подтверждает этот итог.
6. Отмена утренней смены не отменяет `COMMON-GOOD/EVT-441` в том же месте в субботу днём и не отменяет `COMMON-GOOD/EVT-442` там же в воскресенье.
7. 18 сентября отчёт фиксирует, что `COMMON-GOOD/EVT-441` состоялось. Он сохраняет `COMMON-GOOD/COUNT-441` открытой задачей с известным сроком и неизвестным владельцем.

## Требуемое состояние: 6 записей

### 1. `COMMON-GOOD/EVT-441` — Community Pantry / Garde-manger communautaire

- Тип: событие.
- Владелец: Roxane Gervais, координатор события.
- Конечное состояние: состоялось, не отменено.
- Время в исходном календаре: `Saturday 18 September 2027, 12:00–15:30`.
- Нормализованное время: начало `2027-09-18T12:00:00-04:00`, конец `2027-09-18T15:30:00-04:00`.
- Источники: `input/calendar.txt`, `input/coordinator-chat.txt`, `input/meeting-minutes.txt`, `input/event-report.txt`.
- Точные цитаты:
  - `When: Saturday 18 September 2027, 12:00–15:30`
  - `Event coordinator: Roxane Gervais`
  - `COMMON-GOOD/EVT-441 still runs at COMMON-GOOD/Maison-du-Canal from 12:00 to 15:30 on Saturday. The indoor team uses the east entrance.`
  - `COMMON-GOOD/EVT-441 remains confirmed for Saturday 18 September, 12:00–15:30, at COMMON-GOOD/Maison-du-Canal.`
  - `COMMON-GOOD/EVT-441 took place as scheduled from 12:00 to 15:30, using the indoor east entrance.`

### 2. `COMMON-GOOD/VOL-214` — условная утренняя welcome-смена

- Тип: смена.
- Первичный владелец: Amélie Nadeau.
- Последний назначенный владелец: Malik Benali.
- Конечное состояние: отменена решением координатора.
- Время в источниках: `Saturday 18 September 2027 | 08:30–11:00`.
- Нормализованное время: начало `2027-09-18T08:30:00-04:00`, конец `2027-09-18T11:00:00-04:00`.
- Условие: смена могла открыться только после погодной проверки и явного решения Roxane Gervais. Оранжевый бюллетень сам её не открывает и не отменяет.
- Источники: `input/shift-roster.txt`, `input/calendar.txt`, `input/coordinator-chat.txt`, `input/weather-notice.txt`, `input/meeting-minutes.txt`, `input/event-report.txt`.
- Точные цитаты:
  - `Activation | after the Thursday weather review, only if coordinator Roxane Gervais opens the shift`
  - `Status: Tentative — coordinator weather decision pending`
  - `Malik, take the lead for COMMON-GOOD/VOL-214 from Amélie. It remains conditional on Thursday's weather review.`
  - `Saturday 18 September outlook, 06:00–11:00: orange rain level maintained.`
  - `Final decision: cancel COMMON-GOOD/VOL-214, the conditional welcome shift on Saturday morning. Malik, close the volunteer confirmations tied to that shift.`
  - `Roxane confirmed the decision recorded in chat: COMMON-GOOD/VOL-214 is cancelled, including Malik's dependent volunteer-confirmation follow-up.`
  - `The cancelled COMMON-GOOD/VOL-214 morning shift was not reinstated; the event team began its normal setup at 11:30.`

### 3. Подтвердить четырёх волонтёров для `COMMON-GOOD/VOL-214`

- Тип: производное действие, а не отдельное событие.
- Владелец: Malik Benali.
- Исходное состояние: условно открыто только при открытии родительской смены.
- Конечное состояние: отменено вместе с `COMMON-GOOD/VOL-214`; выполнять подтверждение не нужно.
- Срок в источнике: `Thursday 16 September 2027 at 18:00 if the shift is opened`.
- Нормализованный условный срок: `2027-09-16T18:00:00-04:00`.
- Источники: `input/shift-roster.txt`, `input/coordinator-chat.txt`, `input/meeting-minutes.txt`.
- Точные цитаты:
  - `Linked follow-up | Malik Benali to confirm the four volunteers by Thursday 16 September 2027 at 18:00 if the shift is opened`
  - `COMMON-GOOD/VOL-214 and its pending confirmation follow-up are closed as cancelled.`
  - `Roxane confirmed the decision recorded in chat: COMMON-GOOD/VOL-214 is cancelled, including Malik's dependent volunteer-confirmation follow-up.`

### 4. `COMMON-GOOD/SIGN-441` — отправить двуязычный пакет входной вывески

- Тип: действие подготовки к `COMMON-GOOD/EVT-441`, отдельное от времени события.
- Владелец: Leïla Roy.
- Конечное состояние: завершено 16 сентября в 13:42.
- Старый срок из процитированной истории: `Wednesday 15 September at 17:00`.
- Конечный срок в актуальном письме: `Thursday 16 September at 14:00 Montréal time`.
- Нормализованный конечный срок: `2027-09-16T14:00:00-04:00`.
- Источники: `input/partner-email.txt`, `input/coordinator-chat.txt`, `input/meeting-minutes.txt`, `input/event-report.txt`.
- Точные цитаты:
  - `Please have Leïla send the final bilingual package for COMMON-GOOD/SIGN-441 by Thursday 16 September at 14:00 Montréal time.`
  - `I accept the revised cutoff and will send the bilingual entrance sign package by then.`
  - `COMMON-GOOD/SIGN-441 was delivered to COMMON-GOOD/Partenaire-Rivage at 13:42, ahead of the revised cutoff.`
  - `Leïla reported that COMMON-GOOD/SIGN-441 reached COMMON-GOOD/Partenaire-Rivage at 13:42.`
  - `COMMON-GOOD/SIGN-441 was installed beside the east doors and both language headings were visible from the lobby.`

### 5. `COMMON-GOOD/EVT-442` — Repair Café / Café de réparation

- Тип: событие, отдельное от `COMMON-GOOD/EVT-441` и `COMMON-GOOD/VOL-214`.
- Владелец: Riad Moreau, координатор события.
- Конечное состояние: подтверждено, запланировано.
- Время в источнике: `Sunday 19 September 2027, 10:00–13:00`.
- Нормализованное время: начало `2027-09-19T10:00:00-04:00`, конец `2027-09-19T13:00:00-04:00`.
- Источники: `input/calendar.txt`, `input/coordinator-chat.txt`, `input/meeting-minutes.txt`.
- Точные цитаты:
  - `Title: Repair Café / Café de réparation`
  - `Event coordinator: Riad Moreau`
  - `COMMON-GOOD/EVT-442 also keeps its Sunday slot at the same venue.`
  - `COMMON-GOOD/EVT-442 remains confirmed for Sunday 19 September, 10:00–13:00, at the same venue.`

### 6. `COMMON-GOOD/COUNT-441` — отправить итог посещаемости партнёру

- Тип: действие после `COMMON-GOOD/EVT-441`.
- Владелец: неизвестен. Нельзя назначать Amélie, Malik, Roxane, Riad или Leïla по соседнему контексту.
- Конечное состояние: открыто.
- Срок в источнике: `Monday 20 September at 12:00 Montréal time`.
- Нормализованный срок: `2027-09-20T12:00:00-04:00`.
- Источники: `input/meeting-minutes.txt`, `input/event-report.txt`.
- Точные цитаты:
  - `The owner of COMMON-GOOD/COUNT-441 was not selected; the Monday check-in will assign it.`
  - `COMMON-GOOD/COUNT-441 remains open: send the attendance total to COMMON-GOOD/Partenaire-Rivage by Monday 20 September 2027 at 12:00 Montréal time.`

## Изменения жизненного цикла и связи

- `COMMON-GOOD/VOL-214`: условно запланирована → переназначена с Amélie Nadeau на Malik Benali → отменена Roxane Gervais.
- Подтверждение четырёх волонтёров: условно открыто → отменено из-за отмены родительской смены.
- `COMMON-GOOD/SIGN-441`: срок перенесён с 15 сентября 17:00 на 16 сентября 14:00 → завершено 16 сентября 13:42.
- `COMMON-GOOD/EVT-441`: подтверждено → состоялось; отмена утренней смены не распространяется на событие.
- Правильное межфайловое слияние: все упоминания `COMMON-GOOD/VOL-214` в реестре, календаре, чате, протоколе и отчёте относятся к одной смене. Более позднее решение определяет её конечное состояние.
- Похожая отдельная пара: `COMMON-GOOD/EVT-441` и `COMMON-GOOD/EVT-442` проходят в `COMMON-GOOD/Maison-du-Canal` на соседних датах, но остаются двумя событиями с разными названиями, временем и координаторами.

## Положительные проверки

1. Реестр содержит ровно 6 конечных записей.
2. `COMMON-GOOD/VOL-214` не дублируется по числу источников.
3. Конечный владелец `COMMON-GOOD/VOL-214` — Malik Benali, а не Amélie Nadeau.
4. Конечное состояние `COMMON-GOOD/VOL-214` — отменена.
5. Производное подтверждение волонтёров тоже отменено.
6. `COMMON-GOOD/EVT-441` не отменено и имеет конечное состояние «состоялось».
7. `COMMON-GOOD/EVT-442` остаётся отдельным подтверждённым событием.
8. Конечный срок `COMMON-GOOD/SIGN-441` — 16 сентября 14:00, а не срок из процитированного старого письма.
9. `COMMON-GOOD/SIGN-441` завершено до конечного срока.
10. `COMMON-GOOD/COUNT-441` открыто, имеет срок 20 сентября 12:00 и неизвестного владельца.
11. Время события `COMMON-GOOD/EVT-441` не подменяет срок подготовки `COMMON-GOOD/SIGN-441`.
12. Оранжевый погодный бюллетень рассматривается как условие для решения, а не как автор отмены.

## Не создавать и не связывать

1. `N03`: не оставлять актуальным старый срок `Wednesday 15 September at 17:00` из процитированной цепочки письма и не создавать по нему вторую задачу `COMMON-GOOD/SIGN-441`.
2. `N04`: не создавать запрос версии `R2` из `Our paper supplier calls this matte stock “R2”; it is the same sheet used for the May run.`; `R2` — название материала.
3. `N04`: не создавать событие на 7 сентября из `the west room piano tuning happened on 7 September and is complete.`; это завершённый факт о помещении.
4. `N05`: не создавать задачу на вторую вывеску из вопроса `would a second sign near the indoor queue help?`.
5. `N05`: не создавать октябрьскую смену из вопроса `whether October shifts could begin at 09:00`; расписание октября не составлено.
6. `N07`: не создавать ноябрьский seed-swap event из `a possible seed-swap evening was discussed for November, with no date selected.`.
7. `N10`: не создавать задачу купить oat milk из бытовой реплики Malik; это личная реплика без рабочего назначения и срока.
8. `N10`: не создавать рабочее голосование или закупку из реплики `The tea vote is tied, six for mint and six for breakfast blend.`.
9. `N01`: не превращать показатели `91`, `224`, `63`, `58` и `5` из отчёта события в сроки, владельцев или отдельные обязательства.
10. `N05`: не считать вопрос про QR tally назначением владельца `COMMON-GOOD/COUNT-441`.
11. Не сливать `COMMON-GOOD/EVT-441`, `COMMON-GOOD/VOL-214` и `COMMON-GOOD/EVT-442` только из-за общего места.
12. Не назначать владельца `COMMON-GOOD/COUNT-441` по автору отчёта или участникам протокола.

## Допустимая неоднозначность

- Для отменённого условного подтверждения волонтёров допустимы два представления интерфейса: отдельная отменённая строка или отменённое дочернее действие внутри `COMMON-GOOD/VOL-214`. В обоих случаях оно остаётся отдельным смысловым обязательством в числе шести, имеет владельца Malik Benali и не остаётся открытым.
- Для `COMMON-GOOD/EVT-441` допустимы состояния `состоялось` или `завершено`. Состояния `отменено`, `условно` и `запланировано без учёта отчёта` недопустимы.
