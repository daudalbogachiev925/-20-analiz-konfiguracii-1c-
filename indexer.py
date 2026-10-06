import sqlite3, re
from pathlib import Path

PROC_RE = re.compile(r'(Процедура|Функция)\s+(\w+)\s*\(([^)]*)\)', re.IGNORECASE)
CALL_RE = re.compile(r'\b([А-Яа-яA-Za-z_][\w]*)\s*\(')

def index_bsl(conn, module_id, object_name, code):
    conn.execute("INSERT INTO fts_bsl (module_id, object_name, body) VALUES (?,?,?)",
                 (module_id, object_name, code))
    for m in PROC_RE.finditer(code):
        kind, name, params = m.groups()
        is_export = 1 if 'Экспорт' in params or 'Export' in params else 0
        conn.execute("INSERT INTO proc_defs (module_id, name, is_export) VALUES (?,?,?)",
                     (module_id, name, is_export))
    for line_no, line in enumerate(code.splitlines(), 1):
        if line.strip().startswith('//'):
            continue
        for m in CALL_RE.finditer(line):
            conn.execute("""INSERT INTO calls (caller_module, callee_name, line_no)
                            VALUES (?,?,?)""",
                         (module_id, m.group(1), line_no))
    conn.commit()

def scan_dir(conn, root: str):
    for p in Path(root).rglob('*.bsl'):
        code = p.read_text(encoding='utf-8')
        conn.execute("""INSERT INTO modules (object_uuid, module_kind, code, lines)
                        VALUES (?,?,?,?)""",
                     (p.stem, p.parent.name, code, len(code.splitlines())))
        mid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        index_bsl(conn, mid, p.stem, code)
        print(f"Проиндексирован: {p}")

def search(conn, query: str):
    cur = conn.execute("""SELECT object_name, snippet(fts_bsl, 2, '<b>', '</b>', '...', 20)
                          FROM fts_bsl WHERE body MATCH ? LIMIT 20""", (query,))
    return cur.fetchall()

def find_calls_to(conn, name: str):
    cur = conn.execute("""SELECT m.object_uuid, c.line_no
                          FROM calls c JOIN modules m ON m.id = c.caller_module
                          WHERE c.callee_name = ?""", (name,))
    return cur.fetchall()

def find_unused_exports(conn):
    cur = conn.execute("""
        SELECT pd.module_id, pd.name FROM proc_defs pd
        WHERE pd.is_export = 1
          AND NOT EXISTS (SELECT 1 FROM calls c WHERE c.callee_name = pd.name)
    """)
    return cur.fetchall()
