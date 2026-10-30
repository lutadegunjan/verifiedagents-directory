
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="VerifiedAgents Directory",
    page_icon="📋",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "verifiedagents_enriched_candidate_4000.csv"

COLUMNS = [
    "s_no",
    "profile_page_url",
    "full_name",
    "npn_number",
    "location",
    "phone_numbers",
    "email_addresses",
    "websites",
    "appointed_companies",
    "scraped_by",
]

DETAIL_FIELDS = [
    "location",
    "phone_numbers",
    "email_addresses",
    "websites",
    "appointed_companies",
]

st.title("VerifiedAgents Directory")
st.caption("Insurance Agent Directory | 4,000 Profiles")

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()


@st.cache_data
def load_data(path, modified_time):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = [col for col in COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df[COLUMNS].fillna("")


try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load dataset: {exc}")
    st.stop()


def has_value(series):
    return series.astype(str).str.strip().ne("")


st.sidebar.header("Search and Filters")
search = st.sidebar.text_input(
    "Search all fields",
    placeholder="Enter name, NPN, location, email...",
)

filtered = df.copy()

if search.strip():
    mask = filtered.apply(
        lambda row: row.astype(str).str.contains(
            search.strip(), case=False, regex=False
        ).any(),
        axis=1,
    )
    filtered = filtered[mask]

with st.sidebar.expander("Individual column filters", expanded=True):
    for col in COLUMNS:
        value = st.text_input(
            col.replace("_", " ").title(),
            key=f"filter_{col}",
            placeholder=f"Filter by {col.replace('_', ' ')}",
        )
        if value.strip():
            filtered = filtered[
                filtered[col].str.contains(
                    value.strip(),
                    case=False,
                    regex=False,
                    na=False,
                )
            ]

total = len(df)
shown = len(filtered)

st.subheader("Directory Overview")
k1, k2, k3 = st.columns(3)
k1.metric("Total Profiles", f"{total:,}")
k2.metric("Filtered Profiles", f"{shown:,}")
k3.metric("Profiles with NPN", f"{has_value(filtered['npn_number']).sum():,}")

st.subheader("Data Availability")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Locations", f"{has_value(filtered['location']).sum():,}")
k2.metric("Phone Numbers", f"{has_value(filtered['phone_numbers']).sum():,}")
k3.metric("Email Addresses", f"{has_value(filtered['email_addresses']).sum():,}")
k4.metric("Websites", f"{has_value(filtered['websites']).sum():,}")
k5.metric(
    "Appointed Companies",
    f"{has_value(filtered['appointed_companies']).sum():,}",
)

st.subheader("Field Coverage")
coverage = []
for col in DETAIL_FIELDS:
    count = int(has_value(filtered[col]).sum())
    percentage = (count / shown * 100) if shown else 0
    coverage.append(
        {
            "Field": col.replace("_", " ").title(),
            "Available Records": count,
            "Missing Records": shown - count,
            "Coverage (%)": round(percentage, 2),
        }
    )

st.dataframe(pd.DataFrame(coverage), width="stretch", hide_index=True)

if int(has_value(df["websites"]).sum()) == 0:
    st.info(
        "No website URLs are populated in the current dataset. "
        "Blank values have been retained rather than filled with unverified information."
    )

st.subheader("Agent Records")
st.caption(f"Showing {shown:,} of {total:,} profiles.")
st.dataframe(
    filtered,
    column_config={
        "profile_page_url": st.column_config.LinkColumn(
            "Profile Page",
            display_text="Open Profile",
        )
    },
    width="stretch",
    hide_index=True,
    height=600,
)

st.download_button(
    label="Download Filtered CSV",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name="verifiedagents_filtered.csv",
    mime="text/csv",
    disabled=filtered.empty,
)

