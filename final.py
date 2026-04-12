import streamlit as st
import csv
import os
import json
import base64

# ─── Import classes from your existing screener.py ───────────────────────────
from screener import Stock, Data_fetcher, Screener, download_data, merge_delivery_data, download_bhavcopies, run_screener

# ─── Directory Initialization ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
for folder in ["NAMES", "data", "icons"]:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pro-Trader Terminal v1.2",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS (Concept 3: Pro-Trader Terminal - Industrial & Sharp) ────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .mono { font-family: 'JetBrains Mono', monospace !important; }

    .stApp { 
        background-color: #0d1117;
        color: #c9d1d9;
    }

    .main-header {
        background: #161b22;
        padding: 1.25rem 1.75rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        border-left: 6px solid #2dd4bf;
    }
    .main-header h1 { color: #f0f6fc; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
    .main-header p { color: #8b949e; font-size: 0.82rem; margin-top: 6px; font-weight: 500; }

    .stat-card {
        background: #161b22; border-radius: 4px; padding: 1.4rem 1.2rem;
        text-align: left; border: 1px solid #30363d; height: 100%;
    }
    .stat-card-blue { border-left: 4px solid #58a6ff; }
    .stat-card-green { border-left: 4px solid #2dd4bf; }
    .stat-card-purple { border-left: 4px solid #fbbf24; }
    .stat-number { font-size: 2rem; font-weight: 700; color: #f0f6fc; font-family: 'JetBrains Mono', monospace; }
    .stat-label { color: #8b949e; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }

    .tag-breakout {
        background: #0d1117; color: #2dd4bf; padding: 3px 10px; border-radius: 2px;
        font-weight: 700; font-size: 0.68rem; display: inline-block; border: 1px solid #2dd4bf; 
        font-family: 'JetBrains Mono', monospace; text-transform: uppercase;
    }

    .clean-table {
        width: 100%; border-collapse: collapse; border: 1px solid #30363d; background: #0d1117;
    }
    .clean-table thead th {
        background: #161b22; color: #8b949e; padding: 14px; font-weight: 700;
        font-size: 0.72rem; text-transform: uppercase; font-family: 'JetBrains Mono', monospace;
        text-align: left; border-bottom: 2px solid #30363d; border-right: 1px solid #30363d;
    }
    .clean-table tbody tr { background: #0d1117; }
    .clean-table tbody tr:hover { background: #1c2128 !important; }
    .clean-table tbody td { 
        padding: 12px; font-size: 0.88rem; color: #c9d1d9; font-family: 'JetBrains Mono', monospace;
        border-bottom: 1px solid #30363d; border-right: 1px solid #30363d;
    }
    .green { color: #39d353; font-weight: 700; }
    .red { color: #f85149; font-weight: 700; }
    .bold { color: #f0f6fc; font-weight: 700; }
    .muted { color: #484f58; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Target the header to be transparent while keeping buttons */
    header { background-color: rgba(0,0,0,0) !important; border: none !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; border: none !important; }

    /* Make sidebar toggle/chevron buttons brighter and visible */
    [data-testid="stHeader"] button, [data-testid="stSidebar"] button {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        margin: 5px !important;
        border-radius: 8px !important;
    }
    [data-testid="stHeader"] button svg, [data-testid="stSidebar"] button svg {
        fill: #ffffff !important;
    }

    [data-testid="stSidebar"] { background: #010409 !important; border-right: 1px solid #30363d; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f0f6fc !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Ensure Streamlit Icons (which use spans) keep their Material Icon font */
    [data-testid="stSidebar"] [data-testid="expanded_sidebar_window"] span {
        color: #f0f6fc !important;
    }
    
    /* Force Hide the icon labels if they show up as text */
    [data-testid="stSidebar"] .material-icons-sharp, 
    [data-testid="stSidebar"] .material-icons-outlined,
    [data-testid="stSidebar"] .material-icons {
        font-family: "Material Icons", "Material Icons Sharp", "Material Icons Outlined" !important;
    }
    .sidebar-logo { font-size: 1.3rem; font-weight: 900; color: #2dd4bf; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #30363d; padding: 1.5rem 1rem; margin-bottom: 1.5rem; }

    .stTabs [data-baseweb="tab"] { color: #8b949e; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }
    .stTabs [aria-selected="true"] { color: #2dd4bf; border-bottom-color: #2dd4bf !important; font-weight: 700; }

    .stButton > button {
        background-color: #21262d !important; border: 1px solid #30363d !important;
        border-radius: 4px !important; color: #c9d1d9 !important; font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important; padding: 0.5rem 1rem !important;
        text-transform: uppercase; letter-spacing: 1px; font-size: 0.75rem !important;
    }
    .stButton > button:hover {
        background-color: #30363d !important; border-color: #8b949e !important; color: #f0f6fc !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; color: #f0f6fc !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    hr { border-color: #30363d !important; }

    /* Category List Styles */
    .scan-category-row {
        background: #161b22; border: 1px solid #30363d; padding: 1rem;
        border-radius: 4px; margin-bottom: 0.6rem; transition: all 0.2s; cursor: pointer;
        display: flex; align-items: center; justify-content: space-between;
    }
    .scan-category-row:hover { background: #1c2128; border-color: #58a6ff; }
    .scan-cat-left { display: flex; align-items: center; gap: 1rem; }
    .scan-cat-title { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #f0f6fc; font-size: 0.95rem; }
    .scan-cat-desc { font-size: 0.75rem; color: #8b949e; }
    .scan-cat-count { font-size: 0.78rem; color: #2dd4bf; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
    .scan-cat-icon { width: 40px; height: 40px; background: #0d1117; border-radius: 4px; display: flex; align-items: center; justify-content: center; border: 1px solid #30363d; }

    /* Combo Card */
    .combo-card {
        background: #161b22; border: 1px solid #30363d; padding: 1.25rem;
        border-radius: 4px; margin-bottom: 1rem;
    }
    .combo-chip {
        display: inline-flex; align-items: center; background: #0d1117; color: #58a6ff;
        font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 2px;
        margin: 4px; border: 1px solid #30363d; font-family: 'JetBrains Mono', monospace;
    }

    /* Terminal-style Insight Icons Fix */
    .insight-tag {
        background: #ced4da;
        padding: 2px 4px;
        border-radius: 2px;
        display: inline-flex;
        align-items: center;
        margin-right: 4px;
        border: 1px solid #adb5bd;
    }
    .insight-tag img {
        filter: brightness(0.9);
    }
</style>
""", unsafe_allow_html=True)


# ─── Helper functions ────────────────────────────────────────────────────────

def get_available_sectors():
    sectors = []
    names_dir = os.path.join(os.path.dirname(__file__), "NAMES")
    if os.path.exists(names_dir):
        for f in os.listdir(names_dir):
            if f.endswith(".csv"): sectors.append(f.replace(".csv", ""))
    return sorted(sectors)

def load_symbols(sector):
    symbols = []
    filepath = os.path.join(os.path.dirname(__file__), "NAMES", f"{sector}.csv")
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row: symbols.append(row[0])
    return symbols


# ─── Scan / Filter Definitions ──────────────────────────────────────────────

def _breakout_scans(period, badge):
    return {
        "title": f"{badge} RANGE ENGINE",
        "badge": badge,
        "scans": [
            (f"{period}_breakout",   f"{badge} Breakout",  f"Price >= {badge} High",    f"{period} Breakout"),
            (f"{period}_near_high",  f"Near {badge} High", f"Threshold < 5%",           f"Near {period} High"),
            (f"{period}_near_low",   f"Near {badge} Low",  f"Threshold < 5%",           f"Near {period} Low"),
            (f"{period}_breakdown",  f"Below {badge} Low", f"Price <= {badge} Low",     f"{period} Breakdown"),
        ],
    }

PRICE_SUBCATEGORIES = {
    "1y": _breakout_scans("1Y", "1Y"),
    "2y": _breakout_scans("2Y", "2Y"),
    "5y": _breakout_scans("5Y", "5Y"),
    "at": _breakout_scans("AT", "AT"),
    "rs": {
        "title": "RELATIVE STRENGTH ENGINE",
        "badge": "RS",
        "scans": [
            ("rs_55w",   "55W ALPHA vs NIFTY", "55W_RET > NIF50_RET", "RS 55W Outperformer"),
            ("rs_123d",  "123D ALPHA vs NIFTY", "123D_RET > NIF50_RET", "RS 123D Outperformer"),
            ("rs_55w_under", "55W BETA vs NIFTY", "55W_RET < NIF50_RET", "RS 55W Underperformer"),
            ("rs_123d_under", "123D BETA vs NIFTY", "123D_RET < NIF50_RET", "RS 123D Underperformer"),
        ],
    },
}

SCAN_CATEGORIES = {
    "price": {
        "title": "PRICE_ENGINE", "desc": "Technical level monitoring.", "icon": "📊", "css_class": "price",
        "subcategories": PRICE_SUBCATEGORIES, "scans": [],
    },
    "volume": {
        "title": "VOL_DELIVERY", "desc": "Volume & Delivery analysis.", "icon": "⚡", "css_class": "volume",
        "scans": [
            ("deliv_pct_daily",   "DELIVERY_% (D)", "Today > 1Y Avg", "Delivery % Higher Annual"),
            ("deliv_vol_daily",   "DELIVERY_VOL (D)", "Today > 1Y Avg", "Delivery Vol Higher Annual"),
            ("deliv_pct_weekly",  "DELIVERY_% (W)", "5D Avg > 1Y Avg", "Weekly Delivery % > Avg"),
            ("deliv_vol_weekly",  "DELIVERY_VOL (W)", "5D Total > 1Y Avg", "Weekly Delivery Vol > Avg"),
            ("deliv_pct_monthly", "DELIVERY_% (M)", "21D Avg > 1Y Avg", "Monthly Delivery % > Avg"),
            ("deliv_vol_monthly", "DELIVERY_VOL (M)", "21D Total > 1Y Avg", "Monthly Delivery Vol > Avg"),
            ("tvol_daily",        "TRADE_VOL (D)", "Today > 1Y Avg", "Volume Higher Annual"),
            ("tvol_weekly",       "TRADE_VOL (W)", "5D Total > 1Y Avg", "Weekly Volume > Avg"),
            ("tvol_monthly",      "TRADE_VOL (M)", "21D Total > 1Y Avg", "Monthly Volume > Avg"),
        ],
    },
}

ALL_SCANS = {}
for cat_key, cat in SCAN_CATEGORIES.items():
    for scan in cat.get("scans", []):
        ALL_SCANS[scan[0]] = {"key": scan[0], "label": scan[1], "desc": scan[2], "data_key": scan[3], "category": cat_key}
    for sub_key, sub in cat.get("subcategories", {}).items():
        for scan in sub["scans"]:
            ALL_SCANS[scan[0]] = {"key": scan[0], "label": scan[1], "desc": scan[2], "data_key": scan[3], "category": cat_key, "subcategory": sub_key}

def _get_icon_b64(data_key):
    for ext, mime in [(".svg", "image/svg+xml"), (".png", "image/png")]:
        safe_name = data_key.replace(":", "").replace("/", "").replace("%", "pct").replace(">", "gt").replace(" ", "_")
        icon_path = os.path.join(os.path.dirname(__file__), "icons", f"{safe_name}{ext}")
        if os.path.exists(icon_path):
            with open(icon_path, "rb") as f: return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return None

def _count_all_scans_in_category(cat):
    count = len(cat.get("scans", []))
    for sub in cat.get("subcategories", {}).values(): count += len(sub["scans"])
    return count

COMBOS_FILE = os.path.join(os.path.dirname(__file__), "saved_combos.json")
def load_saved_combos():
    if os.path.exists(COMBOS_FILE):
        try:
            with open(COMBOS_FILE, "r") as f: return json.load(f)
        except: return []
    return []
def save_combos(combos):
    with open(COMBOS_FILE, "w") as f: json.dump(combos, f, indent=2)

if "page" not in st.session_state: st.session_state.page = "scans"
if "active_scan" not in st.session_state: st.session_state.active_scan = None
if "active_combo" not in st.session_state: st.session_state.active_combo = None
if "creating_combo" not in st.session_state: st.session_state.creating_combo = False

with st.sidebar:
    st.markdown('<div class="sidebar-logo">TERMINAL_v1.2</div>', unsafe_allow_html=True)
    if st.button("SYS_SCANS", use_container_width=True): st.session_state.page = "scans"; st.session_state.active_scan = None; st.rerun()
    if st.button("SYS_COMBOS", use_container_width=True): st.session_state.page = "combos"; st.session_state.active_scan = None; st.session_state.active_combo = None; st.rerun()
    st.markdown("---")
    st.markdown("### DATA_OPS")
    sectors = get_available_sectors()
    selected_sector = st.selectbox("REGION_SELECT", sectors, index=0)
    st.markdown("---")
    if st.button("DOWNLOAD_FRESH", use_container_width=True):
        symbols_to_download = load_symbols(selected_sector)
        if symbols_to_download:
            p = st.progress(0); s = st.empty()
            def up(sym, i, tot): s.text(f"FETCHING {sym}..."); p.progress((i+1)/tot)
            download_data(symbols_to_download, os.path.join(BASE_DIR, "data"), 10, up)
            st.rerun()
    if st.button("DOWNLOAD_BHAV", use_container_width=True):
        with st.spinner("FETCHING..."): download_bhavcopies(365); st.rerun()
    if st.button("MERGE_DELIVERY", use_container_width=True):
        with st.spinner("MERGING..."): merge_delivery_data(os.path.join(BASE_DIR, "data"), os.path.join(BASE_DIR, "delivery_data")); st.rerun()

symbols = load_symbols(selected_sector)
data_dir = os.path.join(os.path.dirname(__file__), "data")
results = []
if symbols and os.path.exists(data_dir):
    with st.spinner("EXECUTING_ENGINE..."): results = run_screener(symbols, data_dir)

_PERIOD_COLUMNS = {
    "1y": [("1Y_HIGH", "1Y High", "price"), ("%_DIV", "% From 1Y High", "pct")],
    "at": [("AT_HIGH", "AT High", "price"), ("%_DIV", "% From AT High", "pct")],
    "volume": [("DELIV_%", "Curr Delivery %", "pct"), ("TRADED_VOL", "Curr Traded Vol", "num")],
}
_DEFAULT_COLUMNS = _PERIOD_COLUMNS["at"]

def _resolve_columns(sk=None):
    if sk in ALL_SCANS:
        s = ALL_SCANS[sk]
        if s.get("subcategory") in _PERIOD_COLUMNS: return _PERIOD_COLUMNS[s["subcategory"]]
        if s.get("category") in _PERIOD_COLUMNS: return _PERIOD_COLUMNS[s["category"]]
    return _DEFAULT_COLUMNS

def _format_cell(val, fmt):
    if val is None: return '<td class="muted">NULL</td>'
    if fmt == "price": return f'<td class="muted">{val:,.2f}</td>'
    if fmt == "pct":
        c = "green" if val >= 0 else "red"
        return f'<td class="{c}">{" " if val >= 0 else ""}{val}%</td>'
    return f'<td class="muted">{val:,.0f}</td>'

def render_results_table(stock_list, scan_key=None, show_tags=False):
    if not stock_list: st.info("EOF: NO_RESULTS"); return
    extra_cols = _resolve_columns(scan_key)
    headers = ['SYMBOL', 'PRICE'] + [c[0] for c in extra_cols]
    if show_tags: headers.append('INSIGHTS')
    html = '<table class="clean-table"><thead><tr>' + "".join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
    for stock in stock_list:
        raw = stock['Symbol'].replace(".NS", "")
        tv = f"https://www.tradingview.com/chart/?symbol=NSE%3A{raw}"
        html += f'<tr><td class="bold"><a href="{tv}" target="_blank" style="text-decoration:none; color:inherit;">{stock["Symbol"]} [TAB]</a></td>'
        html += f'<td class="bold">{stock["Current Price"]:,.2f}</td>'
        for _, dk, f in extra_cols: html += _format_cell(stock.get(dk), f)
        if show_tags:
            ti = []
            for s in ALL_SCANS.values():
                if stock.get(s["data_key"]):
                    img = _get_icon_b64(s["data_key"])
                    if img: ti.append(f'<div class="insight-tag"><img src="{img}" style="height:18px;"></div>')
            html += f'<td>{" ".join(ti) if ti else "—"}</td>'
        html += '</tr>'
    st.markdown(html + '</tbody></table>', unsafe_allow_html=True)

def render_stat_cards(total, match):
    pct = round((match / total) * 100, 1) if total > 0 else 0
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-card stat-card-blue"><div class="stat-number">{match}</div><div class="stat-label">MATCH_COUNT</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card stat-card-green"><div class="stat-number">{pct}%</div><div class="stat-label">MATCH_INTENSITY</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card stat-card-purple"><div class="stat-number">{total}</div><div class="stat-label">UNIVERSE_SIZE</div></div>', unsafe_allow_html=True)

if st.session_state.page == "screener":
    st.markdown('<div class="main-header"><h1>[ MARKET_TERMINAL ]</h1></div>', unsafe_allow_html=True)
    if not results: st.stop()
    bo = [r for r in results if r.get("AT Breakout", False)]
    render_stat_cards(len(results), len(bo))
    t1, t2 = st.tabs(["BREAKOUTS", "DIRECTORY"])
    with t1: render_results_table(bo, "AT_breakout")
    with t2:
        render_results_table(results, show_tags=True)

elif st.session_state.page == "scans":
    if st.session_state.active_scan:
        scan = ALL_SCANS[st.session_state.active_scan]
        if st.button("<< BACK"): st.session_state.active_scan = None; st.rerun()
        st.markdown(f'<div class="main-header"><h1>{scan["label"]}</h1></div>', unsafe_allow_html=True)
        sr = [r for r in results if r.get(scan["data_key"], False)]
        render_stat_cards(len(results), len(sr))
        render_results_table(sr, st.session_state.active_scan)
    else:
        st.markdown('<div class="main-header"><h1>[ SYSTEM_SCANS ]</h1></div>', unsafe_allow_html=True)
        for cat_key, cat in SCAN_CATEGORIES.items():
            cat_icon = _get_icon_b64(f"Category_{cat_key}")
            st.markdown(f'<div class="scan-category-row"><div class="scan-cat-left"><div class="scan-cat-icon">{f"<img src={cat_icon} width=24>" if cat_icon else cat["icon"]}</div><b>{cat["title"]}</b></div><span class="scan-cat-count">{_count_all_scans_in_category(cat)} Ready</span></div>', unsafe_allow_html=True)
            with st.expander(f"EXECUTE_{cat['title']}"):
                for s_key, s_lab, s_desc, _ in (cat["scans"] or sum([sc["scans"] for sc in cat.get("subcategories",{}).values()], [])):
                    c1, c2 = st.columns([5,1])
                    c1.markdown(f"**{s_lab}**\n\n{s_desc}")
                    if c2.button("EXEC ›", key=f"run_{s_key}"): st.session_state.active_scan = s_key; st.rerun()

elif st.session_state.page == "combos":
    saved = load_saved_combos()
    if st.session_state.active_combo:
        cb = next((c for c in saved if c["name"] == st.session_state.active_combo), None)
        if st.button("<< BACK"): st.session_state.active_combo = None; st.rerun()
        st.markdown(f'<div class="main-header"><h1>🔗 {cb["name"]}</h1></div>', unsafe_allow_html=True)
        dk = [ALL_SCANS[k]["data_key"] for k in cb["scans"] if k in ALL_SCANS]
        cr = [r for r in results if all(r.get(d) for d in dk)]
        render_results_table(cr, show_tags=True)
    else:
        st.markdown('<div class="main-header"><h1>[ COMBINATION_OPS ]</h1></div>', unsafe_allow_html=True)
        if st.button("＋ CREATE_NEW"): st.session_state.creating_combo = not st.session_state.creating_combo; st.rerun()
        if st.session_state.creating_combo:
            nm = st.text_input("MODULE_NAME")
            sel = []
            for ck, ct in SCAN_CATEGORIES.items():
                with st.expander(ct["title"]):
                    for sk, sl, _, _ in (ct["scans"] or sum([s["scans"] for s in ct.get("subcategories",{}).values()], [])):
                        if st.checkbox(sl, key=f"c_{sk}"): sel.append(sk)
            if st.button("STORE_MODULE"): saved.append({"name": nm, "scans": sel}); save_combos(saved); st.session_state.creating_combo = False; st.rerun()
        for idx, c in enumerate(saved):
            st.markdown(f'<div class="combo-card"><b>{c["name"]}</b> | [{len(c["scans"])} units]</div>', unsafe_allow_html=True)
            cl_r, cl_d = st.columns([4,1])
            if cl_r.button(f"EXECUTE {c['name']}", key=f"r_{idx}"): st.session_state.active_combo = c["name"]; st.rerun()
            if cl_d.button("🗑", key=f"d_{idx}"): saved.pop(idx); save_combos(saved); st.rerun()

st.markdown("---")
st.markdown("<div style='text-align:center; color:#484f58; font-family:JetBrains Mono;'>SYSTEM_STABLE // BUILD_4A4</div>", unsafe_allow_html=True)
