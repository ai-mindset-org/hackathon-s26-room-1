# T014 — многоязычные региональные операции

Все данные в сценарии синтетические. Имена, организации, адреса, проекты и
идентификаторы вымышлены.

## Опорная точка и правила времени

- Опорное время: 30.08.2026 00:30 Asia/Tbilisi
  (2026-08-29T20:30:00Z), после всех восьми входных файлов.
- Локали источников: ru-GE для чата Тбилиси, en-GB для лондонской почты и
  сменной заметки, es-MX для чата, CRM, транскрипта и сводки Мехико.
- Часовые пояса: Asia/Tbilisi (UTC+04:00), Europe/London (UTC+01:00 в эту
  дату), America/Mexico_City (UTC-06:00).
- Форматы дат: dd.mm.yyyy в Тбилиси, dd/mm/yyyy в London и Mexico City.
- При конфликте применяется более позднее прямое обновление той же записи.
  Короткое имя Atlas не является идентификатором; идентификатором служит полный
  ключ POLYGLOT-OPS с региональным суффиксом.

## Итоговый реестр: 5 записей

### R1. Финальный пакет передачи причала — POLYGLOT-OPS/ATLAS-TBS

- Тип: действие.
- Владелец: Майя Бекаури. Варианты имени в источниках относятся к одному
  вымышленному человеку: Майя Бекаури, Maya B., M. Bekauri.
- Исходный срок: 31.08.2026 18:00 Asia/Tbilisi
  (2026-08-31T14:00:00Z).
- Итоговый срок: 01/09/2026 11:30 Asia/Tbilisi
  (2026-09-01T07:30:00Z).
- Итоговое состояние: открыто, срок перенесён.
- Хронология: создание и исходный срок в чате Тбилиси 28.08; английское письмо
  28.08 подтверждает алиас и полный ключ; испанская сводка от 29.08 13:15
  America/Mexico_City является последним прямым обновлением и заменяет срок.
- Источники: input/01-regional-chat-tbilisi.txt,
  input/03-operations-email.txt, input/08-manager-summary.txt.
- Точные цитаты:
  - [28.08.2026 16:42 Asia/Tbilisi] Майя Бекаури: Я подготовлю финальный пакет передачи причала для POLYGLOT-OPS/ATLAS-TBS.
  - [28.08.2026 16:44 Asia/Tbilisi] Ираклий: Майя, отправь пакет до 31.08.2026 18:00 по времени Тбилиси.
  - Maya B. owns the final dock handover packet for POLYGLOT-OPS/ATLAS-TBS; keep the current Tbilisi deadline until management posts a revision.
  - POLYGLOT-OPS/ATLAS-TBS: M. Bekauri mantiene la entrega del paquete; el nuevo vencimiento es 01/09/2026 a las 11:30, hora de Tbilisi.

### R2. Два места для транспорта — POLYGLOT-OPS/ATLAS-MX

- Тип: действие.
- Владелец: Diego Serrano.
- Исходный и итоговый срок: 29/08/2026 12:00
  America/Mexico_City (2026-08-29T18:00:00Z).
- Итоговое состояние: завершено 29/08/2026 12:07
  America/Mexico_City (2026-08-29T18:07:00Z).
- Хронология: CRM фиксирует отдельную открытую запись C-4478; более позднее
  прямое подтверждение Diego в транскрипте завершает её.
- Источники: input/06-crm-export.txt,
  input/07-operations-transcript.txt, input/08-manager-summary.txt.
- Точные цитаты:
  - C-4478|POLYGLOT-OPS/ATLAS-MX|Confirmar dos espacios de vehículo|Diego Serrano|OPEN|due=29/08/2026 12:00 America/Mexico_City
  - [12:07] Diego: Confirmo completado POLYGLOT-OPS/ATLAS-MX: los dos espacios de vehículo quedaron reservados a las 12:07 hora de Ciudad de México.

### R3. Пересмотренная последовательность причалов — POLYGLOT-OPS/EMBER-LDN

- Тип: действие.
- Исходный владелец: Omar Dene.
- Итоговый владелец: Priya Holt.
- Исходный срок: 29/08/2026 15:00 Europe/London
  (2026-08-29T14:00:00Z).
- Итоговый срок: 29/08/2026 16:30 Europe/London
  (2026-08-29T15:30:00Z).
- Итоговое состояние: открыто, просрочено, переназначено и перенесено.
- Хронология: письмо от 28.08 назначает Omar; сменная заметка от 29.08 08:05
  London передаёт запись Priya и заменяет срок.
- Источники: input/03-operations-email.txt,
  input/05-shift-notes-london.txt, input/08-manager-summary.txt.
- Точные цитаты:
  - Omar, please send the revised berth sequence for POLYGLOT-OPS/EMBER-LDN by 29/08/2026 15:00 London time.
  - POLYGLOT-OPS/EMBER-LDN: Priya Holt takes over the revised berth sequence from Omar Dene.
  - New delivery time for that sequence: 29/08/2026 16:30 London time, replacing 15:00.

### R4. Звонок поставщика — POLYGLOT-OPS/COPPER-TBS

- Тип: событие.
- Владелец или организатор: отсутствует в данных; не угадывать.
- Исходное и итоговое время: 01.09.2026 15:00–15:45 Asia/Tbilisi
  (2026-09-01T11:00:00Z–2026-09-01T11:45:00Z).
- Итоговое состояние: запланировано.
- Источник: input/04-shared-calendar.txt.
- Точная цитата:
  - 01.09.2026 15:00–15:45 Asia/Tbilisi | POLYGLOT-OPS/COPPER-TBS | llamada de proveedor / vendor call | sala Narikala
- Поле Organizer в экспорте пустое. Supplier desk и Tbilisi operations —
  участники, а не подтверждённые владельцы.

### R5. Фотографии недостающих пломб — POLYGLOT-OPS/RIO-MX

- Тип: действие.
- Владелец: Lucía Andrade.
- Исходный и итоговый срок: отсутствует в данных; не угадывать.
- Итоговое состояние: открыто.
- Хронология: Lucía берёт обязательство в чате; CRM связывает то же действие с
  C-4421, тем же владельцем и пустым полем due.
- Источники: input/02-regional-chat-mexico.txt,
  input/06-crm-export.txt, input/08-manager-summary.txt.
- Точные цитаты:
  - [28/08/2026 09:42 America/Mexico_City] Lucía Andrade: Yo enviaré las fotos de los sellos que faltan para POLYGLOT-OPS/RIO-MX.
  - C-4421|POLYGLOT-OPS/RIO-MX|Enviar fotos de los sellos faltantes|Lucía Andrade|OPEN|due=

## Изменения жизненного цикла и связи

1. R1: срок перенесён с 31.08.2026 18:00 Tbilisi на 01.09.2026 11:30 Tbilisi.
2. R2: открытая запись C-4478 завершена прямым подтверждением в транскрипте.
3. R3: владелец изменён с Omar Dene на Priya Holt.
4. R3: срок перенесён с 15:00 на 16:30 London.
5. Правильное межфайловое слияние: R1 объединяет три языка и три формы имени
   только внутри полного ключа POLYGLOT-OPS/ATLAS-TBS.
6. Похожая отдельная пара: R1 POLYGLOT-OPS/ATLAS-TBS и R2
   POLYGLOT-OPS/ATLAS-MX остаются разными записями. У них разные регионы,
   действия, владельцы, сроки и состояния.
7. Значимое отсутствие: у R4 нет владельца или организатора, а у R5 нет срока.

## Точные положительные проверки

1. Создать ровно одну R1 для финального пакета POLYGLOT-OPS/ATLAS-TBS.
2. Объединить Майя Бекаури, Maya B. и M. Bekauri как владельца R1.
3. Заменить исходный срок R1 более поздним сроком 01.09.2026 11:30 Tbilisi.
4. Создать отдельную R2 для двух мест транспорта POLYGLOT-OPS/ATLAS-MX.
5. Завершить R2 по подтверждению Diego в 12:07 Mexico City.
6. Не применять обновление R1 к R2 и не применять завершение R2 к R1.
7. Создать R3 из письма и обновить её из сменной заметки.
8. Установить итогового владельца R3 Priya Holt.
9. Установить итоговый срок R3 29/08/2026 16:30 London.
10. Создать R4 как событие 01.09.2026 15:00–15:45 Tbilisi.
11. Оставить владельца или организатора R4 неизвестным.
12. Создать одну R5 из чата и CRM.
13. Установить владельца R5 Lucía Andrade.
14. Оставить срок R5 неизвестным.

## Точные отрицательные проверки

1. N01: строка «Дневная смена закрыла 38 воротных операций, медиана ожидания
   составила 14 минут» не создаёт действие со сроком 14 минут и не создаёт
   новую запись.
2. N02: строка «POLYGLOT-OPS internal routing: London desk / extension 204»
   не назначает London desk владельцем и не создаёт действие с номером 204.
3. N03: цитата «Omar sent the July access roster before 12/08/2026 12:00 and
   Celia archived it after lunch.» не открывает новую запись о roster и не
   заменяет срок R3.
4. N04: строка «The dashboard build number is 29.08.118, despite looking like
   a local date.» не создаёт срок 29.08 и не меняет R1.
5. N04: CAL-0901-1500 не создаёт отдельное событие и не становится владельцем
   или идентификатором R4.
6. N08: повреждённый preview
   «search_preview|POLYGLOT-OPS/ATLAS-??|M4ya B.|dock note|31.08» не создаёт
   третью Atlas-запись, не назначает владельца M4ya B. и не меняет срок R1.
7. N10: реплика «Si el clima mejora, quizá comamos en el patio el lunes.» не
   создаёт встречу, задачу или срок на понедельник.
8. N01: строка «El consumo del generador bajó 4,7 % esta semana» не создаёт
   действие для Diego и не назначает процент сроком или приоритетом.
9. N08: строка «row_recovery|segment 08|crc mismatch|preview retained» не
   создаёт действие восстановления и не связывает обрезанный preview с R1/R2.

## Покрываемые механизмы

- M01: извлечение пяти записей и их полей.
- M03, M08, M15: R1 объединяется между русским, английским и испанским
  источниками, включая три формы имени владельца.
- M04: одноимённые Atlas в Tbilisi и Mexico City остаются разными.
- M05: сроки R1 и R3 перенесены.
- M06: R2 завершена.
- M09: локальные форматы и три часовых пояса нормализованы с сохранением
  локального времени.
- M11: поздние прямые обновления побеждают более ранние значения только в той
  же записи.
- M13: отсутствие владельца R4 и срока R5 сохраняется как отсутствие.
