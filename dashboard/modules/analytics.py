import streamlit as st
import plotly.express as px
import pandas as pd


def show_analytics(df):

    st.markdown("---")
    st.subheader("📈 Log Analytics")

    if df.empty:
        st.info("No analytics available.")
        return

    # ---------------------------------------
    # Prepare Data
    # ---------------------------------------

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ---------------------------------------
    # Error Trend
    # ---------------------------------------

    error_df = df[df["level"] == "ERROR"].copy()

    error_df["date"] = error_df["timestamp"].dt.date

    error_trend = (
        error_df.groupby("date")
        .size()
        .reset_index(name="Errors")
    )

    # ---------------------------------------
    # Severity Distribution
    # ---------------------------------------

    severity_data = (
        df["level"]
        .value_counts()
        .reset_index()
    )

    severity_data.columns = [
        "Level",
        "Count"
    ]

    color_map = {
        "ERROR": "#DC2626",
        "WARN": "#F59E0B",
        "WARNING": "#F59E0B",
        "INFO": "#3B82F6",
        "DEBUG": "#10B981",
        "TRACE": "#6B7280"
    }

    # ---------------------------------------
    # Top Error Messages
    # ---------------------------------------

    top_errors = (
        error_df["message"]
        .value_counts()
        .reset_index()
    )

    if not top_errors.empty:

        top_errors.columns = [
            "Error Message",
            "Count"
        ]

        top_errors["Short Message"] = top_errors[
            "Error Message"
        ].apply(
            lambda x: x[:55] + "..."
            if len(x) > 55
            else x
        )

    # =======================================
    # FIRST ROW
    # =======================================

    col1, col2 = st.columns(2)

    # ---------------------------------------
    # Error Trend
    # ---------------------------------------

    with col1:

        st.subheader("📈 Error Trend")

        if not error_trend.empty:

            if len(error_trend) == 1:

                fig1 = px.bar(
                    error_trend,
                    x="date",
                    y="Errors",
                    text="Errors",
                    color_discrete_sequence=["#DC2626"]
                )

                fig1.update_traces(
                    textposition="outside"
                )

            else:

                fig1 = px.line(
                    error_trend,
                    x="date",
                    y="Errors",
                    markers=True
                )

                fig1.update_traces(
                    line_color="#DC2626"
                )

            fig1.update_layout(
                height=420,
                template="plotly_white",
                showlegend=False,
                xaxis_title="Date",
                yaxis_title="Errors"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        else:

            st.info("No error logs found.")

    # ---------------------------------------
    # Severity Distribution
    # ---------------------------------------

    with col2:

        st.subheader("📊 Severity Distribution")

        fig2 = px.bar(
            severity_data,
            x="Level",
            y="Count",
            text="Count",
            color="Level",
            color_discrete_map=color_map
        )

        fig2.update_traces(
            textposition="outside"
        )

        fig2.update_layout(
            height=420,
            template="plotly_white",
            showlegend=False
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =======================================
    # SECOND ROW
    # =======================================

    st.markdown("---")

    st.subheader("📌 Top Error Messages")

    if not top_errors.empty:

        fig3 = px.bar(
            top_errors,
            x="Count",
            y="Short Message",
            orientation="h",
            text="Count"
        )

        fig3.update_traces(
            marker_color="#DC2626",
            textposition="outside",
            customdata=top_errors["Error Message"],
            hovertemplate="<b>%{customdata}</b><br>Count: %{x}<extra></extra>"
        )

        fig3.update_layout(
            height=420,
            template="plotly_white",
            yaxis=dict(autorange="reversed"),
            xaxis_title="Occurrences",
            yaxis_title=""
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    else:

        st.success("✅ No error messages found.")

    # =======================================
    # ANALYTICS SUMMARY
    # =======================================

    st.markdown("---")
    st.subheader("📝 Analytics Summary")

    total_logs = len(df)

    total_errors = len(df[df["level"] == "ERROR"])

    debug_logs = len(df[df["level"] == "DEBUG"])

    debug_percent = (
        round((debug_logs / total_logs) * 100, 1)
        if total_logs else 0
    )

    top_service = (
        df["logger"]
        .value_counts()
        .idxmax()
        .split(".")[-1]
    )

    if total_errors == 0:
        health = "🟢 Application is healthy. No errors detected."

    elif total_errors <= 3:
        health = "🟡 Only a few errors detected. Overall application appears stable."

    else:
        health = "🔴 Multiple errors detected. Investigation is recommended."

    st.markdown(
        f"""
<div style="
background:white;
padding:22px;
border-radius:16px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);
">

<ul style="font-size:17px;line-height:2;">

<li><b>Total Log Entries:</b> {total_logs}</li>

<li><b>DEBUG Logs:</b> {debug_percent}% of all logs.</li>

<li><b>Most Active Service:</b> {top_service}</li>

<li><b>Total Errors:</b> {total_errors}</li>

<li><b>Overall Health:</b> {health}</li>

</ul>

</div>
""",
        unsafe_allow_html=True
    )