import streamlit as st
import pandas as pd


def show_recent_logs(df):

    st.write("")
    st.write("")
    st.subheader("📋 Recent Logs")

    # ---------------------------------------
    # Check Data
    # ---------------------------------------

    if df.empty:
        st.info("No logs found.")
        return pd.DataFrame()

    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ---------------------------------------
    # Filters
    # ---------------------------------------

    service_options = ["All"] + sorted(
        df["logger"].dropna().unique().tolist()
    )

    level_options = ["All"] + sorted(
        df["level"].dropna().unique().tolist()
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        selected_service = st.selectbox(
            "Filter by Service",
            service_options
        )

    with col2:
        selected_level = st.selectbox(
            "Filter by Level",
            level_options
        )

    with col3:
        search_text = st.text_input(
            "🔍 Search Message"
        )

    with col4:
        start_date = st.date_input(
            "📅 Start Date",
            value=None
        )

    with col5:
        end_date = st.date_input(
            "📅 End Date",
            value=None
        )

    # ---------------------------------------
    # Apply Filters
    # ---------------------------------------

    filtered_df = df.copy()

    if selected_service != "All":
        filtered_df = filtered_df[
            filtered_df["logger"] == selected_service
        ]

    if selected_level != "All":
        filtered_df = filtered_df[
            filtered_df["level"] == selected_level
        ]

    if search_text:
        filtered_df = filtered_df[
            filtered_df["message"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if start_date:
        filtered_df = filtered_df[
            filtered_df["timestamp"].dt.date >= start_date
        ]

    if end_date:
        filtered_df = filtered_df[
            filtered_df["timestamp"].dt.date <= end_date
        ]

    # ---------------------------------------
    # Display Data
    # ---------------------------------------

    display_df = filtered_df.copy()

    display_df["Time"] = display_df["timestamp"].dt.strftime(
        "%d %b %Y %H:%M"
    )

    display_df = display_df.rename(
        columns={
            "logger": "Service",
            "level": "Level",
            "message": "Message"
        }
    )

    display_df = display_df[
        [
            "Time",
            "Service",
            "Level",
            "Message"
        ]
    ]

    # ---------------------------------------
    # Export CSV
    # ---------------------------------------

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇ Export Filtered Logs as CSV",
        csv,
        "filtered_logs.csv",
        "text/csv"
    )

    # ---------------------------------------
    # Pagination
    # ---------------------------------------

    st.write("")

    total_rows = len(display_df)

    rows_col, info_col = st.columns([1, 3])

    with rows_col:
        rows_per_page = st.selectbox(
            "Rows per page",
            [10, 20, 50, 100],
            index=1
        )

    total_pages = max(
        (total_rows - 1) // rows_per_page + 1,
        1
    )

    if "page" not in st.session_state:
        st.session_state.page = 1

    if st.session_state.page > total_pages:
        st.session_state.page = total_pages

    start_idx = (st.session_state.page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    with info_col:
        st.markdown(
            f"""
            <div style="padding-top:28px;">
            Showing <b>{start_idx + 1}</b>–
            <b>{min(end_idx,total_rows)}</b>
            of <b>{total_rows}</b> logs
            </div>
            """,
            unsafe_allow_html=True
        )

    paginated_df = display_df.iloc[start_idx:end_idx]

    # ---------------------------------------
    # Styling
    # ---------------------------------------

    def color_level(value):

        if value == "ERROR":
            return "background-color:#FEE2E2;color:#DC2626;font-weight:bold;"

        elif value in ["WARN", "WARNING"]:
            return "background-color:#FEF3C7;color:#B45309;font-weight:bold;"

        elif value == "INFO":
            return "background-color:#DBEAFE;color:#2563EB;font-weight:bold;"

        return ""

    styled_df = paginated_df.style.map(
        color_level,
        subset=["Level"]
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------
    # Previous / Next Navigation
    # ---------------------------------------

    prev_col, page_col, next_col = st.columns([1, 2, 1])

    with prev_col:

        if st.button(
            "⬅ Previous",
            disabled=st.session_state.page == 1
        ):
            st.session_state.page -= 1
            st.rerun()

    with page_col:

        st.markdown(
            f"<div style='text-align:center;padding-top:8px;'>"
            f"<b>Page {st.session_state.page} of {total_pages}</b>"
            f"</div>",
            unsafe_allow_html=True
        )

    with next_col:

        if st.button(
            "Next ➡",
            disabled=st.session_state.page == total_pages
        ):
            st.session_state.page += 1
            st.rerun()

    # Return filtered dataframe (not paginated)
    return filtered_df