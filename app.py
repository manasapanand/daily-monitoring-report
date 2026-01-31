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
    return sorted(set(re.findall(r"\{\{REMARK:([^}]+)\}\}", html)))

def extract_all_item_names_from_layout():
    """
    Extract Item Name column values from EMAIL_LAYOUT
    (3rd <td> in main table, 2nd <td> in Additional Checks)
    """
    item_names = []

    # --- Main checklist: 3rd <td> ---
    main_rows = re.findall(
        r"<tr>.*?<td>\d+</td>.*?<td>.*?</td>\s*<td>(.*?)</td>",
        EMAIL_LAYOUT,
        flags=re.DOTALL
    )

    # --- Additional checks: 2nd <td> ---
    additional_rows = re.findall(
        r"<b>Additional Checks</b>.*?<table.*?>(.*?)</table>",
        EMAIL_LAYOUT,
        flags=re.DOTALL
    )

    if additional_rows:
        item_names += re.findall(
            r"<tr>\s*<td>\d+</td>\s*<td>(.*?)</td>",
            additional_rows[0],
            flags=re.DOTALL
        )

    item_names = main_rows + item_names

    # Clean + preserve order
    cleaned = []
    for name in item_names:
        name = re.sub(r"<.*?>", "", name).strip()
        if name and name not in cleaned:
            cleaned.append(name)

    return cleaned


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
# MANUAL EDITING
# =====================================================
if "rows" in st.session_state:
    st.header("2️⃣ Edit Case / Status / Remarks")

    all_items = extract_all_item_names_from_layout()

    for key in all_items:
        # Ensure every checklist item exists
        if key not in st.session_state["rows"]:
            st.session_state["rows"][key] = {
                "case_no": "",
                "status": "PASS",
                "remarks": ""
            }

        row = st.session_state["rows"][key]

        with st.expander(key, expanded=False):
            row["case_no"] = st.text_input(
                "Case #",
                value=row["case_no"],
                key=f"case_{key}"
            )

            row["status"] = st.selectbox(
                "Status",
                ["PASS", "FAIL", "CHECKED", "-"],
                index=["PASS", "FAIL", "CHECKED", "-"].index(row["status"]),
                key=f"status_{key}"
            )

            row["remarks"] = st.text_area(
                "Remarks",
                value=row["remarks"],
                key=f"remarks_{key}"
            )


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

        # Detect missing placeholders
        missing = extract_missing_placeholders(html)
        st.session_state["missing_placeholders"] = missing

        if missing:
            st.warning("⚠️ Some placeholders were not filled. Fix them below.")
        else:
            st.success("HTML generated successfully.")


# =====================================================
# FIX MISSING PLACEHOLDERS
# =====================================================
if (
    "missing_placeholders" in st.session_state
    and st.session_state["missing_placeholders"]
):
    st.subheader("⚠️ Missing Fields (Manual Fix)")

    for key in st.session_state["missing_placeholders"]:
        if key not in st.session_state["rows"]:
            st.session_state["rows"][key] = {
                "case_no": "",
                "status": "PASS",
                "remarks": ""
            }

        st.session_state["rows"][key]["remarks"] = st.text_input(
            f"Missing remark for: {key}",
            value=st.session_state["rows"][key]["remarks"],
            key=f"missing_{key}"
        )

# =====================================================
# RELOAD PREVIEW AFTER MANUAL FIX
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
