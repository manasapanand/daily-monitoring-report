import re
import pandas as pd
from datetime import datetime

# =====================================================
# HELPERS (UNCHANGED LOGIC)
# =====================================================
def normalize_desc(text: str) -> str:
    if not text or str(text).lower() == "nan":
        return ""

    txt = str(text).strip()

    # 🔑 NORMALIZE DASH CHARACTERS (CRITICAL FIX)
    txt = txt.replace("–", "-").replace("—", "-")

    txt = re.sub(r"^\d+\s*[-.]\s*", "", txt)
    txt = re.sub(r"\(.*?\)", "", txt)
    txt = re.sub(r"\s*-\s*$", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()

    low = txt.lower()

    # ----- DNC -----
    if "dncimportstagingtable" in low:
        return "DNCImportStagingTable"

    if "dncimportbatchnumbers" in low:
        return "DNCImportBatchNumbers"

    # ----- Archiving -----
    if "archiving of attempt" in low:
        return "Archiving of Attempt - tlArchive" if "archive" in low else "Archiving of Attempt - tlMain"

    if "archiving of lead" in low:
        return "Archiving of Lead - tlArchive" if "archive" in low else "Archiving of Lead - tlMain"

    if "archiving of interaction" in low:
        return "Archiving of Interaction - tlArchive" if "archive" in low else "Archiving of Interaction - tlMain"

    # ----- Existing -----
    if "interaction created" in low:
        return "Last Interaction"

    if "attachment received" in low:
        return "Last Attachment received"

    if "campaign mailer sent" in low:
        return "Last Campaign Mailer Sent"

    if "lead promoted" in low:
        return "Last Lead promoted"

    return txt


def format_datetime(val: str) -> str:
    try:
        val = str(val).strip()
        dt = pd.to_datetime(val, dayfirst=True)
        return dt.strftime("%m/%d/%Y %I:%M %p")
    except Exception:
        return str(val)


# =====================================================
# CORE ENGINE (PURE FUNCTION)
# =====================================================
def generate_remarks(simple_excels, time_series_excel=None):
    """
    simple_excels: list of file paths OR file-like objects
    time_series_excel: file path OR file-like object

    returns: dict[str, str]
    """
    remarks: dict[str, str] = {}

    # ---------- SIMPLE FILES ----------
    for file in simple_excels:
        df = pd.read_excel(file)

        for _, r in df.iterrows():
            key = normalize_desc(r.get("Description", ""))

            raw_val = (
                r.get("Value")
                if "Value" in r
                else r.get("ResultValue")
                if "ResultValue" in r
                else r.get("Count")
            )

            if pd.isna(raw_val) or str(raw_val).strip() == "":
                continue

            val = format_datetime(raw_val)

            if key:
                remarks[key] = val

    # ---------- TIME SERIES ----------
    if time_series_excel:
        df_ts = pd.read_excel(time_series_excel)
        df_ts["Category"] = df_ts["Category"].str.replace(r"^\d+\.\s*", "", regex=True)

        TIME_SERIES_MAP = {
            "Campaign Email Sent": "Count Of Campaign Email sent",
            "Campaign SMS Sent": "Count Of Campaign SMS sent",
            "Attempts": "Count of Attempts",
            "One-to-One SMS Sent": "Count of one-to-one SMS sent",
            "Interactions": "Count of Interactions",
            "Leads": "Count of Leads",
        }

        for category, grp in df_ts.groupby("Category"):
            grp["Date"] = pd.to_datetime(grp["Date"], dayfirst=True)
            grp = grp.sort_values("Date")

            lines = [
                f"{row['Date'].strftime('%m/%d/%Y')} --- {row['Count']}"
                for _, row in grp.iterrows()
            ]

            remarks[TIME_SERIES_MAP[category]] = "<br>".join(lines)

    return remarks
