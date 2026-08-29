# Headless UI-тесты (Playwright)

Нужен пакет `playwright` (`pip install playwright`) и браузер Chromium (`playwright install chromium`).
Каждый скрипт сам поднимает `python -m oleg_web` на свободном порту и пишет только во временный реестр.
Запуск из корня репозитория: `python oleg_web/tests/test_ui_headless.py` — реестр, прогоны движка, правки, ошибки, сортировка.
И `python oleg_web/tests/test_ui_presets.py` — пресеты команды движка и скачивание registry.md / registry.json.
Порт можно задать явно: `python oleg_web/tests/test_ui_headless.py 8795` или через `OLEG_WEB_TEST_PORT`; код возврата 0 — все проверки прошли.
