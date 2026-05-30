"""
utils/theme.py
==============
Massey-inspired formal executive theme — NZ Labour Demand Forecaster.

Colour system
-------------
  #004B8D  primary navy    — titles, sidebar, table headers, metric accents
  #004B8D  deep navy       — hero bg, sidebar gradient base
  #1E293B  near-black navy — body text, chart titles
  #64748B  slate           — secondary text, captions, muted labels
  #F4BD58  gold            — accent only: section rules, borders, eyebrows
  #E2E8F0  cool gray       — card borders, gridlines, dividers
  #F8FAFC  off-white       — page surface
  #FFFFFF  white           — card backgrounds

Typography
----------
  Playfair Display — page titles, metric values (formal serif)
  Inter            — all body, UI labels, section headers, captions

Exports
-------
  PALETTE              dict of all named colour tokens
  CHART_COLORS         list[str] — ordered Plotly sequence
  FORECAST_COLOR       str
  FORECAST_BAND_COLOR  str
  HISTORICAL_COLOR     str

  inject_css()         → call once per page after st.set_page_config
  section_header()     → branded rule divider
  info_card()          → white card with gold top-border
  takeaway_card()      → navy callout block
  page_hero()          → full-width hero banner for inner pages
  plotly_layout()      → Plotly layout dict factory
  line_trace()         → styled go.Scatter
  bar_trace()          → styled go.Bar
  forecast_band_trace()→ shaded confidence band
"""

import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# 1.  COLOUR PALETTE
# ---------------------------------------------------------------------------

PALETTE = {
    # ── Massey navy scale ────────────────────────────────────────────────
    "navy_deep":   "#004B8D",   # deepest — hero bg, sidebar root
    "navy":        "#004B8D",   # primary — titles, sidebar, table heads
    "navy_body":   "#1E293B",   # near-black — body text, chart titles
    "navy_mid":    "#1E293B",   # alias used by pages (kept for compat)

    # ── Gold accent ──────────────────────────────────────────────────────
    "gold":        "#F4BD58",   # single accent — section rules, borders, eyebrows
    "gold_light":  "rgba(212,166,74,0.12)",  # forecast band fill

    # ── Surface & card ───────────────────────────────────────────────────
    "surface":     "#F8FAFC",   # page background
    "card_bg":     "#FFFFFF",   # card / panel white

    # ── Borders & dividers ───────────────────────────────────────────────
    "border":      "#E2E8F0",   # card borders, dividers
    "border_light":"#EEF2F7",   # very subtle inner dividers

    # ── Text scale ───────────────────────────────────────────────────────
    "text_primary":   "#1E293B",   # headings, metric values
    "text_body":      "#1E293B",   # body copy — high contrast on white
    "text_secondary": "#64748B",   # captions, labels, muted
    "text_light":     "#94A3B8",   # placeholders, disabled

    # ── Semantic ─────────────────────────────────────────────────────────
    "white":       "#FFFFFF",
    "positive":    "#166534",   # upward delta
    "negative":    "#991B1B",   # downward delta
    "info_bg":     "#EFF6FF",
    "warning":     "#92400E",
}

# ---------------------------------------------------------------------------
# 2.  CHART COLOUR SEQUENCE
# ---------------------------------------------------------------------------

CHART_COLORS = [
    "#003B5C",   # primary navy
    "#D4A64A",   # gold
    "#2563AB",   # mid blue
    "#0891B2",   # cyan-teal
    "#166534",   # green
    "#64748B",   # slate
    "#92400E",   # amber
]

FORECAST_COLOR      = PALETTE["gold"]
FORECAST_BAND_COLOR = PALETTE["gold_light"]
HISTORICAL_COLOR    = PALETTE["navy"]

# ---------------------------------------------------------------------------
# 3.  CSS INJECTION
# ---------------------------------------------------------------------------

def inject_css() -> None:
    """
    Inject global Streamlit CSS.
    Call once per page, immediately after st.set_page_config.
    """
    C = PALETTE   # local shorthand
    css = f"""
    <style>
    /* ── Fonts ──────────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── CSS custom properties ───────────────────────────────────────────── */
    :root {{
        --m-navy-deep:   {C["navy_deep"]};
        --m-navy:        {C["navy"]};
        --m-navy-body:   {C["navy_body"]};
        --m-gold:        {C["gold"]};
        --m-surface:     {C["surface"]};
        --m-card:        {C["card_bg"]};
        --m-border:      {C["border"]};
        --m-border-lt:   {C["border_light"]};
        --m-text:        {C["text_body"]};
        --m-muted:       {C["text_secondary"]};
        --m-light:       {C["text_light"]};
    }}

    /* ── Global base ─────────────────────────────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
        color: var(--m-text) !important;
        -webkit-font-smoothing: antialiased;
    }}

    /* ── Page canvas ─────────────────────────────────────────────────────── */
    .main .block-container {{
        background-color: {C["surface"]} !important;
        padding: 2rem 3rem 4rem 3rem !important;
        max-width: 1340px !important;
    }}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(175deg, #00263A 0%, #003B5C 100%) !important;
    border-right: 1px solid rgba(212,166,74,0.18) !important;
}}

/* Only style readable text content */
/* Do NOT target generic span, because Streamlit uses icon ligatures in spans */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
    color: rgba(255,255,255,0.9) !important;
    font-family: 'Inter', sans-serif !important;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.82) !important;
    padding: 0.35rem 0.5rem !important;
    border-radius: 4px !important;
    transition: color 0.15s ease !important;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
    color: #D4A64A !important;
    background: rgba(212,166,74,0.08) !important;
}}

section[data-testid="stSidebar"] [aria-selected="true"] {{
    background: rgba(212,166,74,0.14) !important;
    border-left: 3px solid #D4A64A !important;
    color: #ffffff !important;
}}

    /* ── Page title  h1 ─────────────────────────────────────────────────── */
    h1 {{
        font-family: 'Playfair Display', serif !important;
        font-size: 3rem !important;
        font-weight: 600 !important;
        color: {C["navy"]} !important;
        letter-spacing: -0.025em !important;
        line-height: 1.15 !important;
        border: none !important;
        padding: 0 0 0.75rem 0 !important;
        margin: 0 0 0.25rem 0 !important;
    }}

    /* ── H2  st.header ──────────────────────────────────────────────────── */
    h2 {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: {C["navy"]} !important;
        letter-spacing: -0.01em !important;
        margin-top: 2.5rem !important;
        margin-bottom: 0.9rem !important;
    }}

    /* ── H3 ─────────────────────────────────────────────────────────────── */
    h3 {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.55rem !important;
        font-weight: 600 !important;
        color: {C["navy_body"]} !important;
        margin-bottom: 0.55rem !important;
    }}

    /* ── Body copy ───────────────────────────────────────────────────────── */
    p, li {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        color: {C["text_body"]} !important;
        font-weight: 400 !important;
    }}
    .stMarkdown p {{
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        color: {C["text_body"]} !important;
    }}

    /* ── Captions ────────────────────────────────────────────────────────── */
    .stCaption, [data-testid="stCaptionContainer"] p {{
        font-size: 1.05rem !important;
        color: {C["text_secondary"]} !important;
        line-height: 1.6 !important;
    }}

    /* ── Metric cards ────────────────────────────────────────────────────── */
    div[data-testid="metric-container"] {{
        background: {C["card_bg"]} !important;
        border: 1px solid {C["border"]} !important;
        border-top: 3px solid {C["gold"]} !important;
        border-radius: 6px !important;
        padding: 1.4rem 1.5rem 1.25rem !important;
        box-shadow: 0 1px 8px rgba(0,59,92,0.07) !important;
        transition: box-shadow 0.2s ease !important;
    }}
    div[data-testid="metric-container"]:hover {{
        box-shadow: 0 4px 18px rgba(0,59,92,0.12) !important;
    }}
    div[data-testid="metric-container"] label {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.11em !important;
        color: {C["text_secondary"]} !important;
    }}
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
        font-family: 'Playfair Display', serif !important;
        font-size: 2.1rem !important;
        font-weight: 600 !important;
        color: {C["navy"]} !important;
        line-height: 1.15 !important;
        letter-spacing: -0.025em !important;
    }}
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }}

    /* ── Alert / info box ────────────────────────────────────────────────── */
    div[data-testid="stAlert"] {{
        border-radius: 5px !important;
        border-left-width: 4px !important;
        font-size: 0.92rem !important;
        padding: 0.85rem 1.2rem !important;
    }}

    /* ── Dataframes ──────────────────────────────────────────────────────── */
    .stDataFrame {{
        border: 1px solid {C["border"]} !important;
        border-radius: 6px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 4px rgba(0,59,92,0.05) !important;
    }}
    .stDataFrame thead th {{
        background: {C["navy"]} !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.09em !important;
        padding: 0.7rem 1rem !important;
    }}
    .stDataFrame td {{
        font-size: 0.9rem !important;
        color: {C["text_body"]} !important;
        padding: 0.6rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .stDataFrame tr:nth-child(even) td {{
        background-color: {C["surface"]} !important;
    }}

    /* ── Buttons ─────────────────────────────────────────────────────────── */
    .stDownloadButton > button,
    .stButton > button {{
        background: {C["navy"]} !important;
        color: #ffffff !important;
        border: 1px solid {C["navy"]} !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        padding: 0.5rem 1.35rem !important;
        transition: all 0.18s ease !important;
    }}
    .stDownloadButton > button:hover,
    .stButton > button:hover {{
        background: {C["navy_deep"]} !important;
        border-color: {C["navy_deep"]} !important;
        color: #ffffff !important;
    }}

    /* ── Form widget labels ──────────────────────────────────────────────── */
    .stSelectbox label,
    .stMultiSelect label,
    .stSlider label,
    .stRadio label,
    .stCheckbox label {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.09em !important;
        color: {C["text_secondary"]} !important;
    }}

    /* ── Expanders ───────────────────────────────────────────────────────── */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: {C["navy"]} !important;
        background: {C["card_bg"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 5px !important;
        padding: 0.65rem 1rem !important;
    }}

    /* ── Plotly chart wrapper ────────────────────────────────────────────── */
    .stPlotlyChart {{
        background: {C["card_bg"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        box-shadow: 0 1px 8px rgba(0,59,92,0.06) !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════
       CUSTOM COMPONENTS
    ═══════════════════════════════════════════════════════════════════════ */

    /* ── Page title area (used in inner pages via page_hero helper) ──────── */
    .m-page-title-area {{
        padding: 0 0 1.25rem 0;
        margin-bottom: 0.25rem;
        border-bottom: 3px solid {C["gold"]};
    }}
    .m-page-eyebrow {{
        font-family: 'Inter', sans-serif;
        font-size: 1.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: {C["gold"]};
        margin-bottom: 0.35rem;
    }}
    .m-page-title {{
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 600;
        color: {C["navy"]};
        letter-spacing: -0.025em;
        line-height: 1.15;
        margin: 0 0 0.5rem 0;
    }}
    .m-page-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 400;
        color: {C["text_secondary"]};
        line-height: 1.7;
        max-width: 1000px;
        margin: 0;
    }}

    /* ── Section header ──────────────────────────────────────────────────── */
    .m-section {{
        margin-top: 2.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.55rem;
        border-bottom: 2px solid {C["gold"]};
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
    }}
    .m-section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: {C["navy"]};
        letter-spacing: -0.01em;
    }}
    .m-section-sub {{
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 400;
        color: {C["text_secondary"]};
    }}

    /* ── Info / feature card ─────────────────────────────────────────────── */
    .m-card {{
        background: {C["card_bg"]};
        border: 1px solid {C["border"]};
        border-top: 3px solid {C["gold"]};
        border-radius: 6px;
        padding: 1.5rem 1.5rem 1.4rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 6px rgba(0,59,92,0.06);
        height: 100%;
        box-sizing: border-box;
    }}
    .m-card-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.65rem;
        display: block;
        line-height: 1;
    }}
    .m-card-label {{
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: {C["gold"]};
        margin-bottom: 0.45rem;
    }}
    .m-card-title {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: {C["navy"]};
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }}
    .m-card-body {{
        font-family: 'Inter', sans-serif;
        font-size: 0.92rem;
        color: {C["text_body"]};
        line-height: 1.7;
        margin: 0;
    }}

    /* ── Takeaway / insight callout ──────────────────────────────────────── */
    .m-takeaway {{
        background: {C["navy"]};
        border-left: 4px solid {C["gold"]};
        border-radius: 6px;
        padding: 1.4rem 1.75rem;
        margin-top: 1.75rem;
        margin-bottom: 0.5rem;
    }}
    .m-takeaway .m-tk-label {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.06rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.16em !important;
        color: {C["gold"]} !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }}
    .m-takeaway .m-tk-text {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        color: rgba(255,255,255,0.93) !important;
        line-height: 1.75 !important;
        margin: 0 !important;
    }}

    /* ── Controls / filter panel ─────────────────────────────────────────── */
    .m-controls {{
        background: {C["card_bg"]};
        border: 1px solid {C["border"]};
        border-radius: 6px;
        padding: 1.35rem 1.75rem;
        margin-bottom: 1.75rem;
        box-shadow: 0 1px 4px rgba(0,59,92,0.04);
    }}

    /* ── Direction / status card ─────────────────────────────────────────── */
    .m-status-card {{
        background: {C["card_bg"]};
        border: 1px solid {C["border"]};
        border-top: 3px solid {C["gold"]};
        border-radius: 6px;
        padding: 1.4rem 1.5rem 1.2rem;
        box-shadow: 0 1px 8px rgba(0,59,92,0.07);
    }}
    .m-status-label {{
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.11em;
        color: {C["text_secondary"]};
        margin-bottom: 0.4rem;
    }}
    .m-status-value {{
        font-family: 'Playfair Display', serif;
        font-size: 1.55rem;
        font-weight: 600;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}

    /* ── Misc ────────────────────────────────────────────────────────────── */
    hr {{
        border: none !important;
        border-top: 1px solid {C["border"]} !important;
        margin: 2rem 0 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 4.  COMPONENT HELPERS
# ---------------------------------------------------------------------------

def page_hero(
    title: str,
    subtitle: str = "",
    eyebrow: str = "NZ Labour Market Intelligence",
) -> None:
    """
    Full-width navy hero banner for inner pages.
    Rendered above all page content, replaces st.title() on inner pages.

    title    — large Playfair Display heading
    subtitle — optional single-line description
    eyebrow  — small all-caps label above the title
    """
    C = PALETTE
    subtitle_html = (
        f'<div style="font-family:Inter,sans-serif; font-size:1.2rem; font-weight:300; '
        f'color:#FFFFFF; line-height:1.7; max-width:1000px; margin:0.75rem 0 0 0;">'
        f'{subtitle}</div>'
    ) if subtitle else ""

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {C['navy_deep']} 0%, {C['navy']} 100%);
            border-radius: 8px;
            border-bottom: 3px solid {C['gold']};
            padding: 2.5rem 3rem;
            margin-bottom: 2.25rem;
            box-shadow: 0 3px 20px rgba(0,38,58,0.15);
        ">
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 1.10rem; font-weight: 700;
                text-transform: uppercase; letter-spacing: 0.2em;
                color: {C['gold']}; margin-bottom: 0.65rem;
            ">{eyebrow}</div>
            <div style="
                font-family: 'Playfair Display', serif;
                font-size: 3rem; font-weight: 1000;
                color: #ffffff; line-height: 1.15;
                letter-spacing: 0.060em; margin: 0;
            ">{title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    """
    Branded section divider with gold 2px underline.
    title    — bold navy label
    subtitle — optional muted descriptor inline
    """
    sub_html = (
        f'<span class="m-section-sub">— {subtitle}</span>'
    ) if subtitle else ""
    st.markdown(
        f"""
        <div class="m-section">
            <span class="m-section-title">{title}</span>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str, icon: str = "") -> None:
    """
    White card with gold top-border.
    title — card heading (displayed in navy)
    body  — body paragraph
    icon  — optional emoji prefix
    """
    icon_html = f'<span class="m-card-icon">{icon}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="m-card">
            {icon_html}
            <div class="m-card-title">{title}</div>
            <p class="m-card-body">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def takeaway_card(text: str, label: str = "Key Insight") -> None:
    """
    Navy callout block with gold left-border and white body text.
    text  — insight paragraph
    label — eyebrow label (default "Key Insight")
    """
    st.markdown(
        f"""
        <div class="m-takeaway">
            <span class="m-tk-label">&#9670; {label}</span>
            <p class="m-tk-text">{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def controls_panel_open() -> None:
    """Open a styled filter/controls panel wrapper."""
    st.markdown('<div class="m-controls">', unsafe_allow_html=True)


def controls_panel_close() -> None:
    """Close the controls panel opened by controls_panel_open."""
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 5.  PLOTLY LAYOUT FACTORY
# ---------------------------------------------------------------------------

def plotly_layout(
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    legend: bool = True,
    height: int = 440,
) -> dict:
    """
    Return a consistent Plotly layout dict for every chart in the dashboard.

    Design language
    ---------------
    - Playfair Display chart titles (formal, matches page typography)
    - Inter tick labels and axis labels
    - Very subtle #EEF2F7 gridlines — visible but not distracting
    - #003B5C navy hover tooltip with gold border
    - Transparent paper + plot backgrounds (card container provides white bg)
    """
    C = PALETTE
    return dict(
        title=dict(
            text=title,
            font=dict(family="Playfair Display, serif", size=18, color=C["navy"]),
            x=0.0, xanchor="left",
            pad=dict(l=6, b=12),
        ),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=C["text_secondary"]),
        xaxis=dict(
            title=dict(
                text=x_label,
                font=dict(family="Inter, sans-serif", size=11, color=C["text_light"]),
            ),
            tickfont=dict(
                family="Inter, sans-serif", size=11, color=C["text_secondary"]
            ),
            showgrid=False,
            showline=True,
            linecolor=C["border"],
            linewidth=1,
            ticks="outside",
            ticklen=4,
            tickcolor=C["border"],
        ),
        yaxis=dict(
            title=dict(
                text=y_label,
                font=dict(family="Inter, sans-serif", size=11, color=C["text_light"]),
            ),
            tickfont=dict(
                family="Inter, sans-serif", size=11, color=C["text_secondary"]
            ),
            showgrid=True,
            gridcolor=C["border_light"],
            gridwidth=1,
            zeroline=False,
            showline=False,
        ),
        legend=dict(
            visible=legend,
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left",   x=0,
            font=dict(family="Inter, sans-serif", size=12, color=C["text_secondary"]),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        margin=dict(l=56, r=24, t=70, b=56),
        hoverlabel=dict(
            bgcolor=C["navy"],
            bordercolor=C["gold"],
            font=dict(family="Inter, sans-serif", size=12, color="#ffffff"),
            namelength=-1,
        ),
        hovermode="x unified",
    )


def line_trace(
    x,
    y,
    name: str,
    color: str = None,
    dash: str = "solid",
    width: int = 2,
    show_markers: bool = False,
) -> go.Scatter:
    """Styled Plotly line (Scatter) trace."""
    c = color or CHART_COLORS[0]
    marker = (
        dict(size=6, color=c, line=dict(color="#ffffff", width=1.5))
        if show_markers else dict(size=0)
    )
    return go.Scatter(
        x=x, y=y, name=name,
        mode="lines+markers" if show_markers else "lines",
        line=dict(color=c, width=width, dash=dash),
        marker=marker,
        hovertemplate=f"<b>{name}</b>: %{{y:.1f}}<extra></extra>",
    )


def bar_trace(x, y, name: str, color: str = None) -> go.Bar:
    """Styled Plotly bar trace."""
    c = color or CHART_COLORS[0]
    return go.Bar(
        x=x, y=y, name=name,
        marker=dict(color=c, line=dict(width=0)),
        hovertemplate=f"<b>{name}</b>: %{{y:.1f}}<extra></extra>",
    )


def forecast_band_trace(
    x, lower, upper, name: str = "Forecast Interval"
) -> go.Scatter:
    """Shaded confidence-band polygon trace for forecast charts."""
    x_rev = list(x)[::-1]
    y_rev = list(lower)[::-1]
    return go.Scatter(
        x=list(x) + x_rev,
        y=list(upper) + y_rev,
        fill="toself",
        fillcolor=FORECAST_BAND_COLOR,
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        name=name,
        showlegend=True,
    )