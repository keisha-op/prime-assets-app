import streamlit as st
from supabase import create_client

# --- 1. DATABASE CONNECTION ---
# ⚠️ PASTE YOUR ACTUAL KEYS FROM SUPABASE SETTINGS HERE
SUPABASE_URL = "https://your-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Prime Assets | Secure Terminal", layout="wide")

# Custom CSS for the "Fine" Interface
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    [data-testid="stMetricValue"] { color: #f0b90b !important; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; background-color: #f0b90b; color: black; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- LOGIN & SIGNUP LOGIC ---
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.title("🔑 Login")
        email = st.text_input("Email", key="login_email")
        pw = st.text_input("Password", type="password", key="login_pw")
        if st.button("Enter Terminal"):
            res = supabase.table("profiles").select("*").eq("email", email).eq("password", pw).execute()
            if res.data:
                st.session_state.user = res.data[0]
                st.rer
