import streamlit as st
import csv
import os
import json
import base64

# ─── Import classes from your existing screener.py ───────────────────────────
from screener import download_data, run_screener

# ─── Directory Initialization ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
        color: #f0f6fc;
    }

    .main-header {
        background: #161b22;
        padding: 1.25rem 1.75rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        border-left: 6px solid #2dd4bf;
    }
    .main-header h1 { color: #ffffff; font-size: 1.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
    .main-header p { color: #c9d1d9; font-size: 0.82rem; margin-top: 6px; font-weight: 500; }

    .stat-card {
        background: #161b22; border-radius: 4px; padding: 1.4rem 1.2rem;
        text-align: left; border: 1px solid #30363d; height: 100%;
    }
    .stat-card-blue { border-left: 4px solid #58a6ff; }
    .stat-card-green { border-left: 4px solid #2dd4bf; }
    .stat-card-purple { border-left: 4px solid #fbbf24; }
    .stat-number { font-size: 2rem; font-weight: 700; color: #ffffff; font-family: 'JetBrains Mono', monospace; }
    .stat-label { color: #c9d1d9; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }

    .tag-breakout {
        background: #0d1117; color: #2dd4bf; padding: 3px 10px; border-radius: 2px;
        font-weight: 700; font-size: 0.68rem; display: inline-block; border: 1px solid #2dd4bf; 
        font-family: 'JetBrains Mono', monospace; text-transform: uppercase;
    }

    .clean-table {
        width: 100%; border-collapse: collapse; border: 1px solid #30363d; background: #0d1117;
    }
    .clean-table thead th {
        background: #161b22; color: #c9d1d9; padding: 14px; font-weight: 700;
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
        background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Target all Streamlit labels to ensure they are bright */
    [data-testid="stWidgetLabel"] p, label, .stMarkdown p {
        color: #f0f6fc !important;
        opacity: 1 !important;
    }

    hr { border-color: #30363d !important; }

    /* Expander Dark Theme */
    [data-testid="stExpander"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 4px !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary > span:not([data-testid="stExpanderToggleIcon"]) {
        color: #c9d1d9 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        background: transparent !important;
    }
    [data-testid="stExpanderToggleIcon"] {
        color: #c9d1d9 !important;
    }
    [data-testid="stExpander"] details {
        background: #0d1117 !important;
        border: none !important;
    }

    /* System Health Status */
    .health-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 4px;
        padding: 0.8rem; margin-bottom: 1rem;
    }
    .health-item { 
        display: flex; align-items: center; gap: 10px; font-size: 0.78rem; margin-bottom: 6px;
        color: #ffffff !important; font-weight: 800; font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.5px;
    }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; }
    .status-ok { background: #39d353; box-shadow: 0 0 8px #39d353; }
    .status-empty { background: #f85149; box-shadow: 0 0 8px #f85149; }
    .status-warn { background: #fbbf24; }

    /* Category List Styles */
    .scan-category-row {
        background: #161b22; border: 1px solid #30363d; padding: 1rem;
        border-radius: 4px; margin-bottom: 0.6rem; transition: all 0.2s; cursor: pointer;
        display: flex; align-items: center; justify-content: space-between;
    }
    .scan-category-row:hover { background: #1c2128; border-color: #58a6ff; }
    .scan-cat-left { display: flex; align-items: center; gap: 1rem; }
    .scan-cat-title { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #ffffff; font-size: 0.95rem; }
    .scan-cat-desc { font-size: 0.75rem; color: #c9d1d9; }
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
        background: rgba(66, 75, 84, 0.2);
        padding: 4px 6px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        margin-right: 6px;
        border: 1px solid rgba(88, 166, 255, 0.2);
    }
    .insight-tag img {
        filter: brightness(0.9);
    }

    .subcategory-header {
        color: #2dd4bf; 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 0.8rem; 
        font-weight: 800;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 5px;
        border-bottom: 1px solid #1c2128;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .scan-item-container {
        display: flex; 
        align-items: center; 
        padding: 0.5rem 0;
        border-bottom: 1px solid #161b22;
    }
    .scan-item-icon {
        width: 36px;
        height: 36px;
        background: #0d1117;
        border-radius: 4px;
        border: 1px solid #30363d;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
    }
    .scan-item-details {
        flex-grow: 1;
    }
    .scan-item-title {
        color: #f0f6fc;
        font-weight: 700;
        font-size: 0.95rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .scan-item-desc {
        color: #8b949e;
        font-size: 0.72rem;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)


# ─── Helper functions ────────────────────────────────────────────────────────

def get_available_sectors():
    sectors = []
    # Use global BASE_DIR for consistency
    names_dir = os.path.join(BASE_DIR, "NAMES")
    
    if os.path.exists(names_dir):
        for f in os.listdir(names_dir):
            if f.endswith(".csv"):
                # Always return exact filename base to avoid case mismatch on Linux
                sectors.append(f[:-4])
    return sorted(list(set(sectors)))

def load_symbols(sector):
    symbols = []
    # Linux is case-sensitive! We must append .csv exactly.
    filepath = os.path.join(BASE_DIR, "NAMES", f"{sector}.csv")
    
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip():
                    sym = row[0].strip()
                    # Append .NS if missing to ensure yfinance/screener logic works
                    if not sym.endswith(".NS") and "^" not in sym:
                        sym += ".NS"
                    symbols.append(sym)
    # Remove duplicates while preserving order
    return list(dict.fromkeys(symbols))


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
    "technical": {
        "title": "TECHNICAL_ENGINE", "desc": "Indicator-based signals.", "icon": "📈", "css_class": "technical",
        "scans": [], "coming_soon": True,
    },
    "fundamental": {
        "title": "FUNDAMENTAL_ENGINE", "desc": "Financial data analysis.", "icon": "🏦", "css_class": "fundamental",
        "scans": [], "coming_soon": True,
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
        icon_path = os.path.join(BASE_DIR, "icons", f"{safe_name}{ext}")
        if os.path.exists(icon_path):
            with open(icon_path, "rb") as f: return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return None

def _count_all_scans_in_category(cat):
    count = len(cat.get("scans", []))
    for sub in cat.get("subcategories", {}).values():
        count += len(sub["scans"])
    return count

def render_scan_item(s_key, s_lab, s_desc, s_data_key):
    """Helper to render a single scan row with icon and execute button."""
    icon_b64 = _get_icon_b64(s_data_key)
    c1, c2 = st.columns([5, 1])
    with c1:
        icon_html = f'<img src="{icon_b64}" width="22">' if icon_b64 else '🔍'
        st.markdown(f"""
        <div class="scan-item-container">
            <div class="scan-item-icon">{icon_html}</div>
            <div class="scan-item-details">
                <div class="scan-item-title">{s_lab}</div>
                <div class="scan-item-desc">{s_desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        # Move vertically to align with the middle of the row
        st.markdown('<div style="margin-top: 8px;">', unsafe_allow_html=True)
        if st.button("EXEC ›", key=f"run_{s_key}"):
            st.session_state.active_scan = s_key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

COMBOS_FILE = os.path.join(BASE_DIR, "saved_combos.json")
def load_saved_combos():
    if os.path.exists(COMBOS_FILE):
        try:
            with open(COMBOS_FILE, "r") as f: return json.load(f)
        except (json.JSONDecodeError, IOError): return []
    return []
def save_combos(combos):
    with open(COMBOS_FILE, "w") as f: json.dump(combos, f, indent=2)

# ─── Environment & State Detection ───────────────────────────────────────────

def get_env_state():
    """Detect the current state of data files."""
    data_dir = os.path.join(BASE_DIR, "data")
    
    # Price Data Check
    price_files = []
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith(".csv") and not f.startswith("^"):
                filepath = os.path.join(data_dir, f)
                # Check if file has actual data (not just headers, usually > 200 bytes)
                if os.path.getsize(filepath) > 200:
                    price_files.append(f)
        
    has_prices = len(price_files) > 0
        
    return {
        "has_prices": has_prices,
        "price_count": len(price_files),
    }

if "page" not in st.session_state: st.session_state.page = "scans"
if "active_scan" not in st.session_state: st.session_state.active_scan = None
if "active_combo" not in st.session_state: st.session_state.active_combo = None
if "creating_combo" not in st.session_state: st.session_state.creating_combo = False
if "selected_sector" not in st.session_state: st.session_state.selected_sector = None

# ─── Pre-load sectors so selected_sector is always defined before sidebar renders ─
_all_sectors = get_available_sectors()
if not _all_sectors:
    st.error("❌ No sector files found in NAMES/ folder. Please add at least one .csv sector file.")
    st.stop()

with st.sidebar:
    st.markdown('<div class="sidebar-logo">TERMINAL_v1.2</div>', unsafe_allow_html=True)
    if st.button("SYS_SCANS", use_container_width=True): st.session_state.page = "scans"; st.session_state.active_scan = None; st.rerun()
    if st.button("SYS_COMBOS", use_container_width=True): st.session_state.page = "combos"; st.session_state.active_scan = None; st.session_state.active_combo = None; st.rerun()
    if st.button("SYS_BACKTEST", use_container_width=True): st.session_state.page = "backtest"; st.session_state.active_scan = None; st.session_state.active_combo = None; st.rerun()
    st.markdown("---")
    st.markdown("### DATA_OPS")
    
    state = get_env_state()
    
    # Display System Health
    st.markdown(f"""
    <div class="health-card">
        <div class="health-item"><div class="status-dot {'status-ok' if state['has_prices'] else 'status-empty'}"></div> PRICES: {'READY' if state['has_prices'] else 'MISSING'}</div>
        <div class="health-item"><div class="status-dot {'status-ok' if state['has_prices'] else 'status-empty'}"></div> ENGINE: {'STABLE' if state['has_prices'] else 'PENDING'}</div>
    </div>
    """, unsafe_allow_html=True)

    sectors = _all_sectors
    selected_sector = st.selectbox("REGION_SELECT", sectors, index=0)
    st.markdown("---")
    
    # --- STEP 1: DOWNLOAD PRICES ---
    if st.button("STEP_1: FETCH_PRICES", use_container_width=True):
        symbols_to_download = load_symbols(selected_sector)
        if symbols_to_download:
            p = st.progress(0); s = st.empty()
            def up(sym, i, tot): s.text(f"FETCHING {sym}..."); p.progress((i+1)/tot)
            count = download_data(symbols_to_download, os.path.join(BASE_DIR, "data"), 10, up)
            st.success(f"SUCCESS: {count} SYMBOLS SYNCED")
            st.rerun()

    # ─── ENGINE DIAGNOSTICS ──────────────────────────────────────────────────
    with st.sidebar.expander("🛠️ ENGINE_DIAGNOSTICS"):
        st.write(f"**BASE_DIR:** `{BASE_DIR}`")
        st.write(f"**SECTOR:** `{selected_sector}`")
        if state['has_prices']:
            st.write(f"**FILES FOUND:** {state['price_count']}")
            _diag_data_dir = os.path.join(BASE_DIR, "data")
            sample = os.listdir(_diag_data_dir)[:5]
            st.write(f"**SAMPLES:** `{sample}`")
        else:
            st.write("❌ **DATA_DIR EMPTY**")
        # symbols is loaded after the sidebar block — show sector info instead
        st.write(f"**SECTOR FILE:** `NAMES/{selected_sector}.csv`")

# ─── Load symbols and run screener (outside sidebar, uses selected_sector from above) ─
symbols = load_symbols(selected_sector)
data_dir = os.path.join(BASE_DIR, "data")  # Always use BASE_DIR, not __file__ inline

@st.cache_data(ttl=300, show_spinner="EXECUTING_ENGINE...")
def _cached_screener(syms, d_dir):
    return run_screener(list(syms), d_dir)

results = []
if symbols and os.path.exists(data_dir):
    results = _cached_screener(tuple(symbols), data_dir)

_PERIOD_COLUMNS = {
    "1y": [("1Y_HIGH", "1Y High", "price"), ("%_FROM_HIGH", "% From 1Y High", "pct")],
    "at": [("AT_HIGH", "AT High", "price"), ("%_FROM_HIGH", "% From AT High", "pct")],
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
            is_coming_soon = cat.get("coming_soon", False)
            count_label = "COMING SOON" if is_coming_soon else f"{_count_all_scans_in_category(cat)} Ready"
            count_color = "#fbbf24" if is_coming_soon else "#2dd4bf"
            st.markdown(f'<div class="scan-category-row"><div class="scan-cat-left"><div class="scan-cat-icon">{f"<img src={cat_icon} width=24>" if cat_icon else cat["icon"]}</div><b>{cat["title"]}</b></div><span class="scan-cat-count" style="color:{count_color};">{count_label}</span></div>', unsafe_allow_html=True)
            
            if is_coming_soon:
                with st.expander(f"{cat['title']}", expanded=False):
                    st.markdown(f"""
                    <div style="text-align:center; padding: 2rem 1rem;">
                        <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">{cat['icon']}</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 1.1rem; color: #fbbf24; letter-spacing: 2px;">COMING SOON</div>
                        <div style="color: #8b949e; font-size: 0.8rem; margin-top: 0.5rem;">{cat['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                with st.expander(f"EXECUTE_{cat['title']}", expanded=(cat_key == "price")):
                    if cat.get("subcategories"):
                        for sub_key, sub in cat["subcategories"].items():
                            with st.expander(f"─ {sub['title']}", expanded=False):
                                for s_key, s_lab, s_desc, s_dk in sub["scans"]:
                                    render_scan_item(s_key, s_lab, s_desc, s_dk)
                    else:
                        for s_key, s_lab, s_desc, s_dk in cat["scans"]:
                            render_scan_item(s_key, s_lab, s_desc, s_dk)

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

elif st.session_state.page == "backtest":
    st.markdown('<div class="main-header"><h1>[ BACKTEST_ENGINE ]</h1></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align:center; padding: 2rem 1rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">⚙️</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 1.5rem; color: #fbbf24; letter-spacing: 2px;">COMING SOON</div>
        <div style="color: #8b949e; font-size: 0.85rem; margin-top: 0.5rem;">The Backtesting Engine is currently under development.</div>
    </div>
    """, unsafe_allow_html=True)
    
    img_path = os.path.join(BASE_DIR, "icons", "backtest_preview.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True, caption="Preview of upcoming Backtest Terminal")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#484f58; font-family:JetBrains Mono;'>SYSTEM_STABLE // BUILD_4A4</div>", unsafe_allow_html=True)
