from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Last Mile Logistics Auditor | Veridi Logistics",
    page_icon="VL",
    layout="wide",
    initial_sidebar_state="expanded",
)


COLORS = {
    "bg": "#f3f6fa",
    "panel": "#ffffff",
    "ink": "#111827",
    "muted": "#64748b",
    "line": "#d9e2ec",
    "blue": "#2563eb",
    "teal": "#0f766e",
    "green": "#15803d",
    "amber": "#f59e0b",
    "red": "#dc2626",
    "navy": "#172554",
    "soft_blue": "#dbeafe",
    "soft_red": "#fee2e2",
}

STATUS_COLORS = {
    "On Time": COLORS["green"],
    "Late": COLORS["amber"],
    "Super Late": COLORS["red"],
}

REQUIRED_FILES = {
    "state": Path("outputs/state_delivery_summary.csv"),
    "sentiment": Path("outputs/sentiment_by_delivery_status.csv"),
    "bucket": Path("outputs/delay_bucket_review_summary.csv"),
    "category": Path("outputs/category_delivery_summary.csv"),
}


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

:root {
    --bg: #f3f6fa;
    --panel: #ffffff;
    --ink: #111827;
    --muted: #64748b;
    --line: #d9e2ec;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg);
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
    color: var(--ink) !important;
}

.block-container {
    max-width: 1560px;
    padding: 1rem 1.6rem 2rem;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, p, li {
    color: var(--ink) !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.75rem;
}

div[data-testid="stHorizontalBlock"] {
    gap: 0.75rem;
}

.topbar {
    background: #ffffff;
    border: 1px solid var(--line);
    border-left: 7px solid #2563eb;
    border-radius: 8px;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
}

.brand-title {
    font-size: 24px;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: 0;
}

.brand-sub {
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
}

.top-pill {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    color: #1e3a8a;
    font-size: 12px;
    font-weight: 800;
    padding: 8px 10px;
    white-space: nowrap;
}

.kpi {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    min-height: 98px;
    padding: 13px 14px;
}

.kpi-label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

.kpi-value {
    color: var(--ink);
    font-size: 27px;
    font-weight: 800;
    line-height: 1.05;
    margin-top: 8px;
}

.kpi-note {
    color: var(--muted);
    font-size: 11px;
    font-weight: 600;
    margin-top: 5px;
}

.panel {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 12px 13px 8px;
}

.panel-title {
    color: var(--ink);
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0;
    margin-bottom: 2px;
}

.panel-sub {
    color: var(--muted);
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 4px;
}

.state-strip {
    background: #111827;
    border-radius: 8px;
    color: white;
    display: grid;
    gap: 1px;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    overflow: hidden;
}

.state-cell {
    background: #1f2937;
    padding: 11px 12px;
    min-height: 74px;
}

.state-label {
    color: #cbd5e1;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

.state-value {
    color: white;
    font-size: 21px;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 7px;
}

.state-note {
    color: #cbd5e1;
    font-size: 11px;
    font-weight: 600;
    margin-top: 3px;
}

.action-row {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(4, minmax(0, 1fr));
}

.action {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 8px;
    min-height: 94px;
    padding: 12px;
}

.action b {
    color: var(--ink);
    display: block;
    font-size: 13px;
    margin-bottom: 8px;
}

.action span {
    color: #475569;
    font-size: 12px;
    line-height: 1.45;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 8px;
    overflow: hidden;
}

[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 8px;
}

button[kind="secondary"] {
    border-radius: 8px !important;
}

hr.tight {
    border: none;
    border-top: 1px solid var(--line);
    margin: 0.7rem 0;
}

@media (max-width: 980px) {
    .topbar {
        align-items: flex-start;
        flex-direction: column;
    }
    .state-strip,
    .action-row {
        grid-template-columns: 1fr;
    }
    .kpi-value {
        font-size: 23px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


def stop_for_missing_files() -> None:
    missing = [str(path) for path in REQUIRED_FILES.values() if not path.exists()]
    if missing:
        st.error("Dashboard data is missing. Run the notebook to export the summary CSV files.")
        st.code("\n".join(missing), language="text")
        st.stop()


@st.cache_data
def load_data():
    stop_for_missing_files()

    state = pd.read_csv(REQUIRED_FILES["state"])
    sentiment = pd.read_csv(REQUIRED_FILES["sentiment"])
    bucket = pd.read_csv(REQUIRED_FILES["bucket"])
    category = pd.read_csv(REQUIRED_FILES["category"])

    status_order = ["On Time", "Late", "Super Late"]
    sentiment["Delivery_Status"] = pd.Categorical(
        sentiment["Delivery_Status"], categories=status_order, ordered=True
    )
    sentiment = sentiment.sort_values("Delivery_Status").reset_index(drop=True)

    state = state.sort_values("late_rate", ascending=False).reset_index(drop=True)
    category = category.sort_values("late_rate", ascending=False).reset_index(drop=True)

    return state, sentiment, bucket, category


def pct(value: float) -> str:
    return f"{value:.1%}"


def whole(value: float) -> str:
    return f"{int(round(value)):,}"


def score(value: float) -> str:
    return f"{value:.2f}"


def clean_label(value: str) -> str:
    return str(value).replace("_", " ").title()


def section(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"<div class='panel-title'>{title}</div><div class='panel-sub'>{subtitle}</div>",
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, note: str, color: str = COLORS["ink"]) -> None:
    st.markdown(
        f"""
<div class="kpi">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="color:{color};">{value}</div>
  <div class="kpi-note">{note}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def panel_start() -> None:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)


def panel_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def style_fig(fig, height=330, showlegend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["ink"], family="Inter, sans-serif", size=12),
        legend_title_text="",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(size=10, color=COLORS["ink"]),
        ),
        showlegend=showlegend,
    )
    fig.update_xaxes(
        gridcolor=COLORS["line"],
        zerolinecolor=COLORS["line"],
        linecolor=COLORS["line"],
        tickfont=dict(color=COLORS["ink"], size=11),
        title_font=dict(color=COLORS["muted"], size=11),
        showline=True,
    )
    fig.update_yaxes(
        gridcolor=COLORS["line"],
        zerolinecolor=COLORS["line"],
        linecolor=COLORS["line"],
        tickfont=dict(color=COLORS["ink"], size=11),
        title_font=dict(color=COLORS["muted"], size=11),
        showline=True,
    )
    fig.update_coloraxes(
        colorbar=dict(
            thickness=10,
            tickfont=dict(color=COLORS["ink"], size=10),
            outlinecolor=COLORS["line"],
        )
    )
    return fig


state_df, sent_df, bucket_df, cat_df = load_data()

total_delivered = int(state_df["delivered_orders"].sum())
total_late = int(state_df["late_orders"].sum())
total_super_late = int(state_df["super_late_orders"].sum())
total_on_time = total_delivered - total_late
national_late_rate = total_late / total_delivered
national_super_late_rate = total_super_late / total_delivered
national_on_time_rate = total_on_time / total_delivered
weighted_review_score = (
    (sent_df["avg_review_score"] * sent_df["order_count"]).sum() / sent_df["order_count"].sum()
)

state_df = state_df.copy()
state_df["on_time_orders"] = state_df["delivered_orders"] - state_df["late_orders"]
state_df["on_time_rate"] = 1 - state_df["late_rate"]
state_df["late_order_share"] = state_df["late_orders"] / total_late
state_df["risk_score"] = (
    state_df["late_rate"]
    * (state_df["super_late_rate"] + 0.01)
    * (5 - state_df["avg_review_score"])
    * state_df["delivered_orders"].pow(0.35)
)
state_df["risk_rank"] = state_df["risk_score"].rank(ascending=False, method="dense").astype(int)

cat_df = cat_df.copy()
cat_df["category_clean"] = cat_df["category"].map(clean_label)
cat_df["late_order_share"] = cat_df["late_orders"] / cat_df["late_orders"].sum()
cat_df["impact_score"] = cat_df["late_orders"] * (5 - cat_df["avg_review_score"])
cat_df["risk_score"] = cat_df["late_rate"] * (5 - cat_df["avg_review_score"]) * cat_df[
    "delivered_orders"
].pow(0.35)

worst_state = state_df.iloc[0]
highest_impact_state = state_df.sort_values("late_orders", ascending=False).iloc[0]
worst_super_state = state_df.sort_values("super_late_rate", ascending=False).iloc[0]
at_risk_states = int((state_df["late_rate"] > national_late_rate).sum())
worst_category = cat_df.iloc[0]
highest_impact_category = cat_df.sort_values("impact_score", ascending=False).iloc[0]
on_time_score = sent_df.loc[sent_df["Delivery_Status"] == "On Time", "avg_review_score"].iloc[0]
late_score = sent_df.loc[sent_df["Delivery_Status"] == "Late", "avg_review_score"].iloc[0]
super_late_score = sent_df.loc[sent_df["Delivery_Status"] == "Super Late", "avg_review_score"].iloc[0]
score_gap = on_time_score - super_late_score

with st.sidebar:
    st.markdown("## Veridi Logistics")
    st.caption("Audit controls")
    st.divider()

    state_choice = st.selectbox(
        "State drilldown",
        ["National"] + state_df["customer_state"].tolist(),
        index=0,
    )
    top_n_states = st.slider("States shown", 5, len(state_df), 14, 1)
    top_n_categories = st.slider("Categories shown", 5, min(25, len(cat_df)), 12, 1)
    min_category_orders = st.slider("Min category orders", 50, 1000, 100, 50)
    category_sort = st.radio(
        "Category ranking",
        ["Late rate", "Late orders", "Impact score"],
        horizontal=False,
    )

    st.divider()
    with st.expander("Download data"):
        for label, path in REQUIRED_FILES.items():
            st.download_button(
                label=f"{label.title()} CSV",
                data=path.read_bytes(),
                file_name=path.name,
                mime="text/csv",
                use_container_width=True,
            )

if state_choice == "National":
    focus = None
    focus_name = "National"
    focus_late_rate = national_late_rate
    focus_orders = total_delivered
    focus_late_orders = total_late
    focus_super_rate = national_super_late_rate
    focus_score = weighted_review_score
    focus_rank = "-"
else:
    focus = state_df.loc[state_df["customer_state"] == state_choice].iloc[0]
    focus_name = focus["customer_state"]
    focus_late_rate = focus["late_rate"]
    focus_orders = int(focus["delivered_orders"])
    focus_late_orders = int(focus["late_orders"])
    focus_super_rate = focus["super_late_rate"]
    focus_score = focus["avg_review_score"]
    focus_rank = f"#{int(focus['risk_rank'])}"

st.markdown(
    f"""
<div class="topbar">
  <div>
    <div class="brand-title">Last Mile Logistics Auditor</div>
    <div class="brand-sub">Delivery promise accuracy, regional risk, sentiment, and category performance</div>
  </div>
  <div class="top-pill">Focus: {focus_name}</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Delivered Orders", whole(total_delivered), "clean delivered base", COLORS["navy"])
with k2:
    kpi_card("Promise Accuracy", pct(national_on_time_rate), f"{whole(total_on_time)} on time", COLORS["green"])
with k3:
    kpi_card("Late Rate", pct(national_late_rate), f"{whole(total_late)} late orders", COLORS["amber"])
with k4:
    kpi_card("Super Late Rate", pct(national_super_late_rate), f"{whole(total_super_late)} over 5 days", COLORS["red"])

k5, k6, k7, k8 = st.columns(4)
with k5:
    kpi_card("Avg Review Score", f"{score(weighted_review_score)}/5", "delivered orders", COLORS["blue"])
with k6:
    kpi_card("Review Damage", f"-{score(score_gap)}", "on time vs super late", COLORS["red"])
with k7:
    kpi_card("States Above Avg", str(at_risk_states), f"of {len(state_df)} states", COLORS["amber"])
with k8:
    kpi_card("Highest Risk Category", clean_label(worst_category["category"]), pct(worst_category["late_rate"]), COLORS["teal"])

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="state-strip">
  <div class="state-cell">
    <div class="state-label">Drilldown</div>
    <div class="state-value">{focus_name}</div>
    <div class="state-note">risk rank {focus_rank}</div>
  </div>
  <div class="state-cell">
    <div class="state-label">Orders</div>
    <div class="state-value">{whole(focus_orders)}</div>
    <div class="state-note">delivered</div>
  </div>
  <div class="state-cell">
    <div class="state-label">Late Rate</div>
    <div class="state-value">{pct(focus_late_rate)}</div>
    <div class="state-note">{whole(focus_late_orders)} late</div>
  </div>
  <div class="state-cell">
    <div class="state-label">Super Late</div>
    <div class="state-value">{pct(focus_super_rate)}</div>
    <div class="state-note">5+ days late</div>
  </div>
  <div class="state-cell">
    <div class="state-label">Avg Review</div>
    <div class="state-value">{score(focus_score)}/5</div>
    <div class="state-note">customer sentiment</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

left, mid, right = st.columns([1.18, 0.95, 0.87])

with left:
    panel_start()
    section("Regional Late Rate", "Ranked by % late deliveries")
    geo_df = state_df.head(top_n_states).copy()
    geo_df["band"] = pd.cut(
        geo_df["late_rate"],
        bins=[-0.01, national_late_rate, 0.15, 1],
        labels=["Below national", "High", "Critical"],
    )
    fig_geo = px.bar(
        geo_df.sort_values("late_rate"),
        x="late_rate",
        y="customer_state",
        orientation="h",
        color="band",
        color_discrete_map={
            "Below national": COLORS["green"],
            "High": COLORS["amber"],
            "Critical": COLORS["red"],
        },
        custom_data=["delivered_orders", "late_orders", "super_late_rate", "avg_review_score"],
        labels={"late_rate": "Late Rate", "customer_state": "State"},
    )
    fig_geo.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>Late rate: %{x:.1%}<br>"
            "Late orders: %{customdata[1]:,} / %{customdata[0]:,}<br>"
            "Super late: %{customdata[2]:.1%}<br>"
            "Avg review: %{customdata[3]:.2f}/5<extra></extra>"
        )
    )
    fig_geo.add_vline(
        x=national_late_rate,
        line_color=COLORS["navy"],
        line_dash="dash",
        annotation_text=f"National {pct(national_late_rate)}",
        annotation_font_size=10,
    )
    style_fig(fig_geo, height=390)
    fig_geo.update_xaxes(tickformat=".0%", range=[0, max(0.26, geo_df["late_rate"].max() * 1.15)])
    st.plotly_chart(fig_geo, use_container_width=True)
    panel_end()

with mid:
    panel_start()
    section("Status Mix", "Share of delivered orders")
    fig_mix = px.pie(
        sent_df,
        names="Delivery_Status",
        values="order_count",
        hole=0.58,
        color="Delivery_Status",
        color_discrete_map=STATUS_COLORS,
    )
    fig_mix.update_traces(
        textinfo="percent",
        textfont=dict(size=12, color="#ffffff"),
        marker=dict(line=dict(color="#ffffff", width=2)),
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig_mix.add_annotation(
        text=f"{pct(national_on_time_rate)}<br><span style='font-size:11px'>accurate</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20, color=COLORS["ink"], family="Inter"),
    )
    style_fig(fig_mix, height=390)
    st.plotly_chart(fig_mix, use_container_width=True)
    panel_end()

with right:
    panel_start()
    section("Review by Status", "Average score")
    fig_status = px.bar(
        sent_df,
        x="Delivery_Status",
        y="avg_review_score",
        color="Delivery_Status",
        color_discrete_map=STATUS_COLORS,
        text=sent_df["avg_review_score"].map(lambda value: f"{value:.2f}"),
        custom_data=["order_count"],
        labels={"avg_review_score": "Avg Review", "Delivery_Status": ""},
    )
    fig_status.update_traces(
        textposition="outside",
        textfont=dict(color=COLORS["ink"], size=12),
        hovertemplate="<b>%{x}</b><br>Avg review: %{y:.2f}/5<br>Orders: %{customdata[0]:,}<extra></extra>",
    )
    style_fig(fig_status, height=390, showlegend=False)
    fig_status.update_yaxes(range=[0, 5.35], dtick=1)
    st.plotly_chart(fig_status, use_container_width=True)
    panel_end()

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

q1, q2 = st.columns([1, 1])

with q1:
    panel_start()
    section("Regional Risk Matrix", "Late rate vs review score")
    fig_matrix = px.scatter(
        state_df,
        x="late_rate",
        y="avg_review_score",
        size="delivered_orders",
        color="super_late_rate",
        color_continuous_scale=["#15803d", "#f59e0b", "#dc2626"],
        hover_name="customer_state",
        hover_data={
            "late_rate": ":.1%",
            "super_late_rate": ":.1%",
            "avg_review_score": ":.2f",
            "delivered_orders": ":,",
            "late_orders": ":,",
        },
        labels={
            "late_rate": "Late Rate",
            "avg_review_score": "Avg Review Score",
            "super_late_rate": "Super Late",
        },
    )
    fig_matrix.add_vline(x=national_late_rate, line_dash="dash", line_color=COLORS["navy"])
    fig_matrix.add_hline(y=weighted_review_score, line_dash="dash", line_color=COLORS["navy"])
    style_fig(fig_matrix, height=390)
    fig_matrix.update_xaxes(tickformat=".0%", range=[0, max(0.26, state_df["late_rate"].max() * 1.15)])
    fig_matrix.update_yaxes(range=[3.35, 4.45])
    st.plotly_chart(fig_matrix, use_container_width=True)
    panel_end()

with q2:
    panel_start()
    section("Delay Severity Curve", "Volume and review score")
    fig_bucket = make_subplots(specs=[[{"secondary_y": True}]])
    fig_bucket.add_trace(
        go.Bar(
            x=bucket_df["delay_bucket"],
            y=bucket_df["order_count"],
            name="Orders",
            marker_color=COLORS["soft_blue"],
            marker_line=dict(color="#93c5fd", width=1),
            hovertemplate="<b>%{x}</b><br>Orders: %{y:,}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig_bucket.add_trace(
        go.Scatter(
            x=bucket_df["delay_bucket"],
            y=bucket_df["avg_review_score"],
            name="Avg Review",
            mode="lines+markers",
            line=dict(color=COLORS["red"], width=3),
            marker=dict(size=8, color=COLORS["red"], line=dict(width=2, color="#ffffff")),
            hovertemplate="<b>%{x}</b><br>Avg review: %{y:.2f}/5<extra></extra>",
        ),
        secondary_y=True,
    )
    style_fig(fig_bucket, height=390)
    fig_bucket.update_yaxes(title_text="Orders", secondary_y=False)
    fig_bucket.update_yaxes(title_text="Avg Review", range=[0, 5.2], secondary_y=True)
    fig_bucket.update_xaxes(title_text="")
    st.plotly_chart(fig_bucket, use_container_width=True)
    panel_end()

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

cat_base = cat_df[cat_df["delivered_orders"] >= min_category_orders].copy()
if category_sort == "Late orders":
    cat_ranked = cat_base.sort_values("late_orders", ascending=False)
    category_metric = "late_orders"
    category_axis = "Late Orders"
elif category_sort == "Impact score":
    cat_ranked = cat_base.sort_values("impact_score", ascending=False)
    category_metric = "impact_score"
    category_axis = "Impact Score"
else:
    cat_ranked = cat_base.sort_values("late_rate", ascending=False)
    category_metric = "late_rate"
    category_axis = "Late Rate"

cat_top = cat_ranked.head(top_n_categories).copy()

c1, c2 = st.columns([1.08, 0.92])

with c1:
    panel_start()
    section("Category Risk", f"Ranked by {category_axis.lower()}")
    if cat_top.empty:
        st.warning("No categories match the current filter.")
    else:
        fig_cat = px.bar(
            cat_top.sort_values(category_metric),
            x=category_metric,
            y="category_clean",
            orientation="h",
            color="avg_review_score",
            color_continuous_scale=["#dc2626", "#f59e0b", "#15803d"],
            range_color=[1, 5],
            custom_data=["delivered_orders", "late_orders", "late_rate", "avg_review_score"],
            labels={
                category_metric: category_axis,
                "category_clean": "Category",
                "avg_review_score": "Avg Review",
            },
        )
        if category_metric == "late_rate":
            fig_cat.add_vline(x=national_late_rate, line_dash="dash", line_color=COLORS["navy"])
            fig_cat.update_xaxes(tickformat=".0%")
        fig_cat.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>Orders: %{customdata[0]:,}<br>"
                "Late orders: %{customdata[1]:,}<br>"
                "Late rate: %{customdata[2]:.1%}<br>"
                "Avg review: %{customdata[3]:.2f}/5<extra></extra>"
            )
        )
        style_fig(fig_cat, height=420)
        st.plotly_chart(fig_cat, use_container_width=True)
    panel_end()

with c2:
    panel_start()
    section("Category Impact Matrix", "Late rate vs review score")
    if cat_base.empty:
        st.warning("No categories match the current filter.")
    else:
        fig_cat_matrix = px.scatter(
            cat_base,
            x="late_rate",
            y="avg_review_score",
            size="delivered_orders",
            color="impact_score",
            color_continuous_scale=["#15803d", "#f59e0b", "#dc2626"],
            hover_name="category_clean",
            hover_data={
                "delivered_orders": ":,",
                "late_orders": ":,",
                "late_rate": ":.1%",
                "avg_review_score": ":.2f",
                "impact_score": ":.1f",
            },
            labels={
                "late_rate": "Late Rate",
                "avg_review_score": "Avg Review",
                "impact_score": "Impact",
            },
        )
        fig_cat_matrix.add_vline(x=national_late_rate, line_dash="dash", line_color=COLORS["navy"])
        fig_cat_matrix.add_hline(y=weighted_review_score, line_dash="dash", line_color=COLORS["navy"])
        style_fig(fig_cat_matrix, height=420)
        fig_cat_matrix.update_xaxes(tickformat=".0%")
        fig_cat_matrix.update_yaxes(range=[3.2, 4.75])
        st.plotly_chart(fig_cat_matrix, use_container_width=True)
    panel_end()

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

t1, t2 = st.columns([1, 1])

with t1:
    panel_start()
    section("State Leaderboard", "Worst regions by combined risk")
    state_table = (
        state_df.sort_values("risk_score", ascending=False)
        .head(12)[
            [
                "customer_state",
                "delivered_orders",
                "late_orders",
                "late_rate",
                "super_late_rate",
                "avg_review_score",
                "risk_rank",
            ]
        ]
        .copy()
    )
    state_table.columns = [
        "State",
        "Orders",
        "Late",
        "Late Rate",
        "Super Late",
        "Avg Score",
        "Risk Rank",
    ]
    state_table["Orders"] = state_table["Orders"].map(lambda value: f"{value:,}")
    state_table["Late"] = state_table["Late"].map(lambda value: f"{value:,}")
    state_table["Late Rate"] = state_table["Late Rate"].map(pct)
    state_table["Super Late"] = state_table["Super Late"].map(pct)
    state_table["Avg Score"] = state_table["Avg Score"].map(score)
    state_table["Risk Rank"] = state_table["Risk Rank"].map(lambda value: f"#{value}")
    st.dataframe(state_table, hide_index=True, use_container_width=True, height=320)
    panel_end()

with t2:
    panel_start()
    section("Category Leaderboard", "Highest operational impact")
    cat_table = (
        cat_df.sort_values("impact_score", ascending=False)
        .head(12)[
            [
                "category_clean",
                "delivered_orders",
                "late_orders",
                "late_rate",
                "avg_review_score",
                "impact_score",
            ]
        ]
        .copy()
    )
    cat_table.columns = ["Category", "Orders", "Late", "Late Rate", "Avg Score", "Impact"]
    cat_table["Orders"] = cat_table["Orders"].map(lambda value: f"{value:,}")
    cat_table["Late"] = cat_table["Late"].map(lambda value: f"{value:,}")
    cat_table["Late Rate"] = cat_table["Late Rate"].map(pct)
    cat_table["Avg Score"] = cat_table["Avg Score"].map(score)
    cat_table["Impact"] = cat_table["Impact"].map(lambda value: f"{value:,.0f}")
    st.dataframe(cat_table, hide_index=True, use_container_width=True, height=320)
    panel_end()

st.markdown("<hr class='tight'>", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="action-row">
  <div class="action"><b>Regional repair</b><span>Start with {worst_state['customer_state']}, {worst_super_state['customer_state']}, and {highest_impact_state['customer_state']}.</span></div>
  <div class="action"><b>Promise recalibration</b><span>National late rate is {pct(national_late_rate)}; high-risk states need more conservative estimates.</span></div>
  <div class="action"><b>Sentiment protection</b><span>Super-late orders score {score(super_late_score)}/5 vs {score(on_time_score)}/5 on time.</span></div>
  <div class="action"><b>Category controls</b><span>{clean_label(highest_impact_category['category'])} has the highest category impact score.</span></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div style="text-align:center;color:#64748b;font-size:11px;padding:14px 0 8px;">
  Veridi Logistics - Last Mile Logistics Auditor - Python + Streamlit
</div>
""",
    unsafe_allow_html=True,
)
