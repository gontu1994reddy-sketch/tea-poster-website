import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    data = conn.read(ttl=300)
    st.success("✅ Connected")
    st.write(data)
    st.dataframe(data)
except Exception as e:
    st.error(f"Google sheet error: {e}")