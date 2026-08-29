# Повтор с исключением и возобновлением

Опорное время: `2026-11-20T12:00:00Z`; локаль `en-GB`; пояс
`Europe/London`; рабочие дни — понедельник–пятница, 1 января — праздник.

## Требуемое состояние

1. Проводить backup recovery drill
   - владелец: infrastructure team lead; статус: повтор активен с исключением
   - правило: первый рабочий день месяца, результат до 17:00 local
   - декабрь 2026: пропущен; следующий запуск: `2027-01-04`
   - источник правила: `input/operations-policy.md`
   - цитата правила: `The infrastructure team runs the recovery drill on the first working day of every month.`
   - источник исключения: `input/holiday-exception.eml`
   - цитата исключения: `Skip the December recovery drill during the freeze.`

## Не создавать

- запуск 1 декабря 2026;
- запуск 1 января 2027;
- отдельную бессрочную задачу «resume».

