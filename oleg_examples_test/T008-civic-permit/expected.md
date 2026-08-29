# T008 — городское разрешение CIVIC-ORCHID

## Опорные параметры

- Опорное время: `2029-06-21T15:30:00+02:00`.
- Основная локаль: `de-DE`; дополнительная локаль: `en-GB`.
- Часовой пояс: `Europe/Berlin` (`CEST`, UTC+02:00 в датах сценария).
- Рабочий календарь: понедельник–пятница, берлинское местное время. В интервале расчёта `2029-06-19`–`2029-06-25` праздничных исключений нет.
- Порядок пяти рабочих дней после фактической публикации `2029-06-18`: `19`, `20`, `21`, `22`, `25` июня.

## Хронология и разрешение конфликта

1. `2029-06-04T08:42:00+02:00` — подана `CIVIC-ORCHID/BA-2029-417/V1`.
2. `2029-06-12T10:26:00+02:00` — форма `CIVIC-ORCHID/FORM-417-A2` создаёт `CIVIC-ORCHID/BA-2029-417/V2`; `V1` становится заменённой версией.
3. `2029-06-13T16:18:00+02:00` — письмо ведомства прогнозирует публикацию 14 июня и поэтому даёт предварительный результат `2029-06-21T17:00:00+02:00`.
4. `2029-06-18T09:10:00+02:00` — портал публикует уведомление позднее и явно связывает его с `V2`.
5. `2029-06-20` — утверждённый протокол подтверждает приоритет портала, владельца пакета, перенос слушания и переназначение подготовки.
6. `2029-06-21T15:05:00+02:00` — снимок портала по-прежнему показывает открытый срок `2029-06-25T17:00:00+02:00`.

## Конечный реестр: 5 записей

### R1 — пакет исправлений для CIVIC-ORCHID/BA-2029-417/V2

- Тип: действие.
- Действие: подать одним пакетом размерную схему пути эвакуации и легенду материалов.
- Владелец: `CIVIC-ORCHID/Mira-Falk`; алиас `CIVIC-ORCHID/M.-Falk` обозначает того же человека.
- Исходный срок: условный прогноз `2029-06-21T17:00:00+02:00`, если публикация состоялась бы 14 июня.
- Нормализованный действующий срок: `2029-06-25T17:00:00+02:00` (`2029-06-25T15:00:00Z`).
- Состояние: `open`.
- Слияние: `02-agency-email.txt` задаёт содержание и правило; `03-status-portal.txt` задаёт фактическую публикацию, `V2` и итоговый срок; `06-minutes.txt` задаёт владельца и подтверждает приоритет позднего источника.
- Источники и точные цитаты:
  - `input/02-agency-email.txt`: `Bitte reichen Sie die bemaßte Fluchtwegdarstellung und die Materiallegende zusammen als Ergänzungspaket ein.`
  - `input/02-agency-email.txt`: `Wenn die Veröffentlichung wie geplant am Donnerstag, 14.06.2029, erfolgt, endet die Frist am Donnerstag, 21.06.2029, 17:00 Uhr.`
  - `input/03-status-portal.txt`: `Tatsächliche Veröffentlichung: 18.06.2029 09:10 Europe/Berlin`
  - `input/03-status-portal.txt`: `Berechnetes Fristende: 25.06.2029 17:00 Europe/Berlin.`
  - `input/03-status-portal.txt`: `Portalverknüpfung: CIVIC-ORCHID/NOTICE-417-2 gehört ausschließlich zu CIVIC-ORCHID/BA-2029-417/V2.`
  - `input/06-minutes.txt`: `CIVIC-ORCHID/Mira-Falk übernimmt das Ergänzungspaket aus Fluchtwegdarstellung und Materiallegende für CIVIC-ORCHID/BA-2029-417/V2.`

### R2 — слушание CIVIC-ORCHID/HEAR-417

- Тип: событие, а не срок подготовки.
- Владелец: отсутствует; источники не назначают ответственного за само событие.
- Исходное время: `2029-06-28T10:00:00+02:00`–`2029-06-28T11:30:00+02:00`, затем отменено.
- Нормализованное действующее время: `2029-07-03T14:00:00+02:00`–`2029-07-03T15:30:00+02:00` (`12:00`–`13:30Z`).
- Состояние: `scheduled` / `confirmed`.
- Источники и точные цитаты:
  - `input/04-hearing-calendar.txt`: `Früherer Status: abgesagt; Änderung gespeichert am 20.06.2029 12:16.`
  - `input/04-hearing-calendar.txt`: `Neuer Beginn: 03.07.2029 14:00 Europe/Berlin`
  - `input/06-minutes.txt`: `Die Anhörung CIVIC-ORCHID/HEAR-417 wird vom 28.06.2029 10:00 auf den 03.07.2029 14:00 verschoben.`

### R3 — схема доступа к слушанию CIVIC-ORCHID/HEAR-417

- Тип: подготовительное действие, отдельное от R2.
- Действие: загрузить схему доступа в `CIVIC-ORCHID/ROOM-417`.
- Исходный владелец и срок: `CIVIC-ORCHID/Leon-Brandt`, `2029-06-27T16:00:00+02:00`.
- Действующий владелец и нормализованный срок: `CIVIC-ORCHID/Jonas-Reeve`, `2029-06-29T16:00:00+02:00` (`14:00Z`).
- Состояние: `open`, `reassigned` и `rescheduled`.
- Источники и точные цитаты:
  - `input/05-contractor-email.txt`: `CIVIC-ORCHID/Leon-Brandt lädt die Zugangsskizze bis 27.06.2029, 16:00 Uhr, in CIVIC-ORCHID/ROOM-417 hoch.`
  - `input/06-minutes.txt`: `CIVIC-ORCHID/Jonas-Reeve übernimmt die Zugangsskizze von CIVIC-ORCHID/Leon-Brandt und lädt sie bis 29.06.2029, 16:00 Uhr, in CIVIC-ORCHID/ROOM-417 hoch.`

### R4 — Farbblatt CIVIC-ORCHID/COLOR-471 для отдельной заявки

- Тип: действие.
- Связь: только `CIVIC-ORCHID/BA-2029-471/V1`, не `BA-2029-417`.
- Владелец: `CIVIC-ORCHID/Emil-Hart`.
- Исходный и нормализованный срок: `2029-06-26T12:00:00+02:00` (`10:00Z`).
- Состояние: `open`.
- Источники и точные цитаты:
  - `input/05-contractor-email.txt`: `Für CIVIC-ORCHID/BA-2029-471/V1 liefert CIVIC-ORCHID/Emil-Hart das Farbblatt bis 26.06.2029, 12:00 Uhr.`
  - `input/06-minutes.txt`: `CIVIC-ORCHID/BA-2029-471/V1 bleibt ein getrennter Vorgang; CIVIC-ORCHID/Emil-Hart bestätigt den Farbblatt-Termin 26.06.2029, 12:00 Uhr.`

### R5 — оригинал CIVIC-ORCHID/ANNEX-N7

- Тип: действие.
- Действие: предоставить подписанный оригинал приложения о согласии соседа.
- Владелец: неизвестен; поле ответственного пусто.
- Исходный срок: отсутствует.
- Нормализованный срок: отсутствует.
- Состояние: `open`.
- Источник и точные цитаты:
  - `input/07-correction-form.txt`: `Erklärung: „Das unterzeichnete Original von CIVIC-ORCHID/ANNEX-N7 wird nachgereicht.“`
  - `input/07-correction-form.txt`: `Feld „zuständige Person“ für das Original: [leer]`
  - `input/07-correction-form.txt`: `Feld „Termin“ für das Original: [leer]`

## Изменения жизненного цикла и связи

- R1: предварительный срок 21 июня заменён сроком 25 июня после фактической поздней публикации; обновляется именно `BA-2029-417/V2`.
- R2: событие 28 июня отменено и перенесено на 3 июля.
- R3: владелец изменён с `Leon-Brandt` на `Jonas-Reeve`, срок изменён с 27 на 29 июня.
- Правильное межфайловое слияние: письмо, портал и протокол образуют одну R1, а не три задачи.
- Похожая раздельная пара: `CIVIC-ORCHID/BA-2029-417/V2` и `CIVIC-ORCHID/BA-2029-471/V1` остаются разными заявками; R1/R3 не поглощают R4.
- Значимые отсутствия: у R2 нет владельца; у R5 нет владельца и срока. Эти поля остаются неизвестными.

## Точные положительные проверки

1. В реестре ровно 5 записей R1–R5.
2. R1 относится к `CIVIC-ORCHID/BA-2029-417/V2`, а не к заменённой `V1`.
3. R1 объединяет два документа в один пакет и имеет владельца `CIVIC-ORCHID/Mira-Falk`.
4. Действующий срок R1 равен `2029-06-25T17:00:00+02:00`; прогноз 21 июня не остаётся действующим.
5. R2 — подтверждённое событие 3 июля с отменённым прежним временем 28 июня.
6. R3 — отдельная подготовка; её новый владелец `CIVIC-ORCHID/Jonas-Reeve`, срок `2029-06-29T16:00:00+02:00`.
7. R4 относится только к `BA-2029-471/V1`, владелец `CIVIC-ORCHID/Emil-Hart`, срок `2029-06-26T12:00:00+02:00`.
8. R5 существует, но владелец и срок у неё отсутствуют.
9. Алиас `CIVIC-ORCHID/M.-Falk` разрешается в `CIVIC-ORCHID/Mira-Falk`.
10. `BA-2029-417` и `BA-2029-471` не сливаются, несмотря на близкие номера, общую текстуру и соседние строки в недельном списке.
11. Немецкие и английские строки портала о публикации и сроке описывают одно уведомление.
12. Пять рабочих дней считаются со следующего рабочего дня после 18 июня: 19, 20, 21, 22, 25 июня.

## Точные отрицательные проверки

1. `N01`: строка `Im Juni gingen in der Stelle 83 digitale Vorgänge ein; 61 davon waren beim ersten Import vollständig lesbar.` не создаёт задачу обработать 83 или 61 заявку и не задаёт срок.
2. `N02`: строка `Projektpostfach CIVIC-ORCHID/MAILBOX-OBP-4 | Ablagefrist nach Bürostandard: 36 Monate` не создаёт запись об архивировании и не добавляет R1 срок 36 месяцев.
3. `N03`: цитата `CIVIC-ORCHID/Leon-Brandt könnte im Juni die erste interne Wegeskizze prüfen, sofern Kapazität frei wird.` не возвращает владельца R3 к `Leon-Brandt` и не создаёт шестую задачу.
4. `N03`: цитата `Für CIVIC-ORCHID/BA-2029-417/V1 erwarten wir die interne Plansichtung am 10.06.; der Termin kann sich noch ändern.` не создаёт активную Plansichtung на 10 июня и не переводит R1 на `V1`.
5. `N04`: строка `Die Kostenschätzung nennt 471.300,00 EUR einschließlich einer Reserve von 8 Prozent.` не связывает `BA-2029-417` с `BA-2029-471` и не создаёт денежное обязательство.
6. `N04`: строка `Darin steht noch „Abgabe 30.09.2028“, weil dies der damalige Förderstichtag war.` не задаёт срок ни R1, ни R3, ни новой записи.
7. `N06`: строка `Hinweis des Formularsystems: Bei späteren Ergänzungen bleibt diese Fassungsnummer im Portal sichtbar.` не создаёт обязанность подать ещё одну версию и не открывает отдельную запись.
8. `N07`: строка `Agenda-Notiz: Eine mögliche Dachbegrünung kann in einer späteren Förderphase besprochen werden.` не создаёт проект озеленения, событие или срок.
9. `M10`: вопрос `Könnten wir vorsorglich eine Hebebühne für die Juliwoche reservieren, falls der Ortstermin zustande kommt?` не становится бронированием; протокол говорит, что вопрос вернут после подтверждённой Ortsbegehung.
10. `M10`: строка `Die Gruppe lehnt den Vorschlag ab, schon jetzt eine nächtliche Lärmmessung zu beauftragen.` не создаёт заказ на ночное измерение.

## Покрытие и доля контекста

- Механизмы: `M01 M02 M03 M04 M05 M08 M09 M10 M11 M13`.
- Обязательная связка: `M03+M09+M11` объединяет письмо, позднюю публикацию портала и протокол, считает рабочие дни и обновляет правильную версию `V2`.
- Шум: `N01 N02 N03 N04 N06 N07`.
- Авторская построчная классификация входов: 239 непустых строк; 59 строк нужны для создания или изменения R1–R5, а 180 строк составляют естественный контекст; доля контекста `75.3%`.
