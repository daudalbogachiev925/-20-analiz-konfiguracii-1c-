import sqlite3
from indexer import index_bsl, search, find_calls_to

def test_index_and_search():
    conn = sqlite3.connect(':memory:')
    conn.executescript(open('db/schema.sql').read())
    conn.execute("INSERT INTO modules (object_uuid, module_kind, code, lines) VALUES ('T','Common','',0)")
    mid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    index_bsl(conn, mid, 'TestModule', 'Процедура МояПроц()\nКонецПроцедуры')
    res = search(conn, 'МояПроц')
    assert len(res) > 0
