from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.streamlit.v1.spreadsheet import _get_mito_backend

st.set_page_config(layout="wide")


@st.cache_data
def get_dataset():
    df = pd.read_csv(
        "http://cycpeptmpdb.com/static//download/peptides/CycPeptMPDB_Peptide_All.csv"
    )
    df = df[
        [
            "CycPeptMPDB_ID",
            "Source",
            "Year",
            "Original_Name_in_Source_Literature",
            "SMILES",
            "Permeability",
            "Same_Peptides_ID",
            "Same_Peptides_Source",
            "Same_Peptides_Permeability",
            "Same_Peptides_Assay",
        ]
    ]
    return df


# Title
st.title("📂 Dataset")
st.caption("LLM Hackathon for Materials & Chemistry - EPFL Hub")


# File uploader
uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True
)

for uploaded_file in uploaded_files:
    st.write("filename:", uploaded_file.name)

df = get_dataset()

new_dfs, code = spreadsheet(df)
# code = code if code else "# Edit the spreadsheet above to generate code"
st.code(code)


def clear_mito_backend_cache():
    _get_mito_backend.clear()


# Function to cache the last execution time - so we can clear periodically
@st.cache_resource
def get_cached_time():
    # Initialize with a dictionary to store the last execution time
    return {"last_executed_time": None}


def try_clear_cache():

    # How often to clear the cache
    CLEAR_DELTA = timedelta(hours=12)

    current_time = datetime.now()
    cached_time = get_cached_time()

    # Check if the current time is different from the cached last execution time
    if (
        cached_time["last_executed_time"] is None
        or cached_time["last_executed_time"] + CLEAR_DELTA < current_time
    ):
        clear_mito_backend_cache()
        cached_time["last_executed_time"] = current_time


try_clear_cache()
