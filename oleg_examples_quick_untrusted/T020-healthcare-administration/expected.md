# Административные задачи клиники

Опорное время: `2027-06-01T09:00:00+04:00`; локаль `en-GB`; пояс
`Asia/Tbilisi`. Данные полностью синтетические.

## Требуемое состояние

1. Запросить prior authorization
   - владелец: Benefits team; статус: открыта; срок: `2027-06-03`
   - источник: `input/clinic-office.txt`
   - цитата: `Benefits team must request prior authorization by 3 June.`
2. Забронировать Georgian interpreter
   - владелец: Zoë; статус: открыта; срок: `2027-06-04T12:00:00+04:00`
   - источник: `input/clinic-office.txt`
   - цитата: `Zoë, book the Georgian interpreter by 4 June 12:00.`
3. Review appointment
   - тип: событие; статус: запланировано; время: `2027-06-07T09:30:00+04:00`
   - источник: `input/clinic-office.txt`
   - цитата: `The review appointment is already scheduled for 7 June 09:30.`

## Не создавать

- медицинский диагноз или действие по лечению;
- задачу «запланировать appointment»;
- владельца Zoë для prior authorization.

