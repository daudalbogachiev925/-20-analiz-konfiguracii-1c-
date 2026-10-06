CREATE TABLE objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type TEXT,
    uuid TEXT,
    parent_uuid TEXT
);

CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_uuid TEXT,
    module_kind TEXT,
    code TEXT,
    lines INTEGER
);

CREATE VIRTUAL TABLE fts_bsl USING fts5(
    module_id UNINDEXED,
    object_name,
    body
);

CREATE TABLE calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caller_module INTEGER,
    caller_proc TEXT,
    callee_name TEXT,
    line_no INTEGER
);

CREATE TABLE proc_defs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER,
    name TEXT,
    is_export INTEGER
);

CREATE INDEX idx_calls_callee ON calls(callee_name);
CREATE INDEX idx_proc_name ON proc_defs(name);
