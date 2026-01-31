import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Cryptfy | Prime Assets", layout="wide")

# --- 2. THE CRYPTFY UI CSS (Neon Green & Obsidian) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Obsidian Cards */
    .glass-card { 
        background: #111111; padding: 25px; border-radius: 24px; 
        border: 1px solid #222; margin-bottom: 20px; 
    }
    
    /* Neon Text & Buttons */
    .neon-text { color: #b7ff4d; font-weight: bold; }
    .stButton>button { 
        background: #b7ff4d !important; color: #000 !important; 
        border-radius: 15px !important; font-weight: 800 !important;
        padding: 15px 0px !important; border: none !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    .nav-item { padding: 10px; border-radius: 10px; margin-bottom: 5px; cursor: pointer; }
    .active-nav { background: #b7ff4d; color: black !important; font-weight: bold; }
    
    /* Table Styling */
    .asset-row { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 3. AUTHENTICATION (Login Screen) ---
if st.session_state.user is None:
    st.markdown("<br><br><h1 style='text-align:center;'>Cryptfy</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        with tab1:
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.button("Access Wallet"):
                res = supabase.table("profiles").select("*").eq("email", e.lower().strip()).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n = st.text_input("Full Name")
            em = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            if st.button("Join Cryptfy"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Welcome aboard!")

# --- 4. THE CRYPTFY DASHBOARD ---
else:
    u = st.session_state.user
    u_data = supabase.table("profiles").select("*").eq("email", u['email']).execute().data[0]

    # SIDEBAR NAVIGATION
    st.sidebar.markdown("### 🕸️ Cryptfy")
    menu = ["Dashboard", "Wallet", "Market", "Admin"] if u['email'].lower() == ADMIN_EMAIL.lower() else ["Dashboard", "Wallet", "Market"]
    choice = st.sidebar.radio("MAIN", menu)

    # MAIN CONTENT AREA
    col_main, col_swap = st.columns([2.5, 1])

    with col_main:
        st.markdown(f"## {choice}")
        
        # Portfolio Summary Card
        st.markdown(f"""
            <div class="glass-card">
                <p style="color:#888; margin-bottom:0;">Current balance (USDT)</p>
                <h1 style="font-size: 50px; margin-top:0;">${u_data['balance']:,}.02</h1>
                <p class="neon-text">▲ 0.23% (1d) &nbsp; <span style="color:white;">+${u_data['interest']:,}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts Area
        chart_data = pd.DataFrame(np.random.randn(20, 1).cumsum() + 100, columns=['Value'])
        st.line_chart(chart_data, color="#b7ff4d")

        # Top Assets List
        st.markdown("### Top assets")
        assets = [
            {"name": "Bitcoin", "sym": "BTC", "price": "$102,241", "change": "▲ 0.23%", "val": "0.232341"},
            {"name": "Ethereum", "sym": "ETH", "price": "$4,223", "change": "▲ 23.23%", "val": "425.135"},
            {"name": "Polkadot", "sym": "DOT", "price": "$13,245", "change": "▲ 5.23%", "val": "13.223"},
        ]
        for a in assets:
            st.markdown(f"""
                <div class="asset-row">
                    <div><b>{a['name']}</b><br><small style='color:#888'>{a['sym']}</small></div>
                    <div style='text-align:right;'>{a['val']}<br><small class='neon-text'>{a['change']}</small></div>
                </div>
                """, unsafe_allow_html=True)

    with col_swap:
        # Swap Interface
        st.markdown("""
            <div class="glass-card">
                <h3>Swap</h3>
                <small style='color:#888'>FROM:</small>
                <div style='background:#222; padding:10px; border-radius:10px; margin-bottom:10px;'>
                    <b>Bitcoin</b> <span style='float:right;'>7,235.02</span>
                </div>
                <small style='color:#888'>TO:</small>
                <div style='background:#222; padding:10px; border-radius:10px; margin-bottom:20px;'>
                    <b>USDT</b> <span style='float:right;'>24,230.02</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Confirm Swap"):
            st.balloons()

    # Admin Panel (Secret)
    if choice == "Admin":
        st.divider()
        st.header("Admin Control")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance']])
        
        target = st.selectbox("Client", df['email'])
        new_b = st.number_input("Set Balance")
        if st.button("Update"):
            supabase.table("profiles").update({"balance": new_b}).eq("email", target).execute()
            st.rerun()
