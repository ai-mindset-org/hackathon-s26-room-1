# Отмена поездки и новое действие

Опорное время: `2027-06-01T10:15:00+02:00`; локаль `en-GB`; пояс
`Europe/Berlin`.

## Требуемое состояние

1. Flight SP-204 4 июня 07:10
   - тип: событие; конечный статус: отменено
   - цитата отмены: `Flight SP-204 is cancelled. Do not travel on that booking.`
2. Выбрать replacement flight
   - владелец: Rina; статус: открыта; срок: `2027-06-01T18:00:00+02:00`
   - источник: `input/change-chat.txt`
   - цитата: `Rina, choose a replacement flight by today 18:00.`

## Не создавать

- активный вылет SP-204;
- отмену Hotel Cedar: есть прямой запрет;
- новую дату вылета до выбора replacement.

