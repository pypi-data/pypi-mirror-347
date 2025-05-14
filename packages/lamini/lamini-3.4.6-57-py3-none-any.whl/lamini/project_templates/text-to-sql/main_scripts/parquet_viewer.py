#!/usr/bin/env python3
"""
One‑file dark‑theme Parquet viewer for Lamini.
No external assets needed—CSS is embedded via index_string.
Works on Dash ≥2.0 (covers both react‑select v1 & v2 classnames).
"""

import os, argparse, json, math, collections.abc as cab
import pandas as pd, numpy as np
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, ALL


# ──── helpers ────────────────────────────────────────────────────────────────
def _stringify(v):
    """Hash‑safe, human‑readable surrogate for any Python object."""
    if isinstance(v, cab.Hashable):
        return v
    return json.dumps(v, sort_keys=True, default=str)


find_parquet_files = lambda folder: [
    os.path.join(folder, f)
    for f in sorted(os.listdir(folder))
    if f.lower().endswith(".parquet")
]
load_parquet = pd.read_parquet


# ──── main ───────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Run the Lamini Parquet viewer")
    p.add_argument(
        "folder",
        nargs="?",
        default="local-db",
        help="Folder with .parquet files (default: local-db)",
    )
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", default=8050, type=int)
    args = p.parse_args()

    files = find_parquet_files(args.folder)
    if not files:
        print(f"No .parquet files found in {args.folder!r}")
        return

    app = Dash(__name__)

    # ─── inline CSS injection ────────────────────────────────────────────────
    INLINE_CSS = r"""
    * { box-sizing: border-box; }  body { margin: 0; }

    /* header bar */
    .header {
      position: fixed; top: 0; left: 0; right: 0; height: 60px;
      background: #1b1b1b; color: #e91e63;
      display: flex; align-items: center; justify-content: center;
      font-size: 24px; font-weight: 600;
      border-bottom: 2px solid #e91e63; z-index: 1000;
    }

    /* body layout */
    .body { display: flex; height: calc(100vh - 60px); padding-top: 60px; }
    .sidebar {
      width: 300px; background: #141414; padding: 20px; overflow-y: auto;
    }
    .sidebar-title { color: #f5f5f5; margin-bottom: 8px; }

    /* ── React‑Select v1 support ───────────────────────────────────────── */
    .db-dropdown .Select-control,
    .filter-dropdown .Select-control {
      background-color: #2d2d2d !important;
    }
    .db-dropdown .Select-placeholder { color: #888 !important; }
    .filter-dropdown .Select-placeholder { color: #000 !important; }
    .db-dropdown .Select-value { color: #fff !important; }
    .filter-dropdown .Select-value { color: #000 !important; }
    /* v1 option list */
    .filter-dropdown .Select-menu-outer .Select-option,
    .filter-dropdown .Select-option {
      color: #000 !important;
    }

    /* ── React‑Select v2+ support (Dash 2.10+) ─────────────────────────── */
    .db-dropdown [class*="control"],
    .filter-dropdown [class*="control"] {
      background-color: #2d2d2d !important;
    }
    .db-dropdown [class*="placeholder"] { color: #888 !important; }
    .filter-dropdown [class*="placeholder"] { color: #000 !important; }
    .db-dropdown [class*="singleValue"] { color: #fff !important; }
    .filter-dropdown [class*="singleValue"],
    .filter-dropdown [class*="multiValueLabel"] {
      color: #000 !important;
    }
    /* v2 option list */
    .filter-dropdown [class*="option"] {
      color: #000 !important;
    }

    /* selected‑db label */
    .selected-db-label {
      color: #f5f5f5;
      margin-top: 10px;
      font-style: italic;
      font-size: 14px;
    }
    /* force focused / selected states to stay black */
    .filter-dropdown .Select-option,
    .filter-dropdown .Select-option.is-focused,
    .filter-dropdown .Select-option.is-selected,
    .filter-dropdown [class*="option--is-focused"],
    .filter-dropdown [class*="option--is-selected"] {
      color: #000 !important;
    }

    /* filters grid */
    .filters-box { margin-top:20px; color:#f5f5f5; }
    .filters-grid {
      display:grid;
      grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
      gap:12px;
    }
    .filter-label { color:#f5f5f5; margin-bottom:4px; display:block; }

    /* main table area */
    .main {
      flex:1; padding:20px; background:#121212; overflow:hidden;
    }
    """

    app.index_string = f"""
    <!DOCTYPE html>
    <html>
      <head>
        {{%metas%}}
        <title>Lamini Database Viewer</title>
        {{%favicon%}}
        {{%css%}}
        <style>{INLINE_CSS}</style>
      </head>
      <body>
        {{%app_entry%}}
        <footer>
          {{%config%}}
          {{%scripts%}}
          {{%renderer%}}
        </footer>
      </body>
    </html>
    """

    # ─── layout ───────────────────────────────────────────────────────────────
    app.layout = html.Div(
        [
            html.Div("Lamini Database Viewer", className="header"),
            html.Div(
                [
                    # ── sidebar ───────────────────────────────────────────────────────
                    html.Div(
                        [
                            html.H4("Database", className="sidebar-title"),
                            dcc.Dropdown(
                                id="file-dropdown",
                                options=[
                                    {"label": os.path.basename(f), "value": f}
                                    for f in files
                                ],
                                value=files[0],
                                clearable=False,
                                className="db-dropdown",
                                style={"width": "100%"},
                            ),
                            html.Div(
                                id="selected-db-label",
                                children=f"Selected: {os.path.basename(files[0])}",
                                className="selected-db-label",
                            ),
                            html.Details(
                                [
                                    html.Summary(
                                        "Filters (auto-detect)",
                                        style={"cursor": "pointer"},
                                    ),
                                    html.Div(
                                        id="filter-container", className="filters-grid"
                                    ),
                                ],
                                open=False,
                                className="filters-box",
                            ),
                        ],
                        className="sidebar",
                    ),
                    # ── main table ────────────────────────────────────────────────────
                    html.Div(
                        dash_table.DataTable(
                            id="data-table",
                            columns=[],
                            data=[],
                            page_current=0,
                            page_size=25,
                            page_action="custom",
                            style_table={"width": "100%", "overflowX": "auto"},
                            style_cell={
                                "backgroundColor": "#1e1e1e",
                                "color": "#f5f5f5",
                                "padding": "8px 16px",
                                "textAlign": "left",
                                "minWidth": "100px",
                            },
                            style_header={
                                "backgroundColor": "#2d2d2d",
                                "color": "#f5f5f5",
                                "borderBottom": "2px solid #e91e63",
                                "fontWeight": "bold",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "#252525",
                                },
                                {
                                    "if": {"state": "active"},
                                    "backgroundColor": "#333",
                                    "border": "1px solid #e91e63",
                                },
                            ],
                        ),
                        className="main",
                    ),
                ],
                className="body",
            ),
        ]
    )

    # ─── callbacks ───────────────────────────────────────────────────────────
    @app.callback(
        Output("selected-db-label", "children"), Input("file-dropdown", "value")
    )
    def show_selected_db(path):
        name = os.path.basename(path) if path else "None"
        return f"Selected: {name}"

    @app.callback(
        Output("filter-container", "children"),
        Input("file-dropdown", "value"),
    )
    def update_filters(selected_file):
        df = load_parquet(selected_file)
        widgets = []
        for col in df.columns:
            u = df[col].dropna().map(_stringify).unique()
            if not (0 < len(u) < 5) or any(len(str(x)) > 30 for x in u):
                continue
            opts = [{"label": str(x), "value": x} for x in sorted(u)]
            widgets.append(
                html.Div(
                    [
                        html.Label(col, className="filter-label"),
                        dcc.Dropdown(
                            id={"type": "filter-dropdown", "col": col},
                            options=opts,
                            placeholder=f"Filter {col}",
                            clearable=True,
                            className="filter-dropdown",
                            style={"width": "100%"},
                        ),
                    ],
                    className="filter-item",
                )
            )
        return widgets

    @app.callback(
        Output("data-table", "columns"),
        Output("data-table", "data"),
        Input("file-dropdown", "value"),
        Input("data-table", "page_current"),
        Input("data-table", "page_size"),
        Input({"type": "filter-dropdown", "col": ALL}, "value"),
        Input({"type": "filter-dropdown", "col": ALL}, "id"),
    )
    def update_table(selected_file, page_current, page_size, fvals, fids):
        df = load_parquet(selected_file)
        for val, fid in zip(fvals, fids):
            if val not in (None, ""):
                df = df[df[fid["col"]].map(_stringify) == val]

        start = page_current * page_size
        page = df.iloc[start : start + page_size].copy()
        page.insert(0, "Row", range(start + 1, start + 1 + len(page)))

        def _cell(v):
            if v in (None, pd.NaT) or (isinstance(v, float) and math.isnan(v)):
                return ""
            if isinstance(v, (str, bool, int)):
                return v
            if isinstance(v, (list, tuple, np.ndarray)):
                return "" if len(v) == 0 else json.dumps(list(v))
            return json.dumps(v)

        records = [{c: _cell(v) for c, v in r.items()} for r in page.to_dict("records")]
        cols = [{"name": c, "id": c} for c in page.columns]
        return cols, records

    @app.callback(Output("data-table", "page_current"), Input("file-dropdown", "value"))
    def reset_page(_):
        return 0

    url = f"http://{args.host}:{args.port}"
    print(f"\n📍  Viewer running — open at:\n{url}\n")
    app.run(host=args.host, port=args.port, debug=True)


if __name__ == "__main__":
    main()
