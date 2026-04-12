import os

def generate_svg(period, is_high=True):
    blue = "#1d4ed8"
    green = "#059669"
    red = "#dc2626"
    
    main_text = period
    sub_text = "Hi" if is_high else "Lo"
    arrow_color = green if is_high else red
    
    if is_high:
        main_x, main_y = 10, 42
        sub_x, sub_y = 54, 92
        line_start = (20, 80)
        line_end = (80, 20)
        arrow_head = "55,20 80,20 80,45"
    else:
        main_x, main_y = 50, 42
        sub_x, sub_y = 10, 92
        line_start = (20, 20)
        line_end = (80, 80)
        arrow_head = "55,80 80,80 80,55"
        
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <style>
    .t {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-weight: 800; font-size: 30px; fill: {blue}; }}
  </style>
  <line x1="8" y1="54" x2="92" y2="54" stroke="{blue}" stroke-width="6" stroke-linecap="round"/>
  <text x="{main_x}" y="{main_y}" class="t">{main_text}</text>
  <text x="{sub_x}" y="{sub_y}" class="t">{sub_text}</text>
  <line x1="{line_start[0]}" y1="{line_start[1]}" x2="{line_end[0]}" y2="{line_end[1]}" stroke="{arrow_color}" stroke-width="8" stroke-linecap="round"/>
  <polyline points="{arrow_head}" stroke="{arrow_color}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>"""

def generate_rs_svg(is_outperform=True):
    blue = "#1e3a8a" 
    amber = "#fcd34d"
    dark_gray = "#334155"
    
    top_text = "RS" if is_outperform else "MKT"
    bottom_text = "MKT" if is_outperform else "RS"
    bg_y = 10 if is_outperform else 50
    
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <style>
    .t {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-weight: 700; font-size: 30px; fill: {blue}; text-anchor: middle; }}
  </style>
  <rect x="15" y="{bg_y}" width="80" height="40" fill="{amber}"/>
  <text x="55" y="40" class="t">{top_text}</text>
  <text x="55" y="80" class="t">{bottom_text}</text>
  <line x1="15" y1="10" x2="15" y2="90" stroke="{blue}" stroke-width="4"/>
  <line x1="15" y1="90" x2="95" y2="90" stroke="{blue}" stroke-width="4"/>
  <line x1="15" y1="50" x2="95" y2="50" stroke="{dark_gray}" stroke-width="4" stroke-dasharray="10 8"/>
</svg>"""

def generate_near_svg(period, is_high=True):
    blue = "#1e3a8a"
    bg_color = "#bbf7d0" if is_high else "#fecaca"
    
    if is_high:
        texts = f'<text x="10" y="42" class="t">{period}</text>\n  <text x="55" y="42" class="t">Hi</text>'
        solid_line = f'<line x1="10" y1="48" x2="90" y2="48" stroke="{blue}" stroke-width="4" stroke-linecap="round"/>'
        bg_rect = f'<rect x="10" y="50" width="80" height="28" fill="{bg_color}"/>'
        dotted_line = f'<line x1="10" y1="82" x2="90" y2="82" stroke="{blue}" stroke-width="4" stroke-dasharray="5 5" stroke-linecap="round"/>'
        diagonals = "".join([f'<line x1="{12 + i*16}" y1="76" x2="{12 + i*16 + 10}" y2="52" stroke="{blue}" stroke-width="3" stroke-linecap="round"/>\n  ' for i in range(5)])
    else:
        texts = f'<text x="10" y="88" class="t">{period}</text>\n  <text x="55" y="88" class="t">Lo</text>'
        solid_line = f'<line x1="10" y1="52" x2="90" y2="52" stroke="{blue}" stroke-width="4" stroke-linecap="round"/>'
        bg_rect = f'<rect x="10" y="22" width="80" height="28" fill="{bg_color}"/>'
        dotted_line = f'<line x1="10" y1="18" x2="90" y2="18" stroke="{blue}" stroke-width="4" stroke-dasharray="5 5" stroke-linecap="round"/>'
        diagonals = "".join([f'<line x1="{12 + i*16}" y1="24" x2="{12 + i*16 + 10}" y2="48" stroke="{blue}" stroke-width="3" stroke-linecap="round"/>\n  ' for i in range(5)])
            
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <style>
    .t {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-weight: 700; font-size: 28px; fill: {blue}; }}
  </style>
  {texts}
  {solid_line}
  {bg_rect}
  {diagonals}
  {dotted_line}
</svg>"""

def generate_vol_quantity_svg(prefix):
    """Bar chart style for quantities/volumes."""
    navy = "#003893"
    light_blue = "#60a5fa"
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <text x="5" y="35" font-family="sans-serif" font-weight="600" font-size="34" fill="{navy}">{prefix}</text>
  <rect x="10" y="80" width="16" height="12" fill="{navy}" rx="2"/>
  <rect x="32" y="70" width="16" height="22" fill="{navy}" rx="2"/>
  <rect x="54" y="85" width="16" height="7" fill="{navy}" rx="2"/>
  <rect x="76" y="45" width="16" height="47" fill="{navy}" rx="2"/>
</svg>"""

def generate_vol_pct_svg(prefix):
    """Threshold style for percentage."""
    navy = "#003893"
    light_blue = "#93c5fd"
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <text x="5" y="85" font-family="sans-serif" font-weight="600" font-size="34" fill="{navy}">{prefix}</text>
  <line x1="38" y1="85" x2="38" y2="35" stroke="{navy}" stroke-width="4" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{navy}" />
    </marker>
  </defs>
  <line x1="45" y1="35" x2="95" y2="35" stroke="#64748b" stroke-width="2" stroke-dasharray="6 4"/>
  <rect x="55" y="25" width="30" height="60" fill="{navy}" rx="2"/>
  <rect x="55" y="15" width="30" height="10" fill="{light_blue}" rx="2"/>
</svg>"""

def generate_category_volume_svg():
    """Price line chart over volume bars (Category Logo)."""
    navy = "#003893"
    gray = "#94a3b8"
    return f"""<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <!-- Volume Bars -->
  <rect x="5" y="80" width="6" height="15" fill="{gray}" rx="1"/>
  <rect x="14" y="75" width="6" height="20" fill="{gray}" rx="1"/>
  <rect x="23" y="82" width="6" height="13" fill="{gray}" rx="1"/>
  <rect x="32" y="70" width="6" height="25" fill="{gray}" rx="1"/>
  <rect x="41" y="85" width="6" height="10" fill="{gray}" rx="1"/>
  <rect x="50" y="60" width="6" height="35" fill="{navy}" rx="1"/>
  <rect x="59" y="78" width="6" height="17" fill="{gray}" rx="1"/>
  <rect x="68" y="72" width="6" height="23" fill="{gray}" rx="1"/>
  <rect x="77" y="84" width="6" height="11" fill="{gray}" rx="1"/>
  <rect x="86" y="65" width="6" height="30" fill="{gray}" rx="1"/>
  
  <!-- Price Line (Wavy) -->
  <path d="M5,45 C20,30 35,60 50,45 S80,15 95,35" stroke="{navy}" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>"""

def generate_category_price_svg():
    """Rupee symbol inside a stylized search icon (Category Logo for Price)."""
    navy = "#003893"
    slate = "#475569"
    return f"""<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Search/Magnifying Glass Motif -->
  <circle cx="48" cy="45" r="32" stroke="{slate}" stroke-width="6" fill="none" stroke-dasharray="160 40"/>
  <line x1="72" x2="90" y1="68" y2="86" stroke="{slate}" stroke-width="8" stroke-linecap="round"/>
  
  <!-- Rupee Symbol -->
  <text x="48" y="58" font-family="sans-serif" font-weight="700" font-size="36" fill="{navy}" text-anchor="middle">₹</text>
</svg>"""

if __name__ == "__main__":
    base = os.path.dirname(__file__)

    def save_icon(name, content):
        safe_name = name.replace(":", "").replace("/", "").replace("%", "pct").replace(">", "gt").replace(" ", "_")
        path = os.path.join(base, f"{safe_name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # Category Icons
    save_icon("Category_volume", generate_category_volume_svg())
    save_icon("Category_price", generate_category_price_svg())
    
    # 1. Price Breakouts
    for p in ["1Y", "2Y", "AT", "5Y"]:
        save_icon(f"{p} Breakout", generate_svg(p, True))
        save_icon(f"{p} Breakdown", generate_svg(p, False))
        save_icon(f"Near {p} High", generate_near_svg(p, True))
        save_icon(f"Near {p} Low", generate_near_svg(p, False))

    # 2. RS
    for p in ["55W", "123D"]:
        save_icon(f"RS {p} Outperformer", generate_rs_svg(True))
        save_icon(f"RS {p} Underperformer", generate_rs_svg(False))

    # 3. Volume & Delivery (New Branding)
    # Mapping Display Labels to Prefix chars
    timeframes = {
        "Daily": "d",
        "Weekly": "w",
        "Monthly": "m",
        "Annual": "y"
    }

    metrics = [
        ("Delivery % Higher Annual", "d", "pct"),
        ("Delivery Vol Higher Annual", "d", "qty"),
        ("Weekly Delivery % > Avg", "w", "pct"),
        ("Weekly Delivery Vol > Avg", "w", "qty"),
        ("Monthly Delivery % > Avg", "m", "pct"),
        ("Monthly Delivery Vol > Avg", "m", "qty"),
        # Traded Volume
        ("Volume Higher Annual", "d", "qty"),
        ("Weekly Volume > Avg", "w", "qty"),
        ("Monthly Volume > Avg", "m", "qty")
    ]

    for label, prefix, m_type in metrics:
        content = generate_vol_pct_svg(prefix) if m_type == "pct" else generate_vol_quantity_svg(prefix)
        save_icon(label, content)
