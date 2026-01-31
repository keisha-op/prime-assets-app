import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Fredoka Elite", layout="wide")

# --- 2. THE ULTIMATE FREDOKA CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp, p, div, span, h1, h2, h3, h4, button {
        font-family: 'Fredoka', sans-serif !important;
    }

    .stApp { background-color: #fcfcfc; color: #111111; }
    
    /* FIXING LOGIN LABEL VISIBILITY */
    .stTextInput label, .stPasswordInput label {
        color: #000000 !important; /* Bold Black for visibility */
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    .ticker-wrap { background: #000000; color: #ffffff; padding: 15px 0; overflow: hidden; border-bottom: 2px solid #222; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 20s linear infinite; font-size: 18px; font-weight: 500; }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-move span { color: #00ff88; margin-left: 5px; }

    .kpi-card {
        background: #ffffff; padding: 25px; border-radius: 25px;
        border: 2px solid #f0f0f0; transition: 0.4s; text-align: center;
    }
    .kpi-value { font-size: 36px; font-weight: 700; color: #000; }

    .asset-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 18px 25px; background: white; border-radius: 20px;
        margin-bottom: 12px; border: 1px solid #eee;
    }
    
    .activity-item {
        padding: 10px 15px; border-left: 4px solid #000; background: #f9f9f9;
        margin-bottom: 10px; border-radius: 0 10px 10px 0; font-size: 14px;
    }

    @keyframes wave { 0%, 100% { transform: rotate(0deg); } 20% { transform: rotate(15deg); } 40% { transform: rotate(-10deg); } 60% { transform: rotate(15deg); } }
    .wave { display: inline-block; animation: wave 2.5s infinite; transform-origin: 70% 70%; font-size: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. COMPONENTS ---
def draw_ticker():
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker-move">
                BTC <span>$102,401</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; ETH <span>$4,211</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                SOL <span>$245.89</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; ADA <span>$0.65</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                XRP <span>$0.62</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; DOT <span>$8.45</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
                DOGE <span>$0.18</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; LINK <span>$19.20</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
                AVAX <span>$42.15</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; BNB <span>$612.45</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION (CORRECTED VISIBILITY) ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; font-size:70px;'>P.</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            e = st.text_input("Email Address", placeholder="Enter your corporate email...")
            p = st.text_input("Access Key", type="password", placeholder="Enter your secret key...")
            if st.button("Unlock Dashboard", use_container_width=True):
                res = supabase.table("profiles").select("*").eq("email", e.lower().strip()).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
                else:
                    st.error("Access Denied: Check Credentials")
        with tab2:
            n = st.text_input("Full Name", placeholder="e.g. Aliko Dangote")
            em = st.text_input("Email", placeholder="e.g. aliko@prime.com")
            pw = st.text_input("Password", type="password", placeholder="Create a strong key...")
            if st.button("Create Account", use_container_width=True):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Registration Complete. Please Login.")

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u_data = supabase.table("profiles").select("*").eq("email", st.session_state.user['email']).execute().data[0]

    st.sidebar.markdown("<h2 style='padding-top:20px;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
    choice = st.sidebar.radio("Navigation", ["Overview", "Global Index", "Admin"] if u_data['email'].lower() == ADMIN_EMAIL.lower() else ["Overview", "Global Index"])

    if choice == "Overview":
        st.markdown(f"<h1>Welcome back, {u_data['full_name']} <span class='wave'>👋</span></h1>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="kpi-card"><small>BALANCE</small><div class="kpi-value">${u_data["balance"]:,}</div></div>', unsafe_
