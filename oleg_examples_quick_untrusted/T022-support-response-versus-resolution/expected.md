# SLA ответа против срока решения

Опорное время: `2027-02-15T10:30:00Z`; локаль `en-GB`; пояс `UTC`.

## Требуемое состояние

1. Acknowledge customer по HD-77
   - владелец: Mina; конечный статус: завершена в 09:35
   - исходный срок: `2027-02-15T11:00:00Z`
   - цитата создания: `Acknowledge the customer by 11:00 today and resolve the export failure by 16 February 17:00.`
   - цитата завершения: `2027-02-15 09:35 ACK_SENT HD-77 Mina acknowledged the customer.`
2. Устранить export failure по HD-77
   - владелец: Mina; статус: открыта; срок: `2027-02-16T17:00:00Z`
   - источник: `input/ticket.eml`
   - цитата: `Mina owns HD-77. Acknowledge the customer by 11:00 today and resolve the export failure by 16 February 17:00.`

## Не создавать

- одну задачу с одним общим сроком;
- завершённый resolution из статуса `ACK_SENT`;
- отдельную задачу «confirm root cause».

