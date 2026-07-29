import streamlit as st


def show_alerts(df):

    st.write("")
    st.subheader("🚨 Active Alerts")

    if df.empty:
        st.success("✅ No Active Alerts")
        return

    # ---------------------------------------
    # Get Error Logs
    # ---------------------------------------

    error_df = df[df["level"] == "ERROR"]

    if error_df.empty:
        st.success("✅ No Active Alerts")
        return

    # ---------------------------------------
    # Count Errors by Service
    # ---------------------------------------

    service_errors = (
        error_df.groupby("logger")
        .size()
        .reset_index(name="error_count")
        .sort_values(by="error_count", ascending=False)
    )

    # ---------------------------------------
    # Severity Config
    # ---------------------------------------

    severity_config = {
        "HIGH": {
            "color": "#DC2626",
            "icon": "🔴",
            "message": "A high number of errors were detected. Immediate investigation is recommended.",
            "recommendation": "Review application logs and resolve the root cause as soon as possible."
        },
        "MEDIUM": {
            "color": "#F59E0B",
            "icon": "🟡",
            "message": "Multiple errors were detected. This could indicate a recurring issue.",
            "recommendation": "Monitor this service closely and investigate recent failures."
        },
        "LOW": {
            "color": "#10B981",
            "icon": "🟢",
            "message": "Only a small number of errors were detected. This appears to be an isolated issue.",
            "recommendation": "Continue monitoring. No immediate action is required."
        }
    }

    # ---------------------------------------
    # Display Alerts
    # ---------------------------------------

    for _, row in service_errors.iterrows():

        count = int(row["error_count"])

        if count >= 10:
            severity = "HIGH"
        elif count >= 5:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        config = severity_config[severity]

        # Show only class name instead of full package
        service_name = row["logger"].split(".")[-1]

        st.markdown(
            f"""
<div style="
background:white;
padding:22px;
margin-bottom:18px;
border-left:8px solid {config['color']};
border-radius:16px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);
">

<h3 style="margin:0;color:{config['color']};">
{config['icon']} {severity} ALERT
</h3>

<hr style="margin:12px 0;">

<p style="margin-bottom:8px;">
<b>📦 Service:</b> {service_name}
</p>

<p style="margin-bottom:8px;">
<b>📈 Error Count:</b> {count}
</p>

<p style="margin-bottom:8px;">
<b>📝 Assessment:</b><br>
{config['message']}
</p>

<p style="margin-bottom:0;">
<b>💡 Recommendation:</b><br>
{config['recommendation']}
</p>

</div>
""",
            unsafe_allow_html=True
        )