import sqlite3, sys
from indexer import scan_dir, search, find_calls_to, find_unused_exports
from graph_builder import build_module_graph, metrics
from report import export_xlsx, render_graph

def main(dump_dir):
    conn = sqlite3.connect(':memory:')
    conn.executescript(open('db/schema.sql').read())

    print("=== Индексация ===")
    scan_dir(conn, dump_dir)

    print("\n=== Метрики графа ===")
    g = build_module_graph(conn)
    m = metrics(g)
    print(f"Модулей: {m['nodes']}, связей: {m['edges']}")
    print(f"Циклов: {len(m['cycles'])}")
    print(f"Сирот: {len(m['orphans'])}")
    print(f"Топ-связанные: {m['top']}")

    print("\n=== Unused exports ===")
    unused = find_unused_exports(conn)
    print(f"Найдено: {len(unused)}")
    for u in unused[:10]:
        print(f"  {u}")

    print("\n=== Отчёты ===")
    export_xlsx(conn)
    render_graph(g)
    print("report.xlsx, modules.html")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'dump/')
