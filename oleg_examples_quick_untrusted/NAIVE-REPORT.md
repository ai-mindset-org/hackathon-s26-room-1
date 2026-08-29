# Штатный движок (без --llm) против корпуса gagebt

Сгенерировано `report_naive.py`. Грубая сверка по количеству,
не по смыслу — не замена LLM-судьи. Прогон без `--llm`: в окружении,
где строился отчёт, не было `ANTHROPIC_API_KEY`.

| id | сценарий | язык | ожидается 0? | required | извлечено (naive) | ок? |
|---|---|---|---:|---:|---:|:---:|
| T001 | US date and booked event | en-US | нет | 2 | 0 | ❌ |
| T002 | DST cross-timezone handoff | en | нет | 2 | 0 | ❌ |
| T003 | Newsletter with no obligations | en | да | 0 | 0 | ✅ |
| T004 | Quoted closed thread | en | да | 0 | 0 | ✅ |
| T005 | Same action for two projects | en | нет | 2 | 0 | ❌ |
| T006 | Paraphrase duplicate completed | en | нет | 1 | 0 | ❌ |
| T007 | Disputed owner | en | нет | 1 | 0 | ❌ |
| T008 | Rejected hypothesis | en | да | 0 | 0 | ✅ |
| T009 | Cancellation before creation in file order | en | нет | 2 | 0 | ❌ |
| T010 | Reopen after completion | en | нет | 1 | 0 | ❌ |
| T011 | Reassign and reschedule | en | нет | 1 | 0 | ❌ |
| T012 | Recurring skip and next date | en | нет | 1 | 0 | ❌ |
| T013 | Mixed-language deadline | ru plus en plus es | нет | 2 | 0 | ❌ |
| T014 | Noisy OCR table | en | нет | 2 | 0 | ❌ |
| T015 | Boilerplate signature | en | нет | 1 | 0 | ❌ |
| T016 | Truncated fragment | en | да | 0 | 0 | ✅ |
| T017 | External dependency and group owner | en | нет | 2 | 0 | ❌ |
| T018 | Event versus preparation deadlines | en | нет | 3 | 0 | ❌ |
| T019 | Civic permit and hearing | en | нет | 2 | 0 | ❌ |
| T020 | Healthcare administration | en | нет | 3 | 0 | ❌ |
| T021 | Field service dependency | en | нет | 2 | 0 | ❌ |
| T022 | Support response versus resolution | en | нет | 2 | 0 | ❌ |
| T023 | Travel cancellation and replan | en | нет | 2 | 0 | ❌ |
| T024 | Split umbrella task | en | нет | 3 | 0 | ❌ |
| T025 | Many-file quarter close | en | нет | 6 | 1 | ✅ |
| T026 | Long distributed launch thread | en | нет | 6 | 1 | ✅ |

**Итого: 6 из 26** прошли грубую сверку по количеству (0 там, где ожидается 0; хотя бы 1 там, где ожидается непустой результат).

## Что это значит

Корпус целиком на английском/смешанных языках (`languages` в `index.csv`), а `extract/naive.py` — правила целиком на русском (маркеры долженствования, названия месяцев, разбор дат). Провал здесь ожидаем и задокументирован в README-tool.md — правила заточены под стиль `examples/`, для остального нужен `--llm`.

Не проверено: прогон с `--llm` против этого же корпуса — нужен `ANTHROPIC_API_KEY`, которого не было в окружении, где готовился отчёт. Следующий шаг для честной цифры — прогнать этот же скрипт с ключом и добавить колонку.
