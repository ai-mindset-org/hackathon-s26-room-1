# T005 — Полевой ремонт CEDAR-FIELD

## Контекст интерпретации

- Опорное время: `2026-09-04T10:30:00-05:00`.
- Локаль: `es-CO`; даты во входах имеют формат `dd/mm/yyyy` или `dd/mm`.
- Часовой пояс: `America/Bogota` (`UTC-05:00`, без перехода на летнее время).
- Все относительные сроки вычисляются от локальной отметки сообщения. Фраза `mañana antes del mediodía` из SMS от `03/09/2026 10:45` означает `2026-09-04T12:00:00-05:00`.
- Порядок свидетельств определяется датой и временем внутри источника, а не именем файла.

## Конечный реестр: 6 записей

### 1. `CEDAR-FIELD/VISIT-4821` — отменённый выезд к `CEDAR-FIELD/UNIT-CH-17`

- Тип: событие, выезд техника.
- Владелец: Camila Ríos; `Cami` является её алиасом.
- Конечное состояние: `cancelled`.
- Исходный срок: `04/09/2026 08:30 America/Bogota`.
- Исходный нормализованный срок: `2026-09-04T08:30:00-05:00`.
- Изменённый срок до отмены: `05/09/2026 10:00 America/Bogota`.
- Изменённый нормализованный срок: `2026-09-05T10:00:00-05:00`.
- Источники: `input/01-work-order.txt`, `input/02-sms-export.txt`, `input/05-visit-calendar.txt`, `input/07-dispatcher-note.txt`.
- Точные цитаты:
  - `Programar CEDAR-FIELD/VISIT-4821 para el 04/09/2026 a las 08:30, hora de Bogotá.`
  - `[03/09/2026 08:15] Lucía: Reprogramamos CEDAR-FIELD/VISIT-4821 del 04/09 a las 08:30 al sábado 05/09 a las 10:00, hora de Bogotá.`
  - `08:56 — Cancelar CEDAR-FIELD/VISIT-4821, antes prevista para el 05/09 a las 10:00, hora de Bogotá.`

### 2. `CEDAR-FIELD/CONF-4821` — подтверждение доступа для выезда 4821

- Тип: действие подготовки к событию `CEDAR-FIELD/VISIT-4821`.
- Владелец: Lucía Fajardo.
- Конечное состояние: `cancelled` из-за отмены зависимого выезда.
- Исходный срок: `03/09/2026 14:00 America/Bogota`.
- Исходный нормализованный срок: `2026-09-03T14:00:00-05:00`.
- Изменённый срок до отмены: `04/09/2026 16:00 America/Bogota`.
- Изменённый нормализованный срок: `2026-09-04T16:00:00-05:00`.
- Источники: `input/01-work-order.txt`, `input/02-sms-export.txt`, `input/05-visit-calendar.txt`, `input/07-dispatcher-note.txt`.
- Точные цитаты:
  - `Lucía Fajardo debe confirmar con recepción el acceso CEDAR-FIELD/CONF-4821 antes del 03/09/2026 a las 14:00.`
  - `[03/09/2026 08:18] Lucía: Yo confirmaré CEDAR-FIELD/CONF-4821 con recepción el viernes 04/09 antes de las 16:00.`
  - `08:58 — Cancelar también CEDAR-FIELD/CONF-4821; ya no se requiere la llamada de acceso de esta tarde.`

### 3. `CEDAR-FIELD/VISIT-4827` — выезд к `CEDAR-FIELD/UNIT-CH-71`

- Тип: событие, отдельный выезд техника.
- Владелец: Carlos Peña.
- Конечное состояние: `scheduled`.
- Исходный и текущий срок: `07/09/2026 09:30 America/Bogota`.
- Нормализованный срок: `2026-09-07T09:30:00-05:00`.
- Источники: `input/01-work-order.txt`, `input/05-visit-calendar.txt`, `input/07-dispatcher-note.txt`.
- Точные цитаты:
  - `Programar CEDAR-FIELD/VISIT-4827 para el lunes 07/09/2026 a las 09:30, hora de Bogotá.`
  - `09:10 — CEDAR-FIELD/VISIT-4827 para CEDAR-FIELD/UNIT-CH-71 sigue programada el lunes 07/09 a las 09:30 con Carlos Peña.`

### 4. `CEDAR-FIELD/ACT-4827` — загрузка акта после выезда 4827

- Тип: действие.
- Владелец: неизвестен. Пустое поле календаря и заметка диспетчера подтверждают отсутствие назначения; имя нельзя угадывать по владельцу связанного выезда.
- Конечное состояние: `open`.
- Исходный и текущий срок: `08/09/2026 17:00 America/Bogota`.
- Нормализованный срок: `2026-09-08T17:00:00-05:00`.
- Источники: `input/01-work-order.txt`, `input/05-visit-calendar.txt`, `input/07-dispatcher-note.txt`.
- Точные цитаты:
  - `El acta CEDAR-FIELD/ACT-4827 debe cargarse el 08/09/2026 antes de las 17:00; la orden todavía no nombra responsable.`
  - `09:13 — CEDAR-FIELD/ACT-4827 mantiene fecha límite 08/09 a las 17:00; el campo de responsable sigue vacío.`

### 5. `CEDAR-FIELD/PART-7742` — заказ комплекта для `CEDAR-FIELD/UNIT-PM-42`

- Тип: заказ детали с обязательством по доставке.
- Владелец: Juliana Mena.
- Конечное состояние: `ordered`.
- Исходный и текущий срок доставки: `08/09/2026 15:00 America/Bogota`.
- Нормализованный срок: `2026-09-08T15:00:00-05:00`.
- Источники: `input/04-warehouse-email.txt`, `input/07-dispatcher-note.txt`.
- Точные цитаты:
  - `The parts portal accepted order CEDAR-FIELD/PART-7742 for pump CEDAR-FIELD/UNIT-PM-42 at CEDAR-FIELD/PLANTA-MIRTO.`
  - `Portal commitment: “Expected delivery: 08/09/2026 by 15:00 America/Bogota.”`
  - `09:16 — Mantener CEDAR-FIELD/PART-7742: pertenece a CEDAR-FIELD/UNIT-PM-42 en CEDAR-FIELD/PLANTA-MIRTO y Juliana continúa esperando la entrega.`

### 6. `CEDAR-FIELD/PHOTO-4821` — загрузка фотографий уже выполненной инспекции

- Тип: действие.
- Исходный владелец: Camila Ríos (`Cami`).
- Конечный владелец: Diego Orduz.
- Конечное состояние: `open`.
- Исходный срок: `03/09/2026 17:00 America/Bogota`.
- Исходный нормализованный срок: `2026-09-03T17:00:00-05:00`.
- Изменённый срок: `mañana antes del mediodía` в сообщении от `03/09/2026 10:45`.
- Изменённый нормализованный срок: `2026-09-04T12:00:00-05:00`.
- Источники: `input/03-technician-log.txt`, `input/02-sms-export.txt`, `input/06-inspection-report.txt`, `input/07-dispatcher-note.txt`.
- Точные цитаты:
  - `02/09 15:18 — Lucía pidió cargar CEDAR-FIELD/PHOTO-4821 antes del 03/09 a las 17:00; responsable inicial: Cami.`
  - `[03/09/2026 10:45] Lucía: Diego Orduz toma CEDAR-FIELD/PHOTO-4821 en lugar de Cami y subirá las fotos mañana antes del mediodía.`
  - `Se tomaron catorce fotografías y tres clips para el expediente.`
  - `06:38 — Diego Orduz abrió CEDAR-FIELD/PHOTO-4821 y confirmó que hará la carga antes de las 12:00 de hoy.`

## Хронология и изменения жизненного цикла

1. `01/09`: созданы два разных выезда: `CEDAR-FIELD/VISIT-4821` для `CEDAR-FIELD/UNIT-CH-17` и `CEDAR-FIELD/VISIT-4827` для `CEDAR-FIELD/UNIT-CH-71`.
2. `01/09`: портал принял `CEDAR-FIELD/PART-7742` для третьего актива, `CEDAR-FIELD/UNIT-PM-42`.
3. `02/09`: `CEDAR-FIELD/PHOTO-4821` назначена Cami со сроком `03/09 17:00`.
4. `03/09 08:15`: `CEDAR-FIELD/VISIT-4821` перенесён с `04/09 08:30` на `05/09 10:00`.
5. `03/09 08:18`: связанное подтверждение `CEDAR-FIELD/CONF-4821` перенесено с `03/09 14:00` на `04/09 16:00`.
6. `03/09 10:45`: `CEDAR-FIELD/PHOTO-4821` переназначена с Cami на Diego Orduz и перенесена на `04/09 12:00`.
7. `04/09 08:56–08:58`: диспетчер отменяет `CEDAR-FIELD/VISIT-4821` и зависимую `CEDAR-FIELD/CONF-4821`.
8. `04/09 09:10–09:16`: диспетчер сохраняет `CEDAR-FIELD/VISIT-4827`, `CEDAR-FIELD/ACT-4827` и заказ `CEDAR-FIELD/PART-7742` для другого актива.

## Межфайловые связи и раздельные сущности

- Правильное слияние: четыре источника описывают одну запись `CEDAR-FIELD/VISIT-4821`; орфографически повреждённая строка `CEDAR-FIELD/VISlT-482l` не создаёт седьмую запись.
- Взаимодействие `M03+M07`: поздняя отмена меняет итоговое состояние уже перенесённого выезда `CEDAR-FIELD/VISIT-4821` и его дочерней подготовки `CEDAR-FIELD/CONF-4821`.
- Сохранённая независимость: `CEDAR-FIELD/PART-7742` связан с `CEDAR-FIELD/UNIT-PM-42` и не отменяется вместе с работой на `CEDAR-FIELD/UNIT-CH-17`.
- Похожая отдельная пара: `CEDAR-FIELD/VISIT-4821`/`CEDAR-FIELD/UNIT-CH-17` и `CEDAR-FIELD/VISIT-4827`/`CEDAR-FIELD/UNIT-CH-71` остаются разными, хотя находятся на одном сайте и имеют похожие номера.
- Значимое отсутствие: владелец `CEDAR-FIELD/ACT-4827` остаётся неизвестным. Carlos Peña нельзя автоматически назначить владельцем акта.

## Точные положительные проверки

1. Реестр содержит ровно 6 записей с идентификаторами, перечисленными выше.
2. `CEDAR-FIELD/VISIT-4821` имеет состояние `cancelled`, владельца Camila Ríos и последний срок до отмены `2026-09-05T10:00:00-05:00`.
3. `CEDAR-FIELD/CONF-4821` имеет состояние `cancelled`, владельца Lucía Fajardo и последний срок до отмены `2026-09-04T16:00:00-05:00`.
4. Отмена `CEDAR-FIELD/VISIT-4821` распространяется на зависимую запись `CEDAR-FIELD/CONF-4821`.
5. `CEDAR-FIELD/VISIT-4827` остаётся `scheduled` на `2026-09-07T09:30:00-05:00` с владельцем Carlos Peña.
6. `CEDAR-FIELD/ACT-4827` остаётся `open` до `2026-09-08T17:00:00-05:00`, а владелец отсутствует.
7. `CEDAR-FIELD/PART-7742` остаётся `ordered` для `CEDAR-FIELD/UNIT-PM-42` до `2026-09-08T15:00:00-05:00` с владельцем Juliana Mena.
8. `CEDAR-FIELD/PHOTO-4821` имеет конечного владельца Diego Orduz, а не Cami.
9. Относительный срок `mañana antes del mediodía` нормализуется в `2026-09-04T12:00:00-05:00`.
10. Свидетельства из четырёх файлов объединяются в одну `CEDAR-FIELD/VISIT-4821`.
11. Повреждённое `CEDAR-FIELD/VISlT-482l` сопоставляется существующему выезду и не создаёт дубликат.
12. `CEDAR-FIELD/VISIT-4821` и `CEDAR-FIELD/VISIT-4827` остаются двумя разными событиями.

## Точные отрицательные проверки

1. `N01`: строка `La batería del medidor quedó al 82 % después de una hora de carga.` не создаёт действие со сроком `82` и не меняет состояние ни одного выезда.
2. `N01`: строка `[03/09/2026 11:11] Lucía: El promedio de cierre de las rutas del miércoles fue 46 minutos.` не создаёт обязательство Lucía со сроком 46 минут.
3. `N03`: процитированный запрос `Could you reserve CEDAR-FIELD/PART-7310 for CEDAR-FIELD/UNIT-PM-24?` не возвращает старый заказ `CEDAR-FIELD/PART-7310` в конечный реестр.
4. `N03`: пересланное сообщение `[14/08/2026 07:12] Lucía: Cami, vuelve a CEDAR-FIELD/TORRE-ARCE a las 15:00 para recoger la pinza roja.` не создаёт новый выезд или действие в сентябре.
5. `N04`: версия `3.8.12` не становится датой, сроком или идентификатором новой записи.
6. `N04`: показание `4,75 mm/s durante once segundos` не становится датой `04/07`, суммой или сроком.
7. `N04`: `Tax reference: 19` и `Unit price: COP 684,200` не создают срок 19-го числа и не создают платёжное обязательство.
8. `N07`: календарные элементы `Café de cuadrilla` и `Almuerzo escalonado de bodega` не создают рабочие обязательства в конечном реестре.
9. `N07`: старый `Bloque de viaje de Cami` не сохраняет отменённый выезд в состоянии `scheduled` после заметки диспетчера.
10. `N08`: повреждённая строка `05/09|10:00|CEDAR-FIELD/VISlT-482l|CEDAR-FIELD/UNIT-CH-l7|Camila Rios|1h30` не создаёт отдельную сущность `VISlT-482l` и не меняет владельца.
11. `N08`: строка таблицы `CEDAR-FIELD/UNIT-CH-71|3,2l estable|40,9|019 OK` не создаёт дату, срок или новую задачу `019`.
12. Межсущностная граница: отмена работ на `CEDAR-FIELD/UNIT-CH-17` не отменяет `CEDAR-FIELD/PART-7742`, `CEDAR-FIELD/VISIT-4827` или `CEDAR-FIELD/ACT-4827`.

## Покрытие механизмов

- `M01`: извлечение событий, действий, владельцев, сроков и состояний.
- `M02`: выезд `CEDAR-FIELD/VISIT-4821` и отдельное подготовительное действие `CEDAR-FIELD/CONF-4821`.
- `M03`: сборка одной сущности по наряду, SMS, календарю и заметке диспетчера.
- `M04`: раздельные выезды 4821 и 4827, а также отдельный актив PM-42.
- `M05`: перенос выезда, подтверждения и загрузки фотографий.
- `M07`: отмена выезда и зависимого подтверждения.
- `M08`: алиас Cami, переназначение с Cami на Diego, явные владельцы и один отсутствующий владелец.
- `M09`: `dd/mm`, локальное время Bogotá и относительный срок `mañana`.
- `M13`: отсутствие владельца `CEDAR-FIELD/ACT-4827` без выдуманного назначения.

Классы естественного шума: `N01 N03 N04 N07 N08`.
