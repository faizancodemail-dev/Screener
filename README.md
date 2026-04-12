# 🚀 Pro-Trader Terminal: Advanced Stock Screener

A professional-grade fintech dashboard and statistical screening engine designed for institutional-level stock market analysis. Built with **Python** and **Streamlit**, featuring a high-density industrial UI.

## 💎 Primary Features

- **Pro-Trader Terminal UI**: A high-fidelity, industrial "Dark Terminal" interface designed for professional traders who need high information density and tactical legibility.
- **Volume & Delivery Statistical Engine**: 
    - Benchmarks daily, weekly, and monthly performance against **1-year annual baselines**.
    - Identifies institutional delivery accumulation and traded volume surges across multiple timeframes.
- **Programmatic Branding**: Custom-generated SVG icon system (Volume, Delivery, Price, and RS) for clean, high-contrast visual cues.
- **Direct TradingView Integration**: Every stock symbol is an active link that redirects directly to its **TradingView Chart** (NSE) for immediate technical review.
- **Combination Scans Module**: Save your custom logic combinations into named "modules" for one-click execution during the trading day.

---

## ☁️ Hosting on Streamlit Community Cloud

This project is optimized for direct deployment from GitHub to Streamlit Cloud.

1. **Push to GitHub**: Push this repository to your GitHub account.
2. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Select your repository and the `main` branch.
   - **Main file path**: Set this to **`pro_trader.py`**.
3. **Important Note on Data Persistence**:
   - Streamlit Cloud is ephemeral. Historical data in the `data/` folder is cleared on reboot.
   - Use the **Sidebar Controls** to "Download Fresh Data" and "Merge Delivery Data" to refresh your local environment on the cloud.

---

## 🛠️ Local Setup

Experience the terminal in its most responsive state by running it locally:

1. **Clone & Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Terminal**:
   ```bash
   streamlit run pro_trader.py
   ```

## 📂 Repository Structure
- `pro_trader.py`: The flagship Terminal UI.
- `screener.py`: The core high-performance screening and data processing logic.
- `icons/`: Programmatically generated SVG assets.
- `NAMES/`: Sector-wise symbol lists for targeted scanning.
- `saved_combos.json`: Your persistent custom scan module configurations.

---
*Created for advanced traders and technical analysts.*
