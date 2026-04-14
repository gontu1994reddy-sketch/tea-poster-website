import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    data = conn.read(ttl=0)
    st.write("✅ Connected")
    st.write(data)
    st.write(type(data))
except Exception as e:
    st.error(f"Google sheet error: {e}")