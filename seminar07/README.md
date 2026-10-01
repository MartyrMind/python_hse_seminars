# Семинар 7. Исключения, предупреждения и контекстные менеджеры

В этом семинаре вам предстоит разбирать складские записи, загружать страницы из
основного и резервного источников, строить дерево исключений, предупреждать об
устаревшем формате данных и записывать отчёт через временный файл. Для решения
понадобятся `try`/`except`, цепочки исключений и traceback, модуль `warnings`
и собственный контекстный менеджер.

Задачи независимы: каждую можно решать отдельно.

## Задачи

1. **5/10 — [`parse_stock_row`](tasks/task01_parse_stock_row/README.md):** разобрать
   одну запись и обработать ожидаемую ошибку преобразования.
2. **6/10 — [`load_pages`](tasks/task02_load_pages/README.md):** получить страницы
   по курсору, переключиться на резерв и сохранить только полный результат.
3. **7/10 — [`build_exception_tree`](tasks/task03_build_exception_tree/README.md):**
   раскрыть группы, цепочки исключений и traceback в дереве.
4. **7/10 — [`normalize_rows`](tasks/task04_normalize_rows/README.md):**
   собрать предупреждения об устаревших записях и включить строгий режим.
5. **9/10 — [`AtomicExport`](tasks/task05_atomic_export/README.md):**
   публиковать готовый отчёт, учитывать бюджет ошибок и сохранять двойной сбой.

## Проверка

```bash
uv run pytest seminar07/tasks/task01_parse_stock_row -v
uv run pytest seminar07/tasks/task02_load_pages -v
uv run pytest seminar07/tasks/task03_build_exception_tree -v
uv run pytest seminar07/tasks/task04_normalize_rows -v
uv run pytest seminar07/tasks/task05_atomic_export -v
```

Пока задачи не решены, тесты завершаются с `NotImplementedError`. Реализуйте
функции в файлах задач и запустите тесты соответствующего каталога.
