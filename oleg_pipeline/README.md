# `oleg_pipeline`

`oleg_pipeline` запускает любой совместимый движок на любом каталоге примеров и делает единый смысловой отчёт.

## Быстрый запуск

Из корня репозитория. Первая команда работает на этой ветке без внешних зависимостей (встроенный fake engine):

```powershell
python -m oleg_pipeline run `
  --examples examples `
  --engine "python oleg_pipeline/fake_engine.py run --input {input} --registry {registry}" `
  --out oleg_pipeline/out/fake
```

Штатный движок комнаты (`cli.py`) через адаптер `room_engine.py`. После слияния в main `cli.py` лежит в корне репозитория, и `--room-root` не нужен; до слияния укажите `--room-root <путь к checkout с cli.py>`:

```powershell
python -m oleg_pipeline run `
  --examples examples `
  --engine "python oleg_pipeline/room_engine.py --input {input} --registry {registry}" `
  --out oleg_pipeline/out/room
```

`oleg_engine` (нужна папка движка в репозитории после слияния или на `PYTHONPATH`):

```powershell
python -m oleg_pipeline run `
  --examples examples `
  --engine "python -m oleg_engine run --input {input} --registry {registry}" `
  --out oleg_pipeline/out
```

Команда движка обязана содержать `{input}` и `{registry}`. Если она содержит `{now}`, pipeline берёт дату из строки `Опорное время`, `Reference time` или `Reference clock` в `expected.md`. Если такой строки нет, используется текущая локальная дата.

Движок должен завершиться с кодом 0 и создать `registry.json` и `registry.md` рядом. Pipeline не зависит от внутренней реализации движка.

**Любые данные.** Подходит любая папка, чьи подпапки содержат `input/` и `expected.md`: укажите её через `--examples <папка>`.
Подходит любой движок: подставьте его команду в шаблон `--engine` с `{input}` и `{registry}`.

## Правило цепочки

Если `expected.md` содержит текст вида `ПОВЕРХ реестра из примера 01`, pipeline сначала выполняет пример 01. Затем он копирует состояние реестра в каталог дочернего примера и запускает дочерний пример поверх этой копии. Так итог дочернего прогона не меняет уже оценённый артефакт родителя.

Независимые примеры выполняются параллельно. Зависимый пример ждёт родителя.

## Судья

По умолчанию используется `codex`: `gpt-5.6-sol` с `high` reasoning и строгой JSON-схемой. При ошибке или неверном JSON выполняется одна повторная попытка. После двух ошибок pipeline пробует `claude -p --model opus` с пустой MCP-конфигурацией и без унаследованных `ANTHROPIC_API_KEY` и `ANTHROPIC_AUTH_TOKEN`.

Судья получает `expected.md`, итоговый `registry.md` и все файлы `input/`. Он проверяет факты по смыслу, точность цитат в названных источниках, отрицательные требования `Не создавать` и пустой результат для нулевых сценариев.

```powershell
# Только Claude
python -m oleg_pipeline run ... --judge claude

# Без LLM: выполнить движок и напечатать реестры
python -m oleg_pipeline run ... --judge none
```

В режиме `--judge none` смысловой счёт имеет вид `прошло 0 из 0`, а отдельный счёт показывает успешные запуски движка. Поэтому запуск движка не выглядит как смысловой PASS. Ошибка движка всё равно даёт ненулевой код выхода.

## Флаги

- `--examples <dir>`: обязательный каталог сценариев. Каждый сценарий содержит `input/` и `expected.md`.
- `--engine <template>`: обязательная команда движка.
- `--judge codex|claude|none`: судья; по умолчанию `codex`.
- `--out <dir>`: реестры и `report.md`; по умолчанию `oleg_pipeline/out`.
- `--jobs N`: параллельные независимые сценарии; по умолчанию 4.
- `--only <substring>`: выбрать сценарии по подстроке имени. Нужный родитель цепочки запускается автоматически.

Переменные `OLEG_PIPELINE_ENGINE_TIMEOUT` и `OLEG_PIPELINE_JUDGE_TIMEOUT` задают тайм-ауты в секундах. Обе по умолчанию равны 600.

## Встроенный fake engine

Fake engine проверяет полный путь без зависимости от рабочего движка:

```powershell
python -m oleg_pipeline run `
  --examples examples `
  --engine "python oleg_pipeline/fake_engine.py run --input {input} --registry {registry}" `
  --out oleg_pipeline/out/fake
```

Для отрицательной проверки добавьте `--wrong-booking-deadline` в шаблон движка. Тогда пример 01 получает неверный срок бронирования 25.09 и должен завершиться с FAIL.

## Выход

Pipeline всегда пытается записать одну строку отчёта на каждый выбранный сценарий. Ошибка одного движка не останавливает остальные. В конце stdout содержит `прошло N из M` и путь к `<out>/report.md`. Код выхода 0 означает, что все выбранные сценарии прошли; код 1 означает хотя бы один FAIL.

## Ограничения

- Сравнение по смыслу требует работающего Codex или Claude, кроме режима `--judge none`.
- Формат цепочки сейчас распознаёт явную русскую фразу `поверх реестра из примера NN`.
- Pipeline проверяет текстовые входы. Он не извлекает текст из бинарных PDF или изображений.
- Ограничение параллелизма относится к сценариям, а не к внутренней работе движка или судьи.
