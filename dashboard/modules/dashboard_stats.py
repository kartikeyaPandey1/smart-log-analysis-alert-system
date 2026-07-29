import streamlit as st


def show_dashboard_stats(df):

    st.markdown("---")
    st.subheader("📈 Dashboard Statistics")

    if df.empty:
        st.info("No statistics available.")
        return

    # ---------------------------------------
    # Calculate Statistics
    # ---------------------------------------

    total_logs = len(df)

    total_errors = (
        df["level"] == "ERROR"
    ).sum()

    total_services = df["logger"].nunique()

    avg_logs = (
        round(total_logs / total_services, 2)
        if total_services else 0
    )

    # ---------------------------------------
    # Most Active Service
    # ---------------------------------------

    most_active_service = (
        df["logger"]
        .value_counts()
        .idxmax()
        .split(".")[-1]
    )

    # ---------------------------------------
    # Most Frequent Error
    # ---------------------------------------

    error_df = df[df["level"] == "ERROR"]

    if not error_df.empty:

        most_common_error = (
            error_df["message"]
            .value_counts()
            .idxmax()
        )

        if len(most_common_error) > 60:
            most_common_error = (
                most_common_error[:60] + "..."
            )

    else:

        most_common_error = "No errors detected"

    # ---------------------------------------
    # Active Alerts
    # ---------------------------------------

    active_alerts = total_errors

    # ---------------------------------------
    # Card Data
    # ---------------------------------------

    cards = [

        {
            "title": "🖥 Total Services",
            "value": total_services,
            "color": "#2563EB"
        },

        {
            "title": "🔥 Most Active Service",
            "value": most_active_service,
            "color": "#10B981"
        },

        {
            "title": "📊 Avg Logs / Service",
            "value": avg_logs,
            "color": "#7C3AED"
        },

        {
            "title": "❌ Total Errors",
            "value": total_errors,
            "color": "#DC2626"
        },

        {
            "title": "🚨 Active Alerts",
            "value": active_alerts,
            "color": "#F59E0B"
        },

        {
            "title": "📌 Most Frequent Error",
            "value": most_common_error,
            "color": "#3B82F6"
        }

    ]

    # ---------------------------------------
    # Layout
    # ---------------------------------------

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    columns = [
        col1, col2, col3,
        col4, col5, col6
    ]

    for col, card in zip(columns, cards):

        with col:

            st.markdown(
                f"""
<div style="
background:white;
padding:18px;
border-radius:16px;
border-left:8px solid {card['color']};
box-shadow:0 4px 15px rgba(0,0,0,0.08);
height:165px;
display:flex;
flex-direction:column;
justify-content:center;
margin-bottom:20px;
">

<h4 style="
margin:0;
font-size:19px;
color:#374151;
text-align:center;
">
{card['title']}
</h4>

<div style="
margin-top:16px;
font-size:28px;
font-weight:700;
color:{card['color']};
text-align:center;
word-break:break-word;
">
{card['value']}
</div>

</div>
""",
                unsafe_allow_html=True
            )