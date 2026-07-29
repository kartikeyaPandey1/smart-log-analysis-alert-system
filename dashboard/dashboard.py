import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st

from modules.summary import show_summary
from modules.alerts import show_alerts
from modules.charts import render_charts
from modules.recent_logs import show_recent_logs
from modules.dashboard_stats import show_dashboard_stats
from modules.analytics import show_analytics
from modules.ai_insights import show_ai_insights

from app.services.log_parser import parse_log_file


# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Smart Log Dashboard",
    layout="wide"
)

st.title("📊 Smart Log System Dashboard")

# ---------------------------------------
# Initialize Session State
# ---------------------------------------

if "parsed_df" not in st.session_state:
    st.session_state.parsed_df = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ---------------------------------------
# FILE UPLOAD
# ---------------------------------------

st.markdown("### 📂 Upload Spring Boot Log File")

uploaded_file = st.file_uploader(
    "Choose a .log or .txt file",
    type=["log", "txt"]
)

if uploaded_file is not None:

    st.success(f"Selected File: {uploaded_file.name}")

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button(
            "🚀 Analyze Logs",
            use_container_width=True
        ):

            with st.spinner("Analyzing log file..."):

                df = parse_log_file(uploaded_file)

            if df.empty:

                st.error("No valid log entries found.")
                st.stop()

            st.session_state.parsed_df = df
            st.session_state.file_name = uploaded_file.name

            # Reset pagination when a new file is analyzed
            st.session_state.page = 1

            st.rerun()

    with col2:

        if st.session_state.parsed_df is not None:

            if st.button(
                "🗑 Clear Analysis",
                use_container_width=True
            ):

                st.session_state.parsed_df = None
                st.session_state.file_name = None

                if "page" in st.session_state:
                    del st.session_state.page

                st.rerun()


# ---------------------------------------
# SHOW DASHBOARD
# ---------------------------------------

if st.session_state.parsed_df is not None:

    df = st.session_state.parsed_df

    st.success(
        f"Showing analysis for: **{st.session_state.file_name}**"
    )

    st.success(
        f"Successfully parsed **{len(df)}** log entries."
    )

    st.subheader("Parsed Log Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    # ---------------------------------------
    # SUMMARY
    # ---------------------------------------

    show_summary(df)

    # ---------------------------------------
    # ALERTS
    # ---------------------------------------

    show_alerts(df)

    # ---------------------------------------
    # CHARTS
    # ---------------------------------------

    render_charts(df)

    # ---------------------------------------
    # RECENT LOGS
    # ---------------------------------------

    filtered_df = show_recent_logs(df)

    # ---------------------------------------
    # DASHBOARD STATS
    # ---------------------------------------

    show_dashboard_stats(filtered_df)

    # ---------------------------------------
    # ANALYTICS
    # ---------------------------------------

    show_analytics(filtered_df)

    # ---------------------------------------
    # AI INSIGHTS
    # ---------------------------------------

    show_ai_insights(filtered_df)

elif uploaded_file is None:

    st.info("👆 Upload a Spring Boot log file to begin analysis.")