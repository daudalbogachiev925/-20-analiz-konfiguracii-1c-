# Архитектура

Слои:
1. indexer.py — читает BSL, пишет в SQLite (objects, modules, proc_defs, calls)
2. FTS5 — полнотекстовый поиск
3. graph_builder.py — граф модулей
4. report.py — Excel + Plotly HTML

Запросы:
- Найти процедуру: search('Провести')
- Кто вызывает: find_calls_to('Провести')
- Мёртвый код: find_unused_exports()
