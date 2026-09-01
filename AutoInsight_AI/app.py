# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
# pyrefly: ignore [missing-import]
import plotly.express as px

# pyrefly: ignore [missing-import]
from plotly.subplots import make_subplots
import json
from data_processor import DataProcessor
from ai_insights import AIInsightGenerator

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoInsight AI – BI Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="block-container"] {
    font-family: 'Inter', sans-serif !important;
    background: #f0f4f8 !important;
    color: #1a1a2e !important;
}
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }
header[data-testid="stHeader"]   { display: none !important; }

/* force ALL native streamlit text dark */
p, span, div, label, li, h1, h2, h3, h4, h5, h6 { color: #1a1a2e !important; }

/* ── hero ── */
.hero {
    background: linear-gradient(135deg,#1565c0 0%,#42a5f5 60%,#90caf9 100%);
    padding: 22px 40px 18px; display:flex; flex-direction:column; align-items:center;
    box-shadow: 0 2px 12px rgba(0,0,0,.18);
}
.hero-title { font-size:2.1rem; font-weight:700; color:#fff !important;
              display:flex; align-items:center; gap:10px; }
.hero-sub   { color:#e3f2fd !important; font-size:.95rem; margin-top:4px; }

/* ── card ── */
.card {
    background:#fff !important; border-radius:12px;
    padding:16px 18px; margin-bottom:14px;
    box-shadow:0 2px 10px rgba(0,0,0,.09); border:1px solid #e8eaf6;
}
.card-title {
    font-size:1rem !important; font-weight:700 !important;
    color:#1a237e !important; margin-bottom:10px !important;
    border-bottom:2px solid #e8eaf6; padding-bottom:6px; display:block;
}

/* ── metric boxes ── */
.metric-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
.metric-box  { border-radius:8px; padding:10px 12px; text-align:center;
               font-weight:700 !important; font-size:1.1rem !important; }
.metric-box .label { font-size:.7rem !important; font-weight:600 !important;
                     margin-top:3px; display:block; }
.m-green  { background:#e8f5e9 !important; color:#1b5e20 !important; }
.m-blue   { background:#e3f2fd !important; color:#0d47a1 !important; }
.m-orange { background:#fff3e0 !important; color:#bf360c !important; }
.m-teal   { background:#e0f2f1 !important; color:#004d40 !important; }
.m-green .label  { color:#2e7d32 !important; }
.m-blue  .label  { color:#1565c0 !important; }
.m-orange .label { color:#e65100 !important; }
.m-teal  .label  { color:#00695c !important; }

/* ── insight bullets ── */
.insight-bullet {
    display:flex; align-items:flex-start; gap:8px;
    padding:8px 12px; border-radius:8px; margin-bottom:8px;
    font-size:.85rem !important; line-height:1.5; color:#1a1a2e !important;
}
.insight-bullet.warn { background:#fff8e1 !important; border-left:3px solid #ff9800; }
.insight-bullet.good { background:#f1f8e9 !important; border-left:3px solid #4caf50; }
.insight-bullet.info { background:#e8f4fd !important; border-left:3px solid #2196f3; }

/* ── risk ── */
.risk-header { display:flex; align-items:center; gap:8px;
               font-size:1rem !important; font-weight:700 !important;
               color:#b71c1c !important; margin-bottom:8px; }
.risk-item   { display:flex; align-items:flex-start; gap:6px;
               font-size:.84rem !important; color:#212121 !important;
               margin-bottom:7px; line-height:1.45; }
.risk-dot    { color:#e53935 !important; flex-shrink:0; }

/* ── region legend ── */
.region-legend { display:flex; flex-direction:column; gap:5px; margin-top:8px; }
.legend-item { display:flex; align-items:center; gap:8px;
               font-size:.82rem !important; color:#212121 !important; font-weight:600; }
.legend-dot  { width:12px; height:12px; border-radius:3px; flex-shrink:0; }

/* ── recommendations ── */
.rec-item { display:flex; align-items:flex-start; gap:8px;
            font-size:.85rem !important; color:#1a1a2e !important;
            margin-bottom:8px; line-height:1.5; }
.rec-dot  { color:#ff9800 !important; flex-shrink:0; }

/* ── file uploader ── */
div[data-testid="stFileUploader"] { margin:0 !important; }
div[data-testid="stFileUploader"] label { display:none !important; }
div[data-testid="stFileUploader"] section {
    border:2px dashed #90caf9 !important; border-radius:8px !important;
    padding:10px 16px !important; background:#f5f9ff !important; min-height:unset !important;
}
div[data-testid="stFileUploader"] section span,
div[data-testid="stFileUploader"] section p,
div[data-testid="stFileUploader"] section small { color:#1565c0 !important; }

/* ── primary button ── */
.stButton > button {
    background: linear-gradient(135deg,#1565c0,#42a5f5) !important;
    color:#fff !important; border:none !important; border-radius:8px !important;
    padding:10px 28px !important; font-weight:600 !important;
    box-shadow:0 3px 10px rgba(21,101,192,.3);
}
.stButton > button p, .stButton > button span { color:#fff !important; }
.stButton > button:hover { transform:translateY(-1px); }

/* ── download button ── */
.stDownloadButton > button {
    background:#1565c0 !important; color:#fff !important;
    border-radius:8px !important; font-weight:600 !important;
}
.stDownloadButton > button p { color:#fff !important; }

/* ── expander ── */
[data-testid="stExpander"] {
    background:#fff !important; border-radius:10px !important;
    border:1px solid #e0e0e0 !important;
}
[data-testid="stExpander"] summary span { color:#1a237e !important; font-weight:600 !important; }

#MainMenu, footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-title">☁️ AutoInsight AI</div>
  <div class="hero-sub">Automated Business Intelligence Report Generator</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
API_KEY = "AIzaSyC_MuHH5duRNUncA28gDF-d4uEcmaJ9Z4U"

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def load_csv(uploaded):
    for enc in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            uploaded.seek(0)
            return pd.read_csv(uploaded, encoding=enc)
        except Exception:
            continue
    raise ValueError("Cannot decode this CSV. Please re-save as UTF-8.")

def fmt_num(n):
    if abs(n) >= 1_000_000: return f"${n/1_000_000:.2f}M"
    if abs(n) >= 1_000:     return f"${n/1_000:.1f}K"
    return f"{n:.1f}"

# ══════════════════════════════════════════════════════════════════════════════
# UPLOAD AREA (full-width bar below header)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding: 0 20px;">', unsafe_allow_html=True)
up_col1, up_col2 = st.columns([5, 1])
with up_col1:
    uploaded_file = st.file_uploader(
        "upload", type=['csv', 'xlsx', 'xls'], label_visibility="collapsed"
    )
with up_col2:
    generate_btn = st.button("⬆ Upload Data", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DEFAULT / DEMO DATA
# ══════════════════════════════════════════════════════════════════════════════
def demo_df():
    np.random.seed(42)
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    sales  = [320,380,290,410,450,390,480,520,460,540,580,620]
    profit = [60,75,45,90,95,70,100,110,85,120,130,150]
    return pd.DataFrame({
        'Month': months, 'Sales': sales, 'Profit': profit,
        'Region': ['North','South','East','West','North','South','East','West','North','South','East','West'],
        'Product': ['Product A','Product B','Product C','Others']*3,
        'Discount': np.random.uniform(5,30,12).round(1)
    })

# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
df = None
insights_data = {}
processed_data = {}

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = load_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ **{uploaded_file.name}** loaded — {df.shape[0]:,} rows × {df.shape[1]} columns")
    except Exception as e:
        st.error(f"❌ {e}")
else:
    df = demo_df()

# ══════════════════════════════════════════════════════════════════════════════
# PROCESS DATA
# ══════════════════════════════════════════════════════════════════════════════
try:
    processor = DataProcessor(df)
    processed_data = processor.process()
except Exception:
    processed_data = {'dataframe': df, 'kpis': {}, 'trends': {}, 'anomalies': {}, 'correlations': {}, 'summary': {}, 'statistics': pd.DataFrame(), 'column_info': {'numeric': [], 'categorical': [], 'date': []}}

numeric_cols    = df.select_dtypes(include=np.number).columns.tolist()
cat_cols        = df.select_dtypes(include='object').columns.tolist()

# ── Quick KPIs from auto-detected or first 4 numeric cols ──
kpi_vals = {}
for col in numeric_cols[:4]:
    kpi_vals[col] = df[col].sum()

# ══════════════════════════════════════════════════════════════════════════════
# AI INSIGHTS (generate on button click or auto if demo)
# ══════════════════════════════════════════════════════════════════════════════
if 'ai_insights' not in st.session_state:
    st.session_state['ai_insights'] = None

if generate_btn or (uploaded_file is None and st.session_state['ai_insights'] is None):
    with st.spinner("🤖 Generating AI insights…"):
        try:
            ai_gen = AIInsightGenerator(API_KEY)
            st.session_state['ai_insights'] = ai_gen.generate_insights(
                processed_data, "Comprehensive Analysis", "Detailed"
            )
        except Exception as e:
            st.session_state['ai_insights'] = {
                'executive_summary': str(e),
                'key_findings': ["Unable to generate insights. Check API key."],
                'recommendations': ["Verify your internet connection and API key."],
                'risks': []
            }

ai = st.session_state['ai_insights'] or {
    'executive_summary': 'Upload your data and click Upload Data to generate AI insights.',
    'key_findings': ['Sales trend analysis ready', 'Profit margin tracking enabled', 'Regional performance available'],
    'recommendations': ['Upload your dataset to get personalised recommendations.'],
    'risks': ['No risks detected yet — upload data to analyse.']
}

# ══════════════════════════════════════════════════════════════════════════════
# CHARTS
# ══════════════════════════════════════════════════════════════════════════════

# ── 1. Sales & Profit combo chart ──
def make_sales_chart():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    x_col = None
    # pick a time/label column
    for c in df.columns:
        if df[c].dtype == 'object' or str(df[c].dtype).startswith('datetime'):
            x_col = c; break
    if x_col is None and len(df) <= 50:
        x_col = df.index.astype(str)
    else:
        x_col = df[x_col] if x_col else df.index

    y1 = numeric_cols[0] if numeric_cols else None
    y2 = numeric_cols[1] if len(numeric_cols) > 1 else None

    if y1:
        fig.add_trace(go.Bar(
            x=x_col, y=df[y1], name=y1,
            marker_color='rgba(66,165,245,0.75)', showlegend=True
        ), secondary_y=False)
    if y2:
        fig.add_trace(go.Scatter(
            x=x_col, y=df[y2], name=y2,
            mode='lines+markers',
            line=dict(color='#ff9800', width=2.5),
            marker=dict(size=6, color='#ff9800'),
            showlegend=True
        ), secondary_y=True)

    fig.update_layout(
        title=dict(text="Monthly Sales & Profit Trend", font=dict(size=13, color='#1a237e')),
        height=270, margin=dict(l=10,r=10,t=38,b=10),
        plot_bgcolor='#fff', paper_bgcolor='#fff',
        legend=dict(orientation='h', y=1.15, x=0),
        font=dict(family='Inter', size=11),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=False, tickfont=dict(size=10))
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0', tickfont=dict(size=10))
    return fig

# ── 2. Regional map / bar ──
def make_regional_chart():
    if 'Region' in df.columns and numeric_cols:
        grp = df.groupby('Region')[numeric_cols[0]].sum().reset_index()
        total = grp[numeric_cols[0]].sum()
        grp['pct'] = ((grp[numeric_cols[0]] / total - 0.25) * 100).round(1)
        colors = ['#388e3c','#1565c0','#ff9800','#42a5f5']
        fig = go.Figure(go.Bar(
            x=grp['Region'], y=grp['pct'],
            marker_color=colors[:len(grp)],
            text=[f"{'+' if v>0 else ''}{v}%" for v in grp['pct']],
            textposition='outside', textfont=dict(size=11, color='#333')
        ))
        fig.update_layout(
            height=200, margin=dict(l=4,r=4,t=10,b=10),
            plot_bgcolor='#fff', paper_bgcolor='#fff',
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=True, zerolinecolor='#ccc'),
            xaxis=dict(showgrid=False),
            font=dict(family='Inter', size=11),
            showlegend=False
        )
        return fig, grp
    return None, None

# ── 3. Top products pie ──
def make_pie_chart():
    pie_col = None
    for c in cat_cols:
        if df[c].nunique() <= 10: pie_col = c; break
    if pie_col and numeric_cols:
        grp = df.groupby(pie_col)[numeric_cols[0]].sum().reset_index().nlargest(4, numeric_cols[0])
        fig = go.Figure(go.Pie(
            labels=grp[pie_col], values=grp[numeric_cols[0]],
            hole=0,
            marker=dict(colors=['#42a5f5','#ff9800','#66bb6a','#263238']),
            textinfo='percent', textfont=dict(size=11),
            showlegend=True
        ))
        fig.update_layout(
            height=200, margin=dict(l=4,r=4,t=10,b=10),
            paper_bgcolor='#fff',
            font=dict(family='Inter', size=10),
            legend=dict(font=dict(size=10), orientation='v', x=-.15)
        )
        return fig, grp, pie_col
    return None, None, None

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT — 3 columns
# ══════════════════════════════════════════════════════════════════════════════
pad = '<div style="padding: 0 12px;">'
st.markdown(pad, unsafe_allow_html=True)

left, center, right = st.columns([1.15, 2.2, 1.15], gap="small")

# ━━━━━━━━━━━━━━━━━━━━━━ LEFT COLUMN ━━━━━━━━━━━━━━━━━━━━━━
with left:
    # ── Upload panel ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📁 Upload Your Dataset</div>', unsafe_allow_html=True)
    findings = ai.get('key_findings', [])
    for f in findings[:4]:
        st.markdown(f'<div class="insight-bullet info">🔵 {f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Key Metrics ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Key Metrics</div>', unsafe_allow_html=True)
    m_classes = ['m-green','m-blue','m-orange','m-teal']
    m_labels  = list(kpi_vals.keys())
    m_values  = list(kpi_vals.values())
    grid_html = '<div class="metric-grid">'
    for i in range(min(4, len(m_labels))):
        cls = m_classes[i % 4]
        val = fmt_num(m_values[i])
        lbl = m_labels[i]
        grid_html += f'<div class="metric-box {cls}">{val}<div class="label">{lbl}</div></div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Risk Alerts ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="risk-header">🚨 Risk Alerts</div>', unsafe_allow_html=True)
    risks = ai.get('risks', [])
    if risks:
        for r in risks[:3]:
            st.markdown(f'<div class="risk-item"><span class="risk-dot">●</span>{r}</div>', unsafe_allow_html=True)
    else:
        anomalies = processed_data.get('anomalies', {})
        if anomalies:
            for col, anom in list(anomalies.items())[:2]:
                pct = anom.get('percentage', 0)
                st.markdown(f'<div class="risk-item"><span class="risk-dot">●</span>{col}: {anom["count"]} anomalies ({pct:.1f}% of data)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-item"><span class="risk-dot" style="color:#4caf50">✔</span>No significant risks detected.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━ CENTER COLUMN ━━━━━━━━━━━━━━━━━━━━━
with center:
    # ── Sales & Profit chart ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 Sales & Profit Analysis</div>', unsafe_allow_html=True)
    try:
        st.plotly_chart(make_sales_chart(), use_container_width=True, config={'displayModeBar': False})
    except Exception:
        st.info("Upload data with numeric columns to see chart.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── AI-Generated Insights ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🤖 AI-Generated Insights</div>', unsafe_allow_html=True)
    summary = ai.get('executive_summary', '')
    if summary:
        # Split into sentences for display
        sentences = [s.strip() for s in summary.replace('\n', ' ').split('.') if len(s.strip()) > 20]
        icons_cls = [('🔴', 'warn'), ('🟢', 'good'), ('🔵', 'info')]
        for i, s in enumerate(sentences[:3]):
            icon, cls = icons_cls[i % 3]
            st.markdown(f'<div class="insight-bullet {cls}">{icon} {s}.</div>', unsafe_allow_html=True)
    for f in findings[:2]:
        st.markdown(f'<div class="insight-bullet good">🟢 {f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Recommendations ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💡 Recommendations</div>', unsafe_allow_html=True)
    recs = ai.get('recommendations', [])
    for r in recs[:4]:
        st.markdown(f'<div class="rec-item"><span class="rec-dot">●</span>{r}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━ RIGHT COLUMN ━━━━━━━━━━━━━━━━━━━━━
with right:
    # ── Regional Performance ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗺️ Regional Performance</div>', unsafe_allow_html=True)
    reg_fig, reg_grp = make_regional_chart()
    if reg_fig:
        st.plotly_chart(reg_fig, use_container_width=True, config={'displayModeBar': False})
        # Legend
        r_colors = ['#388e3c','#1565c0','#ff9800','#42a5f5']
        legend_html = '<div class="region-legend">'
        for i, row in reg_grp.iterrows():
            clr = r_colors[i % 4]
            sign = '+' if row['pct'] >= 0 else ''
            legend_html += f'<div class="legend-item"><div class="legend-dot" style="background:{clr}"></div>{row["Region"]} &nbsp;<b>{sign}{row["pct"]}%</b></div>'
        legend_html += '</div>'
        st.markdown(legend_html, unsafe_allow_html=True)
    else:
        st.info("Add a 'Region' column to see regional breakdown.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Top Products ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏆 Top Products</div>', unsafe_allow_html=True)
    pie_fig, pie_grp, pie_col = make_pie_chart()
    if pie_fig:
        st.plotly_chart(pie_fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Add a categorical column (e.g. Product) to see distribution.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close padding div

# ══════════════════════════════════════════════════════════════════════════════
# STATS TABLE (collapsible)
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("📋 Full Statistical Summary", expanded=False):
    stats = processed_data.get('statistics')
    if stats is not None and not (hasattr(stats, 'empty') and stats.empty):
        st.dataframe(stats, use_container_width=True)
    else:
        st.dataframe(df.describe(), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("💾 Export Insights", expanded=False):
    ec1, ec2 = st.columns(2)
    with ec1:
        st.download_button(
            "📥 Download Insights (JSON)",
            data=json.dumps(ai, indent=2),
            file_name="autoinsight_report.json",
            mime="application/json",
            use_container_width=True
        )
    with ec2:
        st.download_button(
            "📥 Download Data (CSV)",
            data=df.to_csv(index=False),
            file_name="processed_data.csv",
            mime="text/csv",
            use_container_width=True
        )
