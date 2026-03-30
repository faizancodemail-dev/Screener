import streamlit as st
import csv
import os

# ─── Import classes from your existing screener.py ───────────────────────────
from screener import Stock, Data_fetcher, Screener

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Breakout Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Light Minimal CSS with Pastel Accents ───────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Force light background */
    .stApp { background: #f8fafc; }

    .main-header {
        background: #ffffff;
        padding: 0.8rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .main-header h1 {
        color: #1e293b;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 0.8rem;
        margin: 0.2rem 0 0 0;
        font-weight: 400;
    }

    /* Stat cards with pastel accents */
    .stat-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.4rem 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }
    .stat-card-blue { border-top: 3px solid #93c5fd; }
    .stat-card-green { border-top: 3px solid #86efac; }
    .stat-card-purple { border-top: 3px solid #c4b5fd; }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.2;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 0.4rem;
    }

    /* Breakout tags */
    .tag-breakout {
        background: #ecfdf5;
        color: #059669;
        padding: 4px 14px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.72rem;
        display: inline-block;
        border: 1px solid #a7f3d0;
        letter-spacing: 0.5px;
    }
    .tag-none {
        background: #fef2f2;
        color: #dc2626;
        padding: 4px 14px;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.72rem;
        display: inline-block;
        border: 1px solid #fecaca;
        letter-spacing: 0.5px;
    }

    /* Table with alternating rows */
    .clean-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        background: #ffffff;
    }
    .clean-table thead th {
        background: #f8fafc;
        color: #64748b;
        padding: 13px 18px;
        font-weight: 600;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }
    .clean-table tbody tr:nth-child(even) {
        background: #f8fafc;
    }
    .clean-table tbody tr:nth-child(odd) {
        background: #ffffff;
    }
    .clean-table tbody tr {
        transition: background 0.15s ease;
    }
    .clean-table tbody tr:hover {
        background: #eff6ff !important;
    }
    .clean-table tbody td {
        padding: 11px 18px;
        font-size: 0.86rem;
        color: #475569;
        border-bottom: 1px solid #f1f5f9;
    }
    .green { color: #059669; font-weight: 600; }
    .red { color: #dc2626; font-weight: 600; }
    .bold { color: #1e293b; font-weight: 600; }
    .muted { color: #94a3b8; }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Light sidebar */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Custom Sidebar Nav */
    .sidebar-logo {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 2rem;
        padding-left: 0.5rem;
    }
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.6rem 1rem;
        color: #64748b;
        font-weight: 500;
        font-size: 0.95rem;
        border-radius: 8px;
        margin-bottom: 0.2rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .nav-item:hover {
        background: #f1f5f9;
        color: #1e293b;
    }
    .nav-item.active {
        background: #e2e8f0;
        color: #0f172a;
        font-weight: 600;
    }
    .nav-item .icon {
        margin-right: 0.8rem;
        font-size: 1.1rem;
        opacity: 0.7;
    }
    .nav-item.active .icon {
        color: #1e293b;
        opacity: 1;
    }

    /* Force all text to dark for light theme */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {
        color: #374151;
    }
    .stApp h1, .stApp h2, .stApp h3 { color: #1e293b; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #374151; }
    .stTabs [data-baseweb="tab"] { color: #475569; }
    .stTabs [aria-selected="true"] { color: #1e293b; }
    .stTextInput label, .stSelectbox label { color: #475569; font-weight: 500; }
    input, textarea { color: #1e293b !important; }
    .stCaption, [data-testid="stCaptionContainer"] { color: #94a3b8 !important; }

    /* Override widget backgrounds */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        color: #1e293b;
    }
    .stSelectbox div[data-baseweb="select"] > div:hover {
        background-color: #e2e8f0;
    }
    
    /* Button explicitly styled */
    .stButton > button {
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #334155 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover {
        background-color: #f1f5f9 !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
    }

    hr { border-color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helper functions ────────────────────────────────────────────────────────

def get_available_sectors():
    sectors = []
    names_dir = os.path.join(os.path.dirname(__file__), "NAMES")
    if os.path.exists(names_dir):
        for f in os.listdir(names_dir):
            if f.endswith(".csv"):
                sectors.append(f.replace(".csv", ""))
    return sorted(sectors)


def load_symbols(sector):
    symbols = []
    filepath = os.path.join(os.path.dirname(__file__), "NAMES", f"{sector}.csv")
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    symbols.append(row[0])
    return symbols


def run_screener(symbols):
    datafolder = os.path.join(os.path.dirname(__file__), "data")
    fetcher = Data_fetcher(datafolder)
    results = []

    for symbol in symbols:
        stock = Stock(symbol)
        prices = fetcher.fetch_price(symbol)
        if len(prices) == 0:
            continue
        stock.set_price(prices)
        results.append({
            "Symbol": symbol.replace(".NS", ""),
            "Full Symbol": symbol,
            "Current Price": round(stock.current_price(), 2),
            "52W High": round(stock.high(), 2),
            "% From High": round((stock.current_price() / stock.high() - 1) * 100, 2),
            "Breakout": stock.is_breakout(),
        })

    return results


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">StockScreener</div>
    <div class="nav-item active"><span class="icon">🔍</span> Screener</div>
    <br><br>
    """, unsafe_allow_html=True)

    st.markdown("### Data Controls")

    sectors = get_available_sectors()
    if not sectors:
        st.error("No sector files found in NAMES/ folder.")
        st.stop()

    selected_sector = st.selectbox(
        "Sector",
        sectors,
        index=sectors.index("final_names") if "final_names" in sectors else 0,
    )

    st.markdown("---")

    time_frame = st.selectbox(
        "Time Frame",
        options=[1, 2, 3, 5],
        format_func=lambda x: f"{x} Year{'s' if x > 1 else ''}",
        index=0,
    )

    st.markdown("---")

    st.markdown("**Download Data**")

    if st.button("Download Fresh Data", use_container_width=True):
        import yfinance as yf

        symbols_to_download = load_symbols(selected_sector)
        if not symbols_to_download:
            st.error("No symbols found in the selected sector.")
        else:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            os.makedirs(data_dir, exist_ok=True)

            progress_bar = st.progress(0)
            status_text = st.empty()
            total_symbols = len(symbols_to_download)

            for i, symbol in enumerate(symbols_to_download):
                status_text.text(f"Downloading {symbol}... ({i+1}/{total_symbols})")
                try:
                    data = yf.download(symbol, period=f"{time_frame}y", progress=False)
                    file_path = os.path.join(data_dir, f"{symbol}.csv")
                    data.to_csv(file_path)
                except Exception as e:
                    st.warning(f"Failed: {symbol} — {e}")
                progress_bar.progress((i + 1) / total_symbols)

            status_text.text("All downloads complete!")
            st.success(f"Downloaded {total_symbols} stocks.")
            st.rerun()

    st.markdown("---")
    st.caption(
        "Detects breakout stocks — where current price "
        "equals or exceeds the historical high."
    )


# ─── HEADER ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>Stock Breakout Screener</h1>
    <p>Detect stocks making new highs</p>
</div>
""", unsafe_allow_html=True)


# ─── LOAD DATA & RUN SCREENER ────────────────────────────────────────────────

symbols = load_symbols(selected_sector)

if not symbols:
    st.warning(f"No symbols found in `NAMES/{selected_sector}.csv`.")
    st.stop()

data_dir = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(data_dir):
    st.error("The data/ folder doesn't exist. Use the sidebar to download stock data first.")
    st.stop()

with st.spinner("Scanning stocks..."):
    results = run_screener(symbols)

if not results:
    st.warning("No stock data found. Make sure the data/ folder has CSV files.")
    st.stop()


# ─── STATS CARDS ─────────────────────────────────────────────────────────────

breakout_stocks = [r for r in results if r["Breakout"]]
total = len(results)
breakout_count = len(breakout_stocks)
pct = round((breakout_count / total) * 100, 1) if total > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card stat-card-blue">
        <div class="stat-number">{total}</div>
        <div class="stat-label">Stocks Scanned</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card stat-card-green">
        <div class="stat-number">{breakout_count}</div>
        <div class="stat-label">Breakout Stocks</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card stat-card-purple">
        <div class="stat-number">{pct}%</div>
        <div class="stat-label">Breakout Rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── TABS ────────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["Breakout Stocks", "All Stocks"])


# ──── TAB 1: Breakouts ───────────────────────────────────────────────────────
with tab1:
    if breakout_stocks:
        st.markdown(f"**{breakout_count} stocks** making new highs")
        st.markdown("")

        table_html = '<table class="clean-table"><thead><tr>'
        table_html += '<th>#</th><th>Symbol</th><th>Current Price</th><th>High</th><th>Status</th>'
        table_html += '</tr></thead><tbody>'

        for i, stock in enumerate(breakout_stocks, 1):
            table_html += f"""
            <tr>
                <td class="muted">{i}</td>
                <td class="bold">{stock['Symbol']}</td>
                <td class="green">₹{stock['Current Price']:,.2f}</td>
                <td class="muted">₹{stock['52W High']:,.2f}</td>
                <td><span class="tag-breakout">● Breakout</span></td>
            </tr>"""

        table_html += '</tbody></table>'
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("No breakout stocks detected.")


# ──── TAB 2: All Stocks ──────────────────────────────────────────────────────
with tab2:
    st.markdown(f"**All {total} stocks**")

    search = st.text_input("Search", "", placeholder="e.g. RELIANCE, TCS, INFY")

    filtered = results
    if search:
        search_upper = search.upper()
        filtered = [r for r in results if search_upper in r["Symbol"]]

    if filtered:
        table_html = '<table class="clean-table"><thead><tr>'
        table_html += '<th>#</th><th>Symbol</th><th>Price</th><th>High</th><th>% From High</th><th>Status</th>'
        table_html += '</tr></thead><tbody>'

        filtered_sorted = sorted(filtered, key=lambda x: (-x["Breakout"], -x["% From High"]))

        for i, stock in enumerate(filtered_sorted, 1):
            price_class = "green" if stock["% From High"] >= 0 else "red"
            pct_str = f"+{stock['% From High']}%" if stock["% From High"] >= 0 else f"{stock['% From High']}%"
            badge = '<span class="tag-breakout">● Breakout</span>' if stock["Breakout"] else '<span class="tag-none">● Below</span>'

            table_html += f"""
            <tr>
                <td class="muted">{i}</td>
                <td class="bold">{stock['Symbol']}</td>
                <td class="{price_class}">₹{stock['Current Price']:,.2f}</td>
                <td class="muted">₹{stock['52W High']:,.2f}</td>
                <td class="{price_class}">{pct_str}</td>
                <td>{badge}</td>
            </tr>"""

        table_html += '</tbody></table>'
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.warning("No stocks match your search.")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:0.78rem;'>"
    "Built with Streamlit · Data from Yahoo Finance"
    "</div>",
    unsafe_allow_html=True,
)
