# T009 — ATLAS-EVENT/ORBIT-27: поездка и мероприятие

Опорное время: `2026-09-16T10:00:00-04:00` (`America/New_York`) =
`2026-09-16T15:00:00+01:00` (`Europe/Lisbon`). Языки входа — английский и
португальский. Локали — `en-US` для явно нью-йоркских дат и `pt-PT` для явно
лиссабонских дат. В октябре 2026 года использованные здесь смещения равны EDT
`UTC-04:00` и WEST `UTC+01:00`. Более позднее свидетельство изменяет состояние
только той сущности, которую оно называет. Все люди, организации, адреса,
идентификаторы и сообщения в сценарии вымышлены.

## Конечный реестр — 9 записей

### 1. `ATLAS-EVENT/ORBIT-27` — публичное мероприятие

- Тип: событие.
- Владелец: Sofia Mendes.
- Конечное состояние: запланировано, не отменено и не перенесено.
- Исходная дата: `22/10/2026, 15:00-18:00`, время Лиссабона.
- Нормализованный интервал: `2026-10-22T15:00:00+01:00` —
  `2026-10-22T18:00:00+01:00`, `Europe/Lisbon`.
- Источники: `input/04-venue-email.eml`, `input/01-master-itinerary.txt`,
  `input/05-event-calendar.ics`, `input/02-organizer-chat.txt`,
  `input/07-planning-transcript.txt`.
- Точные цитаты:
  - `input/04-venue-email.eml`: `We hold ATLAS-EVENT/Ribeira Forum, Sala Azul, for ATLAS-EVENT/ORBIT-27 on 22/10/2026, 15:00-18:00 Lisbon time.`
  - `input/04-venue-email.eml`: `Sofia Mendes is the organizer responsible for the public event.`
  - `input/02-organizer-chat.txt`: `ATLAS-EVENT/ORBIT-27 remains on 22 October at 15:00 Lisbon time.`

### 2. `ATLAS-EVENT/PREP-204` — подготовка выступающего

- Тип: действие/подготовительная встреча, отдельная от публичного события.
- Владелец: Renata Silva.
- Конечное состояние: открыто и запланировано на новое время.
- Исходный срок: `21/10/2026 16:00`, время Лиссабона
  (`2026-10-21T16:00:00+01:00`).
- Промежуточное состояние: исходный слот отменён после изменения рейса.
- Конечный срок: `22 October 2026 at 12:15 Lisbon time`.
- Нормализованный конечный интервал: `2026-10-22T12:15:00+01:00` —
  `2026-10-22T13:00:00+01:00`, `Europe/Lisbon`.
- Источники: `input/01-master-itinerary.txt`, `input/08-carrier-notice.eml`,
  `input/02-organizer-chat.txt`, `input/05-event-calendar.ics`,
  `input/07-planning-transcript.txt`.
- Точные цитаты:
  - `input/01-master-itinerary.txt`: `ATLAS-EVENT/PREP-204 is planned for 21/10/2026 at 16:00 in Lisbon.`
  - `input/02-organizer-chat.txt`: `Cancel the 21 October 16:00 slot for ATLAS-EVENT/PREP-204 because the replacement flight lands the next morning.`
  - `input/02-organizer-chat.txt`: `I will run ATLAS-EVENT/PREP-204 on 22 October at 12:15 Lisbon time.`
  - `input/07-planning-transcript.txt`: `The replacement prep is 22 October at 12:15 Lisbon time, after arrival and before the 15:00 event.`

### 3. `ATLAS-EVENT/BOOK-431` — подтверждение AV-пакета площадки

- Тип: действие.
- Исходный владелец/контакт: Marco Lee.
- Конечный владелец: Sofia Mendes.
- Конечное состояние: открыто; владелец изменён, срок не изменён.
- Исходный срок: `02/10/2026 at 17:00 Lisbon time`.
- Нормализованный срок: `2026-10-02T17:00:00+01:00`, `Europe/Lisbon`.
- Источники: `input/04-venue-email.eml`, `input/02-organizer-chat.txt`,
  `input/07-planning-transcript.txt`.
- Точные цитаты:
  - `input/04-venue-email.eml`: `Confirm ATLAS-EVENT/BOOK-431 by 02/10/2026 at 17:00 Lisbon time to keep the AV package.`
  - `input/04-venue-email.eml`: `Marco Lee is the contact listed for that confirmation in our current portal snapshot.`
  - `input/02-organizer-chat.txt`: `Marco, please hand ATLAS-EVENT/BOOK-431 to me; I own the AV confirmation now.`

### 4. `ATLAS-EVENT/BOOK-413` — подтверждение переговорной в отеле

- Тип: действие.
- Владелец: Marta Vale.
- Конечное состояние: открыто; срок и владелец не изменены.
- Исходный срок: `October 5 at noon New York time`.
- Нормализованный срок: `2026-10-05T12:00:00-04:00`,
  `America/New_York`.
- Источники: `input/03-hotel-email.eml`, `input/02-organizer-chat.txt`,
  `input/07-planning-transcript.txt`.
- Точные цитаты:
  - `input/03-hotel-email.eml`: `Marta Vale must confirm ATLAS-EVENT/BOOK-413 by October 5 at noon New York time.`
  - `input/02-organizer-chat.txt`: `I still own the hotel meeting-room confirmation under ATLAS-EVENT/BOOK-413.`
  - `input/07-planning-transcript.txt`: `ATLAS-EVENT/BOOK-413 stays with me, and its hotel deadline stays October 5 at noon New York time.`

### 5. `ATLAS-EVENT/TRANSFER-204` — встреча в аэропорту

- Тип: событие/заказ услуги.
- Владелец до отмены: `ATLAS-EVENT/Travel Desk`.
- Конечное состояние: отменено; новая встреча не назначена.
- Исходное время: `21 October 2026 at 08:20 Lisbon time`.
- Нормализованное исходное время: `2026-10-21T08:20:00+01:00`,
  `Europe/Lisbon`.
- Источники: `input/01-master-itinerary.txt`, `input/02-organizer-chat.txt`.
- Точные цитаты:
  - `input/01-master-itinerary.txt`: `ATLAS-EVENT/TRANSFER-204 is booked for 21 October at 08:20 Lisbon time; ATLAS-EVENT/Travel Desk owns the booking.`
  - `input/02-organizer-chat.txt`: `ATLAS-EVENT/TRANSFER-204 is cancelled with the car service; no replacement pickup is booked.`

### 6. `ATLAS-EVENT/EXPENSE-27` — сверка чеков после мероприятия

- Тип: действие.
- Владелец: неизвестен. Joana Reis ведёт структуру таблицы, но это не назначение
  владельца сверки.
- Конечное состояние: открыто, владелец не назначен.
- Исходный срок: `27 October at 17:00 New York time`.
- Нормализованный срок: `2026-10-27T17:00:00-04:00`,
  `America/New_York`.
- Источник: `input/07-planning-transcript.txt`.
- Точные цитаты:
  - `input/07-planning-transcript.txt`: `The receipts for ATLAS-EVENT/EXPENSE-27 must be reconciled by 27 October at 17:00 New York time.`
  - `input/07-planning-transcript.txt`: `We have not assigned an owner for ATLAS-EVENT/EXPENSE-27.`
  - `input/07-planning-transcript.txt`: `I maintain the spreadsheet layout, but ownership of that reconciliation was not decided here.`

### 7. `ATLAS-EVENT/AW204` — исходный перелёт Нью-Йорк—Лиссабон

- Тип: событие поездки.
- Владелец как поле обязательства: не указан; участник — Renata Silva.
- Конечное состояние: отменено поздним уведомлением перевозчика.
- Исходное время: вылет `20 October 2026 19:30 EDT`, прилёт
  `21 October 2026 07:25 WEST`.
- Нормализованный интервал: `2026-10-20T19:30:00-04:00` —
  `2026-10-21T07:25:00+01:00`.
- Источники: `input/01-master-itinerary.txt`, `input/08-carrier-notice.eml`.
- Точные цитаты:
  - `input/01-master-itinerary.txt`: `Outbound: ATLAS-EVENT/AW204, New York (JFK) 20 October 2026 19:30 EDT.`
  - `input/08-carrier-notice.eml`: `ATLAS-EVENT/AW204 on 20 October is cancelled.`

### 8. `ATLAS-EVENT/AW208` — заменяющий перелёт Нью-Йорк—Лиссабон

- Тип: событие поездки.
- Владелец как поле обязательства: не указан; участник — Renata Silva.
- Конечное состояние: запланировано.
- Исходное и конечное время: вылет `21 October 2026 at 20:05 EDT`, прилёт
  `22 October 2026 at 08:10 WEST`.
- Нормализованный интервал: `2026-10-21T20:05:00-04:00` —
  `2026-10-22T08:10:00+01:00`.
- Источник: `input/08-carrier-notice.eml`.
- Точная цитата:
  - `input/08-carrier-notice.eml`: `You are rebooked on ATLAS-EVENT/AW208, departing New York on 21 October 2026 at 20:05 EDT and arriving Lisbon on 22 October 2026 at 08:10 WEST.`

### 9. `ATLAS-EVENT/AW219` — обратный перелёт Лиссабон—Нью-Йорк

- Тип: событие поездки.
- Владелец как поле обязательства: не указан; участник — Renata Silva.
- Конечное состояние: запланировано и не изменено уведомлением.
- Исходное и конечное время вылета: `24 October 2026 at 11:35 WEST`.
- Нормализованное время вылета: `2026-10-24T11:35:00+01:00`,
  `Europe/Lisbon`.
- Время прилёта отсутствует во входах и остаётся неизвестным.
- Источники: `input/01-master-itinerary.txt`, `input/08-carrier-notice.eml`.
- Точная цитата:
  - `input/08-carrier-notice.eml`: `Your return segment ATLAS-EVENT/AW219 remains Lisbon 24 October at 11:35 WEST.`

## Хронология и изменения жизненного цикла

1. `2026-09-02`: письмо площадки создаёт публичное событие
   `ATLAS-EVENT/ORBIT-27` и действие `ATLAS-EVENT/BOOK-431`; Marco Lee указан
   текущим контактом AV-подтверждения.
2. `2026-09-05`: версия 3 маршрута создаёт исходный рейс
   `ATLAS-EVENT/AW204`, обратный рейс `ATLAS-EVENT/AW219`, подготовку
   `ATLAS-EVENT/PREP-204` на 21 октября и трансфер
   `ATLAS-EVENT/TRANSFER-204`.
3. `2026-09-07`: письмо отеля создаёт отдельное действие
   `ATLAS-EVENT/BOOK-413` с нью-йоркским сроком.
4. `2026-09-10`: Sofia Mendes принимает `ATLAS-EVENT/BOOK-431` у Marco Lee.
   Это переназначение, а не новая запись.
5. `2026-09-14 12:18 EDT`: перевозчик отменяет `ATLAS-EVENT/AW204` и создаёт
   замену `ATLAS-EVENT/AW208`, которая прибывает 22 октября в 08:10 WEST.
6. `2026-09-14 17:33-17:43 WEST`: организаторы отменяют исходный слот
   `ATLAS-EVENT/PREP-204`, назначают ту же подготовку на 22 октября 12:15 WEST
   и отменяют `ATLAS-EVENT/TRANSFER-204`. Публичное мероприятие остаётся 22
   октября в 15:00 WEST.
7. `2026-09-14 18:05 WEST`: экспорт календаря подтверждает одну идентичность
   `ATLAS-EVENT/PREP-204`: последовательность 2 отменена, последовательность 3
   активна в новое время.
8. `2026-09-15`: стенограмма создаёт `ATLAS-EVENT/EXPENSE-27`, фиксирует срок
   и оставляет владельца неизвестным.

Изменения жизненного цикла: отмена `ATLAS-EVENT/AW204`; отмена старого времени
и перенос `ATLAS-EVENT/PREP-204`; переназначение `ATLAS-EVENT/BOOK-431`;
отмена `ATLAS-EVENT/TRANSFER-204`. Это четыре независимых изменения.

## Обязательное взаимодействие механизмов

- `M03+M07+M09`: маршрут, уведомление перевозчика, чат, календарь и стенограмма
  относятся к одной подготовке `ATLAS-EVENT/PREP-204`. Прилёт замены в
  `2026-10-22T08:10:00+01:00` делает исходный слот
  `2026-10-21T16:00:00+01:00` невозможным. Старый слот отменяется, а та же
  подготовка получает новый срок `2026-10-22T12:15:00+01:00`. Дубликат
  подготовки не создаётся.
- Дата публичного события `2026-10-22T15:00:00+01:00` не заменяет сроки
  бронирований. `ATLAS-EVENT/BOOK-431` остаётся на 2 октября 17:00 Лиссабон,
  а `ATLAS-EVENT/BOOK-413` — на 5 октября 12:00 Нью-Йорк.
- Похожая пара сохраняется раздельно: `ATLAS-EVENT/BOOK-431` относится к
  AV-пакету `ATLAS-EVENT/Ribeira Forum`; `ATLAS-EVENT/BOOK-413` относится к
  переговорной `ATLAS-EVENT/Cais Meridian Hotel`. У них разные владельцы,
  поставщики, сроки и предметы.
- Межфайловое слияние обязательно для `ATLAS-EVENT/ORBIT-27`,
  `ATLAS-EVENT/PREP-204`, `ATLAS-EVENT/BOOK-431`,
  `ATLAS-EVENT/BOOK-413`, `ATLAS-EVENT/TRANSFER-204`,
  `ATLAS-EVENT/AW204` и `ATLAS-EVENT/AW219`.

## Точные положительные утверждения

1. В конечном реестре ровно 9 записей, перечисленных выше.
2. `ATLAS-EVENT/ORBIT-27` запланировано на 22 октября 15:00 WEST и имеет
   владельца Sofia Mendes.
3. `ATLAS-EVENT/PREP-204` — одна запись, а не две записи календаря.
4. Исходное время `ATLAS-EVENT/PREP-204` отменено.
5. Конечное время `ATLAS-EVENT/PREP-204` равно 22 октября 12:15 WEST.
6. Владелец подготовки — Renata Silva.
7. `ATLAS-EVENT/BOOK-431` переназначено с Marco Lee на Sofia Mendes.
8. Срок `ATLAS-EVENT/BOOK-431` равен 2 октября 17:00 WEST.
9. `ATLAS-EVENT/BOOK-413` остаётся отдельным от `ATLAS-EVENT/BOOK-431`.
10. Владелец `ATLAS-EVENT/BOOK-413` — Marta Vale, срок — 5 октября 12:00 EDT.
11. `ATLAS-EVENT/TRANSFER-204` отменено, замена отсутствует.
12. `ATLAS-EVENT/EXPENSE-27` открыто до 27 октября 17:00 EDT, а владелец
    неизвестен.
13. `ATLAS-EVENT/AW204` отменено, но не удалено из истории.
14. `ATLAS-EVENT/AW208` — отдельный активный заменяющий рейс.
15. `ATLAS-EVENT/AW219` остаётся активным; время прилёта не выдумывается.
16. Время подготовки после изменения рейса остаётся до начала события на 2 часа
    45 минут.

## Не создавать и не смешивать

1. `N01`: фраза `The transfer desk reported an average curb wait of eleven minutes in August.`
   не создаёт новый трансфер, срок ожидания или действие по метрике.
2. `N01`: фраза `The metro airport line carried 7.4 million passengers in the last published year.`
   не создаёт задачу по пассажиропотоку или отдельное событие.
3. `N02`: стандартная строка перевозчика `Online check-in opens 24 hours before departure.`
   не создаёт производное напоминание о регистрации.
4. `N02`: строка подписи `ATLAS-EVENT/Lumen Arc Collective | 14 Paper Harbor Way | New York`
   не создаёт событие по адресу или действие для организации.
5. `N03`: цитата из истории отеля `Last year's draft mentioned a 12 September review and a EUR 204.20 snack estimate.`
   не создаёт срок 12 сентября 2026, проверку меню или расход текущего события.
6. `N03`: цитата площадки `The 2024 event finished at 18:12 after a twelve-minute audience question.`
   не завершает `ATLAS-EVENT/ORBIT-27` и не меняет его время.
7. `N04`: CSV-строка `ATLAS-EVENT/EXP-2025-005,2025,venue,2025-08-15,4310.00,EUR,Joana Reis,closed prior programme invoice`
   не создаёт текущую оплату, владельца или срок.
8. `N04`: фраза `The projector lamp counter reads 431 hours after the September maintenance cycle.`
   не относится к `ATLAS-EVENT/BOOK-431` и не меняет его срок.
9. `N04`: сумма `EUR 413.00` в письме отеля и строка оценки
   `ATLAS-EVENT/EXP-2026-EST-06` не являются номером новой брони и не сливают
   расход с `ATLAS-EVENT/BOOK-413`.
10. `N07`: календарное описание `Doors 14:30. Panel order revision 6. The 2024 archive counted 88 occupied seats.`
    не создаёт отдельное событие открытия дверей, задачу по порядку панели или
    текущую запись на 88 мест.
11. `N07`: строка `The programme note estimates 84 guests, compared with 79 at last year's gathering.`
    не создаёт обязательство набрать 84 гостя или прошлое событие на 79 гостей.
12. `N10`: реплика `Gosto da ideia de café no terraço se o vento estiver fraco.`
    не создаёт встречу на террасе, бронирование или условную задачу.
13. `N10`: реплика `We can decide where to drink coffee when we see the wind that morning.`
    не создаёт действие со сроком утром 22 октября.

## Значимые отсутствия

- У `ATLAS-EVENT/EXPENSE-27` нет владельца. Нельзя назначать Joana Reis только
  потому, что она ведёт таблицу расходов.
- У `ATLAS-EVENT/AW219` нет времени прилёта. Нельзя вычислять или выдумывать его
  из других перелётов.
- После отмены `ATLAS-EVENT/TRANSFER-204` нет новой встречи. Нельзя создавать её
  из факта прибытия `ATLAS-EVENT/AW208`.
