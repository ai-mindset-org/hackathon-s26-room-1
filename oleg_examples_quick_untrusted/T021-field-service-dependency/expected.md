# Полевые работы и зависимость от запчасти

Опорное время: `2027-09-14T07:35:00+04:00`; локаль `en-GB`; пояс
`Asia/Tbilisi`.

## Требуемое состояние

1. Забрать и доставить spare S-44 на site K-9
   - владелец: Jae; статус: открыта; начало не раньше `2027-09-14T08:00:00+04:00`
   - источник: `input/dispatch-chat.txt`
   - цитата: `Jae, collect the S-44 spare from East Depot when it opens at 08:00 and deliver it to site K-9.`
2. Заменить sensor S-44
   - владелец: Niko; статус: открыта; срок: `2027-09-14T14:00:00+04:00`
   - зависимость: доставка spare
   - источник: `input/field-log.txt`
   - цитата: `2027-09-14 07:25 TECH=Niko Replace sensor S-44 before 14:00 after the spare arrives.`

## Не создавать

- задачу из truck ETA 09:10;
- обязательство по температуре 17C;
- владельца Jae для замены sensor.

