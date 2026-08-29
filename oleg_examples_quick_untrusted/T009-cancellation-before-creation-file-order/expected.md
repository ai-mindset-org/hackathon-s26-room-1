# Отмена раньше создания в файловом порядке

Опорное время: `2027-09-03T09:00:00+02:00`; локаль `en-GB`; пояс
`Europe/Paris`. Источники упорядочиваются по времени факта, а не по имени файла.

## Требуемое состояние

1. Cinder site inspection 10 сентября
   - тип: событие; конечный статус: отменено
   - создание: `input/02-original-calendar.ics`
   - цитата создания: `SUMMARY:Cinder site inspection`
   - отмена: `input/01-cancellation.eml`
   - цитата отмены: `The site inspection on 10 September is cancelled.`
2. Отправить site map за два дня
   - тип: производная задача; конечный статус: отменена
   - исходный срок: `2027-09-08`
   - цитата отмены: `Do not send the site map two days before it; that reminder is cancelled too.`

## Не создавать

- активное событие 10 сентября;
- активное напоминание 8 сентября;
- новую дату осмотра.

