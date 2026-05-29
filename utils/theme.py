"""
utils/theme.py
==============
Shared visual theme for the NZ Labour Demand Forecaster dashboard.

Provides:
  - Central colour palette (NZ ocean / blue-green executive style)
  - CSS injection for Streamlit (call inject_css() once per page)
  - Section-header helper        → section_header(title, subtitle="")
  - Metric card helper           → metric_card(label, value, delta=None, delta_label="")
  - Info card helper             → info_card(title, body, icon="")
  - Plotly layout factory        → plotly_layout(title, x_label="", y_label="")
  - Plotly colour sequence       → CHART_COLORS  (list)

Usage
-----
    from utils.theme import inject_css, section_header, metric_card, info_card, plotly_layout, CHART_COLORS
    inject_css()   # call once at the top of the page, after st.set_page_config
"""

import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# 1.  COLOUR PALETTE
# ---------------------------------------------------------------------------

PALETTE = {
    # Primary blues
    "deep_blue":      "#0B2D4E",   # darkest — sidebar bg, heavy headers
    "ocean_blue":     "#1A5276",   # primary brand colour
    "mid_blue":       "#1F6F9C",   # secondary interactive elements
    "sky_blue":       "#2E86C1",   # accent / chart line

    # Teals & greens
    "teal":           "#148A7D",   # positive indicators, CTAs
    "soft_teal":      "#1ABC9C",   # secondary teal accent
    "sage_green":     "#27AE60",   # success / upward deltas
    "light_green":    "#A9DFBF",   # very light positive bg tint

    # Neutrals
    "white":          "#FFFFFF",
    "card_bg":        "#F8FAFB",   # card background
    "surface":        "#EEF3F7",   # page section tint
    "border":         "#D5E3EC",   # subtle card borders
    "text_primary":   "#0D1F2D",   # near-black body text
    "text_secondary": "#4A6580",   # muted label / caption text
    "text_light":     "#7F9BB1",   # placeholder / disabled

    # Status
    "warning":        "#E67E22",
    "danger":         "#C0392B",
    "info_bg":        "#EBF5FB",
    "info_border":    "#2E86C1",
}

# ---------------------------------------------------------------------------
# 2.  CHART COLOUR SEQUENCE  (for Plotly)
# ---------------------------------------------------------------------------

CHART_COLORS = [
    PALETTE["ocean_blue"],
    PALETTE["teal"],
    PALETTE["sky_blue"],
    PALETTE["soft_teal"],
    PALETTE["sage_green"],
    PALETTE["mid_blue"],
    PALETTE["warning"],
]

FORECAST_COLOR      = PALETTE["teal"]
FORECAST_BAND_COLOR = "rgba(20, 138, 125, 0.15)"
HISTORICAL_COLOR    = PALETTE["ocean_blue"]

# ---------------------------------------------------------------------------
# 3.  CSS INJECTION
# ---------------------------------------------------------------------------

def inject_css() -> None:
    """
    Inject global Streamlit CSS.
    Call this once at the top of every page (after st.set_page_config).
    """
    css = f"""
    <style>
    /* ── Google Font import ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    /* ── Root variables ─────────────────────────────────────────────────── */
    :root {{
        --deep-blue:      {PALETTE["deep_blue"]};
        --ocean-blue:     {PALETTE["ocean_blue"]};
        --mid-blue:       {PALETTE["mid_blue"]};
        --sky-blue:       {PALETTE["sky_blue"]};
        --teal:           {PALETTE["teal"]};
        --soft-teal:      {PALETTE["soft_teal"]};
        --sage-green:     {PALETTE["sage_green"]};
        --card-bg:        {PALETTE["card_bg"]};
        --surface:        {PALETTE["surface"]};
        --border:         {PALETTE["border"]};
        --text-primary:   {PALETTE["text_primary"]};
        --text-secondary: {PALETTE["text_secondary"]};
        --text-light:     {PALETTE["text_light"]};
    }}

    /* ── Global typography ──────────────────────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
    }}

    /* ── Page background ────────────────────────────────────────────────── */
    .main .block-container {{
        background-color: {PALETTE["surface"]};
        padding: 2rem 2.5rem 3rem 2.5rem;
        max-width: 1280px;
    }}

    /* ── Sidebar ────────────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {PALETTE["deep_blue"]} 0%, {PALETTE["ocean_blue"]} 100%);
    }}
    section[data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: rgba(255,255,255,0.75) !important;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    section[data-testid="stSidebar"] a {{
        color: {PALETTE["soft_teal"]} !important;
    }}

    /* ── Main page title ────────────────────────────────────────────────── */
    h1 {{
        font-family: 'DM Serif Display', serif;
        font-size: 2rem !important;
        font-weight: 400 !important;
        color: {PALETTE["deep_blue"]} !important;
        letter-spacing: -0.02em;
        padding-bottom: 0.25rem;
        border-bottom: 3px solid {PALETTE["teal"]};
        margin-bottom: 1.25rem !important;
    }}

    /* ── H2 section headers (native st.header) ──────────────────────────── */
    h2 {{
        font-family: 'DM Sans', sans-serif;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: {PALETTE["ocean_blue"]} !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 2rem !important;
        margin-bottom: 0.75rem !important;
    }}

    /* ── H3 ─────────────────────────────────────────────────────────────── */
    h3 {{
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: {PALETTE["text_primary"]} !important;
        margin-bottom: 0.5rem !important;
    }}

    /* ── Body text ──────────────────────────────────────────────────────── */
    p, li, .stMarkdown p {{
        font-size: 0.92rem;
        line-height: 1.7;
        color: var(--text-secondary);
    }}

    /* ── Metrics ────────────────────────────────────────────────────────── */
    div[data-testid="metric-container"] {{
        background: {PALETTE["white"]};
        border: 1px solid {PALETTE["border"]};
        border-left: 4px solid {PALETTE["teal"]};
        border-radius: 8px;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 1px 4px rgba(11,45,78,0.06);
    }}
    div[data-testid="metric-container"] label {{
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: {PALETTE["text_light"]} !important;
    }}
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: {PALETTE["deep_blue"]} !important;
    }}
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        font-size: 0.8rem !important;
    }}
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] svg {{
        width: 0.85rem; height: 0.85rem;
    }}

    /* ── st.info / st.warning / st.success ──────────────────────────────── */
    div[data-testid="stAlert"] {{
        border-radius: 8px;
        border-left-width: 4px;
        font-size: 0.88rem;
    }}

    /* ── Dataframes & tables ─────────────────────────────────────────────── */
    .stDataFrame {{
        border: 1px solid {PALETTE["border"]};
        border-radius: 8px;
        overflow: hidden;
    }}
    .stDataFrame th {{
        background: {PALETTE["ocean_blue"]} !important;
        color: #ffffff !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.65rem 0.9rem !important;
    }}
    .stDataFrame td {{
        font-size: 0.85rem;
        color: {PALETTE["text_primary"]};
        padding: 0.55rem 0.9rem !important;
    }}
    .stDataFrame tr:nth-child(even) td {{
        background-color: {PALETTE["card_bg"]};
    }}

    /* ── Buttons ─────────────────────────────────────────────────────────── */
    .stDownloadButton > button,
    .stButton > button {{
        background: {PALETTE["ocean_blue"]};
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 0.5rem 1.25rem;
        transition: background 0.2s ease;
    }}
    .stDownloadButton > button:hover,
    .stButton > button:hover {{
        background: {PALETTE["teal"]};
        color: #ffffff;
    }}

    /* ── Select / multiselect / slider ───────────────────────────────────── */
    .stSelectbox label,
    .stMultiSelect label,
    .stSlider label,
    .stRadio label,
    .stCheckbox label {{
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: {PALETTE["text_secondary"]} !important;
    }}

    /* ── Expander ─────────────────────────────────────────────────────────── */
    .streamlit-expanderHeader {{
        font-size: 0.82rem;
        font-weight: 600;
        color: {PALETTE["ocean_blue"]};
        background: {PALETTE["card_bg"]};
        border: 1px solid {PALETTE["border"]};
        border-radius: 6px;
        padding: 0.6rem 1rem;
    }}

    /* ── Plotly chart container ───────────────────────────────────────────── */
    .stPlotlyChart {{
        background: {PALETTE["white"]};
        border: 1px solid {PALETTE["border"]};
        border-radius: 10px;
        padding: 0.5rem;
        box-shadow: 0 1px 6px rgba(11,45,78,0.07);
    }}

    /* ── Custom info/callout card ────────────────────────────────────────── */
    .nz-info-card {{
        background: {PALETTE["white"]};
        border: 1px solid {PALETTE["border"]};
        border-left: 4px solid {PALETTE["ocean_blue"]};
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 4px rgba(11,45,78,0.05);
    }}
    .nz-info-card .nz-card-title {{
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: {PALETTE["ocean_blue"]};
        margin-bottom: 0.35rem;
    }}
    .nz-info-card .nz-card-body {{
        font-size: 0.88rem;
        color: {PALETTE["text_secondary"]};
        line-height: 1.6;
        margin: 0;
    }}

    /* ── Section header block ────────────────────────────────────────────── */
    .nz-section-header {{
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        margin-top: 2rem;
        margin-bottom: 0.6rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid {PALETTE["border"]};
    }}
    .nz-section-header .nz-sh-title {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: {PALETTE["ocean_blue"]};
    }}
    .nz-section-header .nz-sh-subtitle {{
        font-size: 0.82rem;
        color: {PALETTE["text_light"]};
    }}

    /* ── Takeaway / key-insight block ────────────────────────────────────── */
    .nz-takeaway {{
        background: linear-gradient(135deg, {PALETTE["info_bg"]}, #e8f5f2);
        border: 1px solid {PALETTE["teal"]};
        border-left: 4px solid {PALETTE["teal"]};
        border-radius: 8px;
        padding: 0.9rem 1.25rem;
        margin-top: 1rem;
    }}
    .nz-takeaway .nz-tk-label {{
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: {PALETTE["teal"]};
        margin-bottom: 0.3rem;
    }}
    .nz-takeaway .nz-tk-text {{
        font-size: 0.9rem;
        color: {PALETTE["text_primary"]};
        line-height: 1.6;
        margin: 0;
    }}

    /* ── Controls panel ──────────────────────────────────────────────────── */
    .nz-controls-panel {{
        background: {PALETTE["white"]};
        border: 1px solid {PALETTE["border"]};
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 4px rgba(11,45,78,0.05);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 4.  COMPONENT HELPERS
# ---------------------------------------------------------------------------

def section_header(title: str, subtitle: str = "") -> None:
    """
    Render a styled section divider with an optional subtitle.

    Parameters
    ----------
    title    : Short all-caps label (e.g. "Regional Trends")
    subtitle : Optional longer description shown inline
    """
    subtitle_html = f'<span class="nz-sh-subtitle">— {subtitle}</span>' if subtitle else ""
    st.markdown(
        f"""
        <div class="nz-section-header">
            <span class="nz-sh-title">{title}</span>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str, icon: str = "") -> None:
    """
    Render a styled informational card.

    Parameters
    ----------
    title : Card heading (displayed in brand blue, uppercase)
    body  : Card body text
    icon  : Optional emoji or Unicode icon prepended to the title
    """
    prefix = f"{icon} " if icon else ""
    st.markdown(
        f"""
        <div class="nz-info-card">
            <div class="nz-card-title">{prefix}{title}</div>
            <p class="nz-card-body">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def takeaway_card(text: str, label: str = "Key Insight") -> None:
    """
    Render a teal-accented 'key takeaway' callout.

    Parameters
    ----------
    text  : The insight sentence(s)
    label : Override the label prefix (default "Key Insight")
    """
    st.markdown(
        f"""
        <div class="nz-takeaway">
            <div class="nz-tk-label">&#9670; {label}</div>
            <p class="nz-tk-text">{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def controls_panel_open() -> None:
    """Open a styled controls panel wrapper (must call controls_panel_close() after)."""
    st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)


def controls_panel_close() -> None:
    """Close the controls panel wrapper opened by controls_panel_open()."""
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 5.  PLOTLY LAYOUT FACTORY
# ---------------------------------------------------------------------------

def plotly_layout(
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    legend: bool = True,
    height: int = 420,
) -> dict:
    """
    Return a consistent Plotly layout dict for all charts in the dashboard.

    Usage
    -----
        fig = go.Figure(data=[...])
        fig.update_layout(**plotly_layout("NZ Hiring Demand Trend", "Date", "Index"))
        st.plotly_chart(fig, use_container_width=True)

    Parameters
    ----------
    title   : Chart title string
    x_label : X-axis title
    y_label : Y-axis title
    legend  : Whether to show the legend
    height  : Chart height in pixels
    """
    font_family = "DM Sans, sans-serif"

    return dict(
        title=dict(
            text=title,
            font=dict(
                family="DM Serif Display, serif",
                size=17,
                color=PALETTE["deep_blue"],
            ),
            x=0.0,
            xanchor="left",
            pad=dict(l=4, b=8),
        ),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=font_family,
            size=12,
            color=PALETTE["text_secondary"],
        ),
        xaxis=dict(
            title=dict(
                text=x_label,
                font=dict(size=11, color=PALETTE["text_light"]),
            ),
            tickfont=dict(size=10, color=PALETTE["text_secondary"]),
            showgrid=False,
            showline=True,
            linecolor=PALETTE["border"],
            linewidth=1,
            ticks="outside",
            ticklen=4,
            tickcolor=PALETTE["border"],
        ),
        yaxis=dict(
            title=dict(
                text=y_label,
                font=dict(size=11, color=PALETTE["text_light"]),
            ),
            tickfont=dict(size=10, color=PALETTE["text_secondary"]),
            showgrid=True,
            gridcolor=PALETTE["border"],
            gridwidth=1,
            zeroline=False,
            showline=False,
        ),
        legend=dict(
            visible=legend,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11, color=PALETTE["text_secondary"]),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        margin=dict(l=50, r=20, t=60, b=50),
        hoverlabel=dict(
            bgcolor=PALETTE["deep_blue"],
            bordercolor=PALETTE["teal"],
            font=dict(
                family=font_family,
                size=12,
                color="#ffffff",
            ),
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
    """
    Return a styled Plotly Scatter trace for a line chart.

    Parameters
    ----------
    x            : X-axis data (e.g. date series)
    y            : Y-axis data
    name         : Legend / hover name
    color        : Line colour (defaults to CHART_COLORS[0])
    dash         : Line dash style ("solid", "dot", "dash")
    width        : Line width in pixels
    show_markers : Whether to show circle markers on each data point
    """
    c = color or CHART_COLORS[0]
    marker = dict(size=5, color=c) if show_markers else dict(size=0)
    return go.Scatter(
        x=x,
        y=y,
        name=name,
        mode="lines+markers" if show_markers else "lines",
        line=dict(color=c, width=width, dash=dash),
        marker=marker,
        hovertemplate=f"<b>{name}</b>: %{{y:.1f}}<extra></extra>",
    )


def bar_trace(
    x,
    y,
    name: str,
    color: str = None,
) -> go.Bar:
    """
    Return a styled Plotly Bar trace.

    Parameters
    ----------
    x     : Category labels
    y     : Bar heights
    name  : Legend / hover name
    color : Bar colour (defaults to CHART_COLORS[0])
    """
    c = color or CHART_COLORS[0]
    return go.Bar(
        x=x,
        y=y,
        name=name,
        marker=dict(
            color=c,
            line=dict(width=0),
        ),
        hovertemplate=f"<b>{name}</b>: %{{y:.1f}}<extra></extra>",
    )


def forecast_band_trace(x, lower, upper, name: str = "Forecast interval") -> go.Scatter:
    """
    Return a shaded confidence-band trace for forecast charts.

    Parameters
    ----------
    x     : Date / X values (shared with forecast line)
    lower : Lower-bound series
    upper : Upper-bound series
    name  : Hover/legend label
    """
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
