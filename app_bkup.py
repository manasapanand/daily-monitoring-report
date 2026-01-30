import streamlit as st
from datetime import datetime
from report_engine import generate_remarks
from email_layout import EMAIL_LAYOUT

st.set_page_config(layout="wide")
st.title("📊 Daily Monitoring Report Builder")

# ================= FILE UPLOAD =================
st.header("1️⃣ Upload Input Excel Files")

simple_files = st.file_uploader(
    "Upload SIMPLE Excel files",
    type=["xlsx"],
    accept_multiple_files=True
)

time_series_file = st.file_uploader(
    "Upload TIME SERIES Excel",
    type=["xlsx"]
)

# ================= GENERATE =================
if st.button("🔄 Generate Auto Values"):
    if not simple_files:
        st.error("Please upload at least one SIMPLE Excel file.")
    else:
        remarks = generate_remarks(simple_files, time_series_file)
        st.session_state["remarks"] = remarks
        st.success("Auto values generated successfully.")

# ================= MANUAL OVERRIDE =================
if "remarks" in st.session_state:
    st.header("2️⃣ Edit / Override Values")

    updated = {}
    col1, col2 = st.columns(2)

    for i, (k, v) in enumerate(st.session_state["remarks"].items()):
        with col1 if i % 2 == 0 else col2:
            updated[k] = st.text_input(k, value=v)

    st.session_state["updated_remarks"] = updated

# ================= GENERATE HTML =================
if st.button("🧱 Generate HTML"):
    if "updated_remarks" not in st.session_state:
        st.error("Generate values first.")
    else:
        html = EMAIL_LAYOUT.replace(
            "{{CHECKLIST_DATE}}",
            datetime.now().strftime("%m/%d/%Y")
        )

        for k, v in st.session_state["updated_remarks"].items():
            html = html.replace(f"{{{{REMARK:{k}}}}}", v)

        st.session_state["html"] = html

        # ✅ PLACEHOLDER CHECK (ADD HERE)
        if "{{REMARK:" in html:
            st.warning("⚠️ Some placeholders were not filled. Please review the inputs.")

        st.success("HTML generated.")

# ================= PREVIEW & DOWNLOAD =================
if "html" in st.session_state:
    st.header("3️⃣ Preview & Download")

    st.components.v1.html(
        st.session_state["html"],
        height=700,
        scrolling=True
    )

    st.download_button(
        "⬇️ Download HTML",
        st.session_state["html"],
        file_name="Daily_Monitoring_Report.html",
        mime="text/html"
    )
