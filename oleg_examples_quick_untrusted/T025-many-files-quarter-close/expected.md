# Масштаб: двенадцать файлов квартального закрытия

Опорное время: `2027-03-06T10:00:00Z`; локаль `en-GB`; пояс `UTC`.

## Требуемое состояние

1. Получить Northwind tax certificate и положить в close folder
   - владелец: Aya; конечный статус: завершена 4 марта
   - исходный срок: `2027-03-05`
   - цитата создания: `Aya, obtain the Northwind tax certificate by 5 March and place it in the close folder.`
   - цитата завершения: `Northwind certificate is in the close folder; my task is complete.`
2. Утвердить cold-chain waiver
   - владелец: Ben; статус: открыта
   - исходный срок: `2027-03-06`; конечный срок: `2027-03-07T12:00:00Z`
   - цитата обновления: `The cold-chain waiver stays with Ben, but its deadline moves to 7 March 12:00.`
3. Сверить invoice 4481
   - владелец: Finance Operations; статус: открыта; срок: `2027-03-08T17:00:00Z`
   - источник: `input/06-invoice.eml`
   - цитата: `Finance Operations must reconcile invoice 4481 by 8 March 17:00.`
4. Подготовить March cash forecast draft
   - владелец: Omar; статус: открыта; срок: `2027-03-09T11:00:00Z`
   - источник: `input/07-forecast-note.md`
   - цитата: `Omar owns the March cash forecast draft and will deliver it by 9 March 11:00.`
5. Quarter-close customs call 10 марта 14:00
   - тип: событие; конечный статус: отменено
   - цитата отмены: `Cancel the quarter-close customs call on 10 March.`
6. Отправить agenda к customs call
   - тип: производная задача; конечный статус: отменена
   - исходный срок: `2027-03-09T14:00:00Z`
   - цитата отмены: `The agenda is no longer needed, so cancel that reminder as well.`

## Не создавать

- дубли certificate из письма и status;
- Tess-задачу из 2025 года;
- обязательства из CSV metrics, суммы 31,448.20 или twelve weeks;
- активные customs call и agenda.

