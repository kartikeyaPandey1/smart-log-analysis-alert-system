import streamlit as st
import plotly.express as px


def render_charts(df):

    if df.empty:
        st.info("No data available for charts.")
        return

    # ---------------------------------------
    # Prepare Log Level Data
    # ---------------------------------------

    log_levels = (
        df["level"]
        .value_counts()
        .reset_index()
    )

    log_levels.columns = [
        "level",
        "count"
    ]

    # Consistent colors used across dashboard
    color_map = {
        "ERROR": "#DC2626",
        "WARN": "#F59E0B",
        "WARNING": "#F59E0B",
        "INFO": "#3B82F6",
        "DEBUG": "#10B981",
        "TRACE": "#6B7280"
    }

    # ---------------------------------------
    # Prepare Service Data
    # ---------------------------------------

    services = (
        df["logger"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    services.columns = [
        "full_service",
        "count"
    ]

    # Keep full logger for hover, show short class name on axis
    services["service"] = services["full_service"].apply(
        lambda x: x.split(".")[-1]
    )

    # ---------------------------------------
    # Charts
    # ---------------------------------------

    col1, col2 = st.columns(2)

    # ---------------------------------------
    # Pie Chart
    # ---------------------------------------

    with col1:

        st.subheader("🥧 Log Level Distribution")

        fig1 = px.pie(
            log_levels,
            names="level",
            values="count",
            hole=0.45,
            color="level",
            color_discrete_map=color_map
        )

        fig1.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Logs: %{value}<br>Percentage: %{percent}<extra></extra>"
        )

        fig1.update_layout(
            height=430,
            legend_title="Log Level",
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # ---------------------------------------
    # Top Services
    # ---------------------------------------

    with col2:

        st.subheader("📦 Top 10 Services")

        fig2 = px.bar(
            services,
            x="count",
            y="service",
            orientation="h",
            text="count"
        )

        fig2.update_traces(
            textposition="outside",
            marker_color="#3B82F6",
            hovertemplate=(
                "<b>%{customdata}</b>"
                "<br>Logs: %{x}"
                "<extra></extra>"
            ),
            customdata=services["full_service"]
        )

        fig2.update_layout(
            height=430,
            yaxis=dict(
                autorange="reversed",
                title=""
            ),
            xaxis_title="Number of Logs",
            margin=dict(l=10, r=20, t=40, b=10)
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )