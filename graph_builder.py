import networkx as nx

def build_module_graph(conn):
    g = nx.DiGraph()
    rows = conn.execute("""
        SELECT m1.id, m2.id
        FROM calls c
        JOIN modules m1 ON m1.id = c.caller_module
        JOIN proc_defs pd ON pd.name = c.callee_name
        JOIN modules m2 ON m2.id = pd.module_id
        WHERE m1.id != m2.id
    """).fetchall()
    for a, b in rows:
        g.add_edge(a, b)
    return g

def metrics(g):
    return {
        'nodes': g.number_of_nodes(),
        'edges': g.number_of_edges(),
        'cycles': list(nx.simple_cycles(g)),
        'orphans': [n for n in g.nodes if g.in_degree(n) == 0],
        'top': sorted(g.degree, key=lambda x: -x[1])[:10]
    }
