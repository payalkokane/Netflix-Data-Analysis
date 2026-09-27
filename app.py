from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).with_name("Netflix.csv")
IMAGES_PATH = Path(__file__).with_name("images")
REQUIRED_COLUMNS = (
    "Customer_ID",
    "Region",
    "Subscription_Plan",
    "Category",
    "Type",
    "Rating",
    "Watch_Count",
    "Watch_Date",
    "Watch_Time_Minutes",
    "Device",
    "Monthly_Revenue",
)

st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

px.defaults.template = "plotly_dark"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink: #f5f5f5; --muted: #a3a3a3; --red: #e50914; --line: #303030; --surface: #141414; --canvas: #090909; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: var(--canvas); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(9, 9, 9, .92); }
    h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] { color: var(--ink); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
    h1 { letter-spacing: 0 !important; font-size: 2.15rem !important; }
    [data-testid="stSidebar"] { background: #101010; border-right: 1px solid var(--line); }
    [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px; }
    [data-testid="stMetricLabel"] { color: #b3b3b3; }
    [data-testid="stMetricValue"] { color: #fff; font-family: 'Space Grotesk', sans-serif; }
    .page-kicker { color: var(--red); text-transform: uppercase; font-size: .75rem; font-weight: 700; letter-spacing: 0; margin-bottom: 4px; }
    .page-caption { color: var(--muted); margin-top: -10px; margin-bottom: 22px; }
    .section-heading { color: #fff; font: 600 1.08rem 'Space Grotesk', sans-serif; margin: 12px 0 2px; }
    div[data-testid="stPlotlyChart"] { background: #111; border: 1px solid #292929; border-radius: 8px; padding: 8px 8px 0; }
    [data-baseweb="select"] > div, [data-testid="stDateInput"] input { background: #1b1b1b; color: #fff; border-color: #383838; }
    [data-testid="stFileUploader"] section { background: #171717; border-color: #454545; }
    [data-testid="stTabs"] button { color: #bdbdbd; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: #fff; border-bottom-color: var(--red); }
    [data-testid="stExpander"] { background: #141414; border-color: #303030; }
    [data-testid="stDataFrame"] { background: #141414; }
    [data-testid="stAlert"] { background: #1b1b1b; color: #fff; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Dataset is missing required columns: {missing}")

    data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
    for column in ("Rating", "Watch_Count", "Watch_Time_Minutes", "Monthly_Revenue"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data.dropna(subset=["Watch_Date"])


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return prepare_data(pd.read_csv(path))


@st.cache_data
def load_uploaded_data(file_contents: bytes) -> pd.DataFrame:
    return prepare_data(pd.read_csv(BytesIO(file_contents)))


st.sidebar.markdown("## Explore the data")
sidebar_logo = IMAGES_PATH / "image3.jfif"
if sidebar_logo.exists():
    st.sidebar.image(str(sidebar_logo), width="stretch")
st.sidebar.caption("Filters apply across every metric and chart.")
uploaded_file = st.sidebar.file_uploader("Upload dataset", type=["csv"], help="Upload a CSV with the Netflix dataset columns.")

try:
    if uploaded_file is not None:
        netflix = load_uploaded_data(uploaded_file.getvalue())
        st.sidebar.caption(f"Using uploaded file: {uploaded_file.name}")
    elif DATA_PATH.exists():
        netflix = load_data(DATA_PATH)
        st.sidebar.caption(f"Using default dataset: {DATA_PATH.name}")
    else:
        st.error("No dataset is loaded. Upload a CSV file to get started.")
        st.stop()
except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error(f"Could not use this dataset: {error}")
    st.stop()

if netflix.empty:
    st.error("The dataset has no rows with valid watch dates. Check the Watch_Date column and upload again.")
    st.stop()

regions = st.sidebar.multiselect("Region", sorted(netflix["Region"].dropna().unique()), default=sorted(netflix["Region"].dropna().unique()))
plans = st.sidebar.multiselect(
    "Subscription plan",
    sorted(netflix["Subscription_Plan"].dropna().unique()),
    default=sorted(netflix["Subscription_Plan"].dropna().unique()),
)
categories = st.sidebar.multiselect(
    "Category",
    sorted(netflix["Category"].dropna().unique()),
    default=sorted(netflix["Category"].dropna().unique()),
)
content_types = st.sidebar.multiselect(
    "Content type",
    sorted(netflix["Type"].dropna().unique()),
    default=sorted(netflix["Type"].dropna().unique()),
)
date_min = netflix["Watch_Date"].min().date()
date_max = netflix["Watch_Date"].max().date()
date_range = st.sidebar.date_input("Watch date", value=(date_min, date_max), min_value=date_min, max_value=date_max)

filtered = netflix[
    netflix["Region"].isin(regions)
    & netflix["Subscription_Plan"].isin(plans)
    & netflix["Category"].isin(categories)
    & netflix["Type"].isin(content_types)
].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[filtered["Watch_Date"].dt.date.between(start_date, end_date)]

title_column, artwork_column = st.columns([1.8, 1], vertical_alignment="center")
with title_column:
    st.markdown('<div class="page-kicker">Audience &amp; viewing</div>', unsafe_allow_html=True)
    st.title("Netflix Data Analysis")
    st.markdown('<div class="page-caption">A closer look at subscriptions, viewing habits, and monthly revenue.</div>', unsafe_allow_html=True)
with artwork_column:
    feature_art = IMAGES_PATH / "image4.jfif"
    if feature_art.exists():
        st.image(str(feature_art), width="stretch")

if filtered.empty:
    st.info("No records match these filters. Widen your selection to see results.")
    st.stop()

total_revenue = filtered["Monthly_Revenue"].sum()
total_watches = filtered["Watch_Count"].sum()
total_minutes = filtered["Watch_Time_Minutes"].sum()
average_rating = filtered["Rating"].mean()
customer_count = filtered["Customer_ID"].nunique()

metric_columns = st.columns(4)
metric_columns[0].metric("Monthly revenue", f"{total_revenue:,.0f}")
metric_columns[1].metric("Viewing hours", f"{total_minutes / 60:,.0f}")
metric_columns[2].metric("Average rating", f"{average_rating:.2f} / 5" if pd.notna(average_rating) else "N/A")
metric_columns[3].metric("Unique customers", f"{customer_count:,}")

st.markdown('<div class="section-heading">Month-wise revenue</div>', unsafe_allow_html=True)
monthly = filtered.assign(Month=filtered["Watch_Date"].dt.to_period("M").dt.to_timestamp())
monthly_revenue = monthly.groupby("Month", as_index=False)["Monthly_Revenue"].sum()
monthly_revenue["Month name"] = monthly_revenue["Month"].dt.strftime("%b %Y")
monthly_revenue["Revenue share (%)"] = monthly_revenue["Monthly_Revenue"].div(monthly_revenue["Monthly_Revenue"].sum()).mul(100)
monthly_revenue["Revenue share label"] = monthly_revenue["Revenue share (%)"].map(lambda share: f"{share:.1f}%")

bar_tab, pie_tab, line_tab = st.tabs(["Bar chart", "Pie chart", "Line chart"])

with bar_tab:
    bar_chart = px.bar(
        monthly_revenue,
        x="Month name",
        y="Monthly_Revenue",
        text="Revenue share label",
        hover_data=["Revenue share (%)"],
        labels={"Month name": "Month", "Monthly_Revenue": "Revenue", "Revenue share (%)": "Revenue share"},
        color_discrete_sequence=["#e50914"],
    )
    bar_chart.update_layout(margin=dict(l=12, r=12, t=18, b=8), height=390, paper_bgcolor="#0b0b0b", plot_bgcolor="#111111", font_color="#f5f5f5")
    bar_chart.update_traces(textposition="outside", cliponaxis=False)
    bar_chart.update_xaxes(showgrid=False)
    bar_chart.update_yaxes(showgrid=True, gridcolor="#333333", zeroline=False)
    st.plotly_chart(bar_chart, use_container_width=True)

with pie_tab:
    pie_chart = px.pie(
        monthly_revenue,
        names="Month name",
        values="Monthly_Revenue",
        color_discrete_sequence=["#e50914", "#f5f5f5", "#b20710", "#777777", "#76000a", "#c9c9c9"],
    )
    pie_chart.update_layout(margin=dict(l=12, r=12, t=18, b=8), height=390, paper_bgcolor="#0b0b0b", font_color="#f5f5f5")
    pie_chart.update_traces(textposition="inside", textinfo="percent+label", marker_line_color="#111111", marker_line_width=2)
    st.plotly_chart(pie_chart, use_container_width=True)

with line_tab:
    line_chart = px.line(
        monthly_revenue,
        x="Month",
        y="Monthly_Revenue",
        markers=True,
        labels={"Month": "Month", "Monthly_Revenue": "Revenue"},
        color_discrete_sequence=["#e50914"],
    )
    line_chart.update_traces(line_width=3, marker_size=9)
    line_chart.update_layout(margin=dict(l=12, r=12, t=18, b=8), height=390, paper_bgcolor="#0b0b0b", plot_bgcolor="#111111", font_color="#f5f5f5", hovermode="x unified")
    line_chart.update_xaxes(showgrid=False, tickformat="%b %Y")
    line_chart.update_yaxes(showgrid=True, gridcolor="#333333", zeroline=False)
    st.plotly_chart(line_chart, use_container_width=True)

st.markdown('<div class="section-heading">More viewing insights</div>', unsafe_allow_html=True)
region_chart_column, device_chart_column = st.columns(2)

with region_chart_column:
    region_ratings = filtered.groupby("Region", as_index=False)["Rating"].sum()
    region_rating_chart = px.pie(
        region_ratings,
        names="Region",
        values="Rating",
        color_discrete_sequence=["#e50914", "#f5f5f5", "#b20710", "#777777", "#76000a"],
    )
    region_rating_chart.update_layout(margin=dict(l=12, r=12, t=18, b=8), height=350, paper_bgcolor="#0b0b0b", font_color="#f5f5f5")
    region_rating_chart.update_traces(textposition="inside", textinfo="percent+label", marker_line_color="#111111", marker_line_width=2)
    st.plotly_chart(region_rating_chart, use_container_width=True)

with device_chart_column:
    device_revenue = filtered.groupby("Device", as_index=False)["Monthly_Revenue"].sum()
    device_revenue_chart = px.line(
        device_revenue,
        x="Device",
        y="Monthly_Revenue",
        markers=True,
        labels={"Device": "Device", "Monthly_Revenue": "Revenue"},
        color_discrete_sequence=["#e50914"],
    )
    device_revenue_chart.update_traces(line_width=3, marker_size=9)
    device_revenue_chart.update_layout(margin=dict(l=12, r=12, t=18, b=8), height=350, paper_bgcolor="#0b0b0b", plot_bgcolor="#111111", font_color="#f5f5f5")
    device_revenue_chart.update_xaxes(showgrid=False)
    device_revenue_chart.update_yaxes(showgrid=True, gridcolor="#333333", zeroline=False)
    st.plotly_chart(device_revenue_chart, use_container_width=True)

rating_counts = filtered["Rating"].value_counts().sort_index().rename_axis("Rating").reset_index(name="Rating count")
rating_counts["Rating share (%)"] = rating_counts["Rating count"].div(rating_counts["Rating count"].sum()).mul(100)
rating_counts["Rating share label"] = rating_counts["Rating share (%)"].map(lambda share: f"{share:.1f}%")
rating_chart = px.bar(
    rating_counts,
    x="Rating",
    y="Rating count",
    text="Rating share label",
    hover_data=["Rating share (%)"],
    labels={"Rating": "Rating", "Rating count": "Number of ratings", "Rating share (%)": "Rating share"},
    color_discrete_sequence=["#e50914"],
)
rating_chart.update_layout(margin=dict(l=12, r=12, t=18, b=8), height=350, paper_bgcolor="#0b0b0b", plot_bgcolor="#111111", font_color="#f5f5f5")
rating_chart.update_traces(textposition="outside", cliponaxis=False)
rating_chart.update_xaxes(showgrid=False, dtick=1)
rating_chart.update_yaxes(showgrid=True, gridcolor="#333333", zeroline=False)
st.plotly_chart(rating_chart, use_container_width=True)

artwork_paths = [IMAGES_PATH / "image1.jfif", IMAGES_PATH / "image2.jfif"]
available_artwork = [path for path in artwork_paths if path.exists()]
if available_artwork:
    st.markdown('<div class="section-heading">Netflix artwork</div>', unsafe_allow_html=True)
    artwork_columns = st.columns(len(available_artwork))
    for artwork_column, artwork_path in zip(artwork_columns, available_artwork):
        artwork_column.image(str(artwork_path), width="stretch")

with st.expander("Browse filtered records"):
    st.caption(f"Showing {len(filtered):,} of {len(netflix):,} records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)