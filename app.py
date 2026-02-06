import streamlit as st
import re
from datetime import datetime
from report_engine import generate_remarks
from email_layout import EMAIL_LAYOUT

st.set_page_config(layout="wide")
st.title("📊 Daily Monitoring Report Builder")


# =====================================================
# Helpers
# =====================================================
def extract_missing_placeholders(html: str):
    """
    Extract all unresolved {{REMARK:Item Name}} placeholders
    """
    return sorted(set(re.findall(r"\{\{REMARK:([^}]+)\}\}", html)))


def is_not_executed(val) -> bool:
    """
    True only if remarks == 'Not executed' (case-insensitive)
    """
    if not isinstance(val, str):
        return False
    return val.strip().lower() == "not executed"


# =====================================================
# FILE UPLOAD
# =====================================================
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

# =====================================================
# GENERATE AUTO VALUES
# =====================================================
if st.button("🔄 Generate Auto Values"):
    if not simple_files:
        st.error("Please upload at least one SIMPLE Excel file.")
    else:
        # report_engine is the single source of truth
        remarks = generate_remarks(simple_files, time_series_file)

        rows = {}
        for key, value in remarks.items():
            rows[key] = {
                "case_no": "",
                "status": "PASS",
                "remarks": value
            }

        st.session_state["rows"] = rows
        st.success("Auto values generated successfully.")

# =====================================================
# HTML BUILDER
# =====================================================
def build_html_from_rows(rows):
    html = EMAIL_LAYOUT.replace(
        "{{CHECKLIST_DATE}}",
        datetime.now().strftime("%m/%d/%Y")
    )

    for key, row in rows.items():
        html = html.replace(f"{{{{REMARK:{key}}}}}", row["remarks"])
        html = html.replace(f"{{{{STATUS:{key}}}}}", row["status"])
        html = html.replace(f"{{{{CASE:{key}}}}}", row["case_no"])

    return html


# =====================================================
# GENERATE HTML
# =====================================================
if st.button("🧱 Generate HTML"):
    if "rows" not in st.session_state:
        st.error("Generate values first.")
    else:
        html = build_html_from_rows(st.session_state["rows"])
        st.session_state["html"] = html

        missing = extract_missing_placeholders(html)
        st.session_state["missing_placeholders"] = missing

        if missing:
            st.warning("⚠️ Some placeholders were not filled. Fix them below.")
        else:
            st.success("HTML generated successfully.")


# =====================================================
# FIX MISSING PLACEHOLDERS (ONLY THESE + RFI Logs)
# =====================================================
if "rows" in st.session_state:
    st.subheader("⚠️ Missing Fields (Manual Fix)")

    keys_to_fix = set(st.session_state.get("missing_placeholders", []))
    keys_to_fix.add("RFI Logs")

    for key in sorted(keys_to_fix):
        if key not in st.session_state["rows"]:
            st.session_state["rows"][key] = {
                "case_no": "",
                "status": "PASS",
                "remarks": ""
            }

        st.session_state["rows"][key]["remarks"] = st.text_input(
            f"Remark for: {key}",
            value=st.session_state["rows"][key]["remarks"],
            key=f"missing_{key}"
        )


# =====================================================
# RELOAD PREVIEW
# =====================================================
if "rows" in st.session_state and st.button("🔁 Reload Preview"):
    st.session_state["html"] = build_html_from_rows(st.session_state["rows"])

    missing = extract_missing_placeholders(st.session_state["html"])
    st.session_state["missing_placeholders"] = missing

    if missing:
        st.warning("⚠️ Some placeholders are still missing.")
    else:
        st.success("Preview refreshed with latest updates.")


# =====================================================
# PREVIEW & DOWNLOAD
# =====================================================
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
