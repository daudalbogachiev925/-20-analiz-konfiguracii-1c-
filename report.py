import pandas as pd
import plotly.graph_objects as go
import networkx as nx

def export_xlsx(conn, path='report.xlsx'):
    df_modules = pd.read_sql("SELECT id, object_uuid, module_kind, lines FROM modules", conn)
    df_procs = pd.read_sql("SELECT module_id, name, is_export FROM proc_defs", conn)
    df_calls = pd.read_sql("SELECT caller_module, callee_name, line_no FROM calls", conn)
    with pd.ExcelWriter(path) as w:
        df_modules.to_excel(w, sheet_name='modules', index=False)
        df_procs.to_excel(w, sheet_name='procedures', index=False)
        df_calls.to_excel(w, sheet_name='calls', index=False)
    return path

def render_graph(g, out_html='modules.html'):
    pos = nx.spring_layout(g, seed=42)
    edge_x, edge_y = [], []
    for a, b in g.edges:
        x0, y0 = pos[a]; x1, y1 = pos[b]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines',
                            line=dict(width=0.6, color='#888'))
    node_x = [pos[n][0] for n in g.nodes]
    node_y = [pos[n][1] for n in g.nodes]
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text',
                            text=[str(n) for n in g.nodes],
                            textposition='top center',
                            marker=dict(size=12, color='#2e86de'))
    fig = go.Figure([edge_trace, node_trace],
                    layout=go.Layout(showlegend=False, hovermode='closest'))
    fig.write_html(out_html)
    return out_html
