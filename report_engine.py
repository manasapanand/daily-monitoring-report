import re
import pandas as pd
from typing import List, Dict, Union, IO


# =====================================================
# HELPERS (LOGIC UNCHANGED)
# =====================================================
def normalize_desc(text: str) -> str:
    """
    Normalize Excel Description → canonical Item Name
    """
    if not text or str(text).lower() == "nan":
        return ""

    txt = str(text).strip()

    # Normalize Unicode dashes (CRITICAL)
    txt = txt.replace("–", "-").replace("—", "-")

    txt = re.sub(r"^\d+\s*[-.]\s*", "", txt)   # remove numbering
    txt = re.sub(r"\(.*?\)", "", txt)          # remove brackets
    txt = re.sub(r"\s*-\s*$", "", txt)          # remove trailing hyphen
    txt = re.sub(r"\s+", " ", txt).strip()     # normalize spaces

    low = txt.lower()

    # ----- DNC -----
    if "dncimportstagingtable" in low:
        return "DNCImportStagingTable"

    if "dncimportbatchnumbers" in low:
        return "DNCImportBatchNumbers"

    # ----- Archiving (tlMain vs tlArchive) -----
    if "archiving of attempt" in low:
        if "archive" in low:
            return "Archiving of Attempt - tlArchive"
        return "Archiving of Attempt – tlMain"   # EN DASH (locked)

    if "archiving of lead" in low:
        if "archive" in low:
            return "Archiving of Lead - tlArchive"
        return "Archiving of Lead - tlMain"

    if "archiving of interaction" in low:
        if "archive" in low:
            return "Archiving of Interaction - tlArchive"
        return "Archiving of Interaction - tlMain"

    # ----- Existing -----
    if "interaction created" in low:
        return "Last Interaction"

    if "attachment received" in low:
        return "Last Attachment received"

    if "campaign mailer sent" in low:
        return "Last Campaign Mailer Sent"

    if "lead promoted" in low:
        return "Last Lead promoted"

    if "incoming from cns" in low:
        return "Last Incoming from CNS"

    return txt


def _is_numeric_value(val) -> bool:
    """
    True when value is a pure numeric count (not datetime).
    """
    if isinstance(val, bool):
        return False
    if isinstance(val, (int, float)):
        return True
    if isinstance(val, str):
        txt = val.strip().replace(",", "")
        if txt == "":
            return False
        return bool(re.fullmatch(r"-?\d+(\.\d+)?", txt))
    return False


def _format_numeric(val) -> str:
    """
    Keep integer-like values clean (e.g., 5663 not 5663.0).
    """
    try:
        num = float(str(val).strip().replace(",", ""))
        if num.is_integer():
            return str(int(num))
        return str(num)
    except Exception:
        return str(val).strip()


def _looks_like_datetime(raw: str) -> bool:
    """
    Detect datetime-like strings so we can normalize formatting.
    """
    txt = raw.strip()
    if txt == "":
        return False

    patterns = [
        r"^\d{1,2}/\d{1,2}/\d{2,4}(\s+\d{1,2}:\d{2}(:\d{2})?\s*([APMapm]{2})?)?$",
        r"^\d{4}-\d{2}-\d{2}(\s+\d{1,2}:\d{2}(:\d{2})?)?$",
    ]
    return any(re.fullmatch(p, txt) for p in patterns)


def format_remark_value(key: str, val) -> str:
    """
    Format remarks safely:
    - Preserve numeric counts as numbers
    - Parse datetime-like fields using day-first input
    - Output datetime as MM/DD/YYYY HH:MM AM/PM
    """
    if _is_numeric_value(val):
        return _format_numeric(val)

    raw = str(val).strip()
    if raw == "":
        return raw

    # Keep explicit non-values untouched.
    if raw.upper() == "NULL":
        return raw

    # Parse date/times for known timestamp fields or datetime-like values.
    is_datetime_field = key.lower().startswith("last ") or _looks_like_datetime(raw)
    if is_datetime_field:
        try:
            if re.fullmatch(r"^\d{4}-\d{2}-\d{2}(\s+\d{1,2}:\d{2}(:\d{2})?)?$", raw):
                dt = pd.to_datetime(raw, dayfirst=False)
            else:
                dt = pd.to_datetime(raw, dayfirst=True)
            return dt.strftime("%m/%d/%Y %I:%M %p")
        except Exception:
            return raw

    return raw


# =====================================================
# CORE ENGINE (PURE FUNCTION)
# =====================================================
def generate_remarks(
    simple_excels: List[Union[str, IO]],
    time_series_excel: Union[str, IO, None] = None
) -> Dict[str, str]:
    """
    Generates remark values from input Excel files.
    """
    remarks: Dict[str, str] = {}

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

            if key:
                remarks[key] = format_remark_value(key, raw_val)

    # ---------- TIME SERIES ----------
    if time_series_excel:
        df_ts = pd.read_excel(time_series_excel)

        df_ts["Category"] = df_ts["Category"].str.replace(
            r"^\d+\.\s*", "", regex=True
        )

        TIME_SERIES_MAP = {
            "Campaign Email Sent": "Count Of Campaign Email sent",
            "Campaign SMS Sent": "Count Of Campaign SMS sent",
            "Attempts": "Count of Attempts",
            "One-to-One SMS Sent": "Count of one-to-one SMS sent",
            "Interactions": "Count of Interactions",
            "Leads": "Count of Leads",
        }

        for category, grp in df_ts.groupby("Category"):
            grp["Date"] = pd.to_datetime(grp["Date"], dayfirst=False)
            grp = grp.sort_values("Date")

            lines = [
                f"{row['Date'].strftime('%m/%d/%Y')} --- {row['Count']}"
                for _, row in grp.iterrows()
            ]

            remarks[TIME_SERIES_MAP[category]] = "<br>".join(lines)

    # ---------- GUARDED DEFAULTS ----------
    # If Last SMS Campaign sent is missing, force NULL
    if "Last SMS Campaign sent" not in remarks:
        remarks["Last SMS Campaign sent"] = "NULL"

    return remarks
