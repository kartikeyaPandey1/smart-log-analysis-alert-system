import streamlit as st


def show_ai_insights(df):

    st.markdown("---")
    st.subheader("🧠 Intelligent Log Analysis")

    if df.empty:
        st.info("No insights available.")
        return

    # ---------------------------------------
    # Basic Statistics
    # ---------------------------------------

    total_logs = len(df)

    total_errors = len(
        df[df["level"] == "ERROR"]
    )

    total_warnings = len(
        df[
            (df["level"] == "WARN") |
            (df["level"] == "WARNING")
        ]
    )

    debug_logs = len(
        df[df["level"] == "DEBUG"]
    )

    debug_percent = round(
        (debug_logs / total_logs) * 100,
        1
    ) if total_logs else 0

    # ---------------------------------------
    # Most Active Service
    # ---------------------------------------

    top_service = (
        df["logger"]
        .value_counts()
        .idxmax()
        .split(".")[-1]
    )

    # ---------------------------------------
    # Latest Error
    # ---------------------------------------

    error_df = df[
        df["level"] == "ERROR"
    ]

    latest_error = "No ERROR logs detected."

    if not error_df.empty:

        latest_error = (
            error_df.iloc[-1]["message"]
        )

        if len(latest_error) > 90:

            latest_error = latest_error[:90] + "..."

    # ---------------------------------------
    # Overall Health
    # ---------------------------------------

    if total_errors == 0:

        health = (
            "Application appears healthy. "
            "No ERROR logs were detected."
        )

    elif total_errors <= 3:

        health = (
            "Application appears stable. "
            "Only a few isolated errors were detected."
        )

    else:

        health = (
            "Application requires attention. "
            "Multiple ERROR logs were detected."
        )

    # ---------------------------------------
    # Recommendations
    # ---------------------------------------

    recommendations = []

    if total_errors > 0:

        recommendations.append(
            "Review the recent ERROR logs."
        )

    if total_warnings > 0:

        recommendations.append(
            "Inspect WARN logs during routine maintenance."
        )

    if debug_percent > 50:

        recommendations.append(
            "Reduce DEBUG logging before deploying to production."
        )

    recommendations.append(
        "Continue monitoring application activity."
    )

    # ---------------------------------------
    # Display Report
    # ---------------------------------------

    st.markdown(
        f"""
<div style="
background:white;
padding:18px;
border:1px solid #E5E7EB;
border-radius:12px;
box-shadow:0 2px 8px rgba(0,0,0,0.05);
">

<h4>Overall Health</h4>

<p>
{health}
</p>

<hr>

<h4>Logging Behaviour</h4>

<p>
{debug_percent}% of the uploaded logs are DEBUG logs.
</p>

<p>
<b>Recommendation:</b>
Consider switching to INFO level before production to reduce unnecessary log volume.
</p>

<hr>

<h4>Service Analysis</h4>

<p>
<b>Most Active Service:</b>
{top_service}
</p>

<p>
This service generated the highest number of log entries in the uploaded log file.
</p>

<hr>

<h4>Error Analysis</h4>

<p>
<b>Latest Error:</b>
</p>

<p>
{latest_error}
</p>

<hr>

<h4>Recommended Actions</h4>

<ul>
{''.join(f"<li>{item}</li>" for item in recommendations)}
</ul>

</div>
""",
        unsafe_allow_html=True
    )