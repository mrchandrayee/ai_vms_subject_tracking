import streamlit as st
from vms.dashboard import run_app

st.set_page_config(page_title="AI VMS | Subject Tracking", layout="wide")
run_app()
