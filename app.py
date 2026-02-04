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

    main_rows = re.findall(
        r"<tr>.*?<td>\d+</td>.*?<td>.*?</td>\s*<td>(.*?)</td>",
        EMAIL_LAYOUT,
        flags=re.DOTALL
    )

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

    cleaned = []
    for name in item_names:
        name = re.sub(r"<.*?>", "", name).strip()
        if name and name not in cleaned:
            cleaned.append(name)

    return cleaned


def reformat_time_series_value(label: str, value: str) -> str:
    """
    Keep time series AS-IS but normalize format to:
    Category | DD/MM/YY | Count
    """
    lines = value.split("<br>")
    out = []

    for line in lines:
        if "---" not in line:
            out.append(line)
            continue

        date_part, count_part = [x.strip() for x in line.split("---", 1)]

        try:
            dt = datetime.strptime(date_part, "%d/%m/%Y")
            date_part = dt.strftime("%d/%m/%y")
        except Exception:
            pass

        out.append(f"{label} | {date_part} | {count_part}")

    return "<br>".join(out)


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

        TIME_SERIES_LABEL_MAP = {
            "Count Of Campaign Email sent": "Campaign Email Sent",
            "Count Of Campaign SMS sent": "Campaign SMS Sent",
            "Count of Attempts": "Attempts",
            "Count of one-to-one SMS sent": "One-to-One SMS Sent",
            "Count of Interactions": "Interactions",
            "Count of Leads": "Leads",
        }

        rows = {}
        for key, value in remarks.items():
            if key in TIME_SERIES_LABEL_MAP:
                value = reformat_time_series_value(
                    TIME_SERIES_LABEL_MAP[key],
                    value
                )

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
        if key not in st.session_state["rows"]:
            st.session_state["rows"][key] = {
                "case_no": "",
                "status": "PASS",
                "remarks": ""
            }

        row = st.session_state["rows"][key]

        # 🚫 Skip items explicitly marked as "not executed"
        if isinstance(row["remarks"], str) and "not executed" in row["remarks"].lower():
            continue

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


# =====================================================
# HTML BUILDER
# =====================================================
def build_html_from_rows(rows):
    html = EMAIL_LAYOUT.replace(
        "{{CHECKLIST_DATE}}",
        datetime.now().strftime("%d/%m/%Y")
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
# FIX MISSING PLACEHOLDERS (RFI Logs always included)
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
            f"Missing remark for: {key}",
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
