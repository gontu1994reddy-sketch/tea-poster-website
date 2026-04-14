import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    data = conn.read()
    st.write("TYPE:", type(data))
    st.write("RAW:", data)

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    st.write("COLUMNS:", data.columns.tolist())
    st.dataframe(data)

except Exception as e:
    st.error(f"Google sheet error: {e}")