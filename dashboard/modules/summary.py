import streamlit as st


def show_summary(df):

    st.write("")

    # ---------------------------------------
    # Calculate Summary
    # ---------------------------------------

    total_logs = len(df)

    level_counts = df["level"].value_counts().to_dict()

    total_errors = level_counts.get("ERROR", 0)

    total_warnings = (
        level_counts.get("WARN", 0)
        + level_counts.get("WARNING", 0)
    )

    total_info = level_counts.get("INFO", 0)

    total_debug = level_counts.get("DEBUG", 0)

    total_trace = level_counts.get("TRACE", 0)

    # ---------------------------------------
    # Dashboard Cards
    # ---------------------------------------

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    cards = [

        {
            "title": "📄 Total Logs",
            "value": total_logs,
            "color": "#2563EB"
        },

        {
            "title": "❌ Errors",
            "value": total_errors,
            "color": "#DC2626"
        },

        {
            "title": "⚠️ Warnings",
            "value": total_warnings,
            "color": "#F59E0B"
        },

        {
            "title": "ℹ️ Info",
            "value": total_info,
            "color": "#3B82F6"
        },

        {
            "title": "🐞 Debug",
            "value": total_debug,
            "color": "#10B981"
        },

        {
            "title": "🔍 Trace",
            "value": total_trace,
            "color": "#6B7280"
        }

    ]

    columns = [col1, col2, col3, col4, col5, col6]

    for col, card in zip(columns, cards):

        with col:

            st.markdown(
                f"""
<div style="
background:white;
padding:18px;
border-radius:18px;
border-left:8px solid {card['color']};
box-shadow:0 4px 15px rgba(0,0,0,0.08);
text-align:center;
height:145px;
display:flex;
flex-direction:column;
justify-content:center;
">

<h4 style="
margin:0;
color:#374151;
font-size:20px;
">
{card['title']}
</h4>

<h1 style="
margin-top:18px;
margin-bottom:0;
font-size:40px;
font-weight:700;
color:{card['color']};
">
{card['value']}
</h1>

</div>
""",
                unsafe_allow_html=True
            )