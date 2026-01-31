import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Institutional Terminal", layout="wide")

# --- 2. ELITE CSS (Animations & Professional UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #f8f9fb; color: #1a1e23; font-family: 'Inter', sans-serif; }
    
    /* Moving Ticker Animation */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #0066ff; color: white; padding: 8px 0; overflow: hidden; font-weight: 600; font-size: 14px; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 30s linear infinite; }

    /* Big Logo Circle */
    .logo-circle {
        width: 100px; height: 100px; background: #0066ff; color: white;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 60px; font-weight: 800; margin: 0 auto 20px;
        box-shadow: 0 10px 20px rgba(0,102,255,0.2);
    }

    /* Professional Asset Card */
    .vault-card {
        background: white; padding: 25px; border-radius: 12px;
        border: 1px solid #eef2f6; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    /* Asset Row with Sparkline Placeholder */
    .asset-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px; background: white; border-radius: 10px;
        margin-bottom: 8px; border: 1px solid #f0f3f7;
    }
    .sparkline { font-family: monospace; color: #00875a; font-weight: bold; letter-spacing: -1px; }

    .stButton>button {
        background: #0066ff !important; color: white !important;
        border-radius: 8px !important; font-weight: 600 !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. REUSABLE MOVING TICKER ---
def draw_ticker():
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker-move">
                BTC: $102,401.50 (+2.4%) &nbsp;&nbsp;&nbsp;&nbsp; ETH: $4,211.20 (+1.8%) &nbsp;&nbsp;&nbsp;&nbsp; 
                SOL: $245.89 (+5.2%) &nbsp;&nbsp;&nbsp;&nbsp; GOLD: $2,340.05 (-0.2%) &nbsp;&nbsp;&nbsp;&nbsp;
                BNB: $612.45 (+0.9%) &nbsp;&nbsp;&nbsp;&nbsp; XRP: $0.62 (+1.1%)
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if 'user' not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        st.markdown('<div class="logo-circle">P</div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔒 Secure Login", "🛡️ Institutional Sign-up"])
        with tab1:
            email = st.text_input("Corporate Email")
            pw = st.text_input("Access Key", type="password")
            if st.button("Enter Terminal"):
                res = supabase.table("profiles").select("*").eq("email", email.lower().strip()).eq("password", pw).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n = st.text_input("Legal Full Name")
            em = st.text_input("Registration Email")
            new_pw = st.text_input("Create Access Key", type="password")
            if st.button("Create Portfolio"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": new_pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Registration Successful. Please Login.")

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u = st.session_state.user
    # Fetch real-time data for the user
    u_data = supabase.table("profiles").select("*").eq("email", u['email']).execute().data[0]

    st.sidebar.markdown("<h2 style='color:#0066ff;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
    menu = ["Assets Overview", "Market Prices", "Admin Control"]
    if u['email'].lower() != ADMIN_EMAIL.lower():
        menu.remove("Admin Control")
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Assets Overview":
        st.markdown(f"### Welcome, {u_data['full_name']} 👋")
        
        # High-End KPI Row
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"""<div class="vault-card"><small>TOTAL EQUITY</small><h3>${u_data['balance']:,}.00</h3></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class="vault-card"><small>ACTIVE CAPITAL</small><h3>${u_data['invested']:,}.00</h3></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class="vault-card"><small>TOTAL YIELD</small><h3 style="color:#00875a;">+${u_data['interest']:,}.00</h3></div>""", unsafe_allow_html=True)

        st.markdown("<br><h4>Market Exposure</h4>", unsafe_allow_html=True)
        
        # Positions with Sparklines and Logos
        positions = [
            {"img": "₿", "name": "Bitcoin", "sym": "BTC", "price": "$102,401", "trend": "📈 ﹏/‾"},
            {"img": "Ξ", "name": "Ethereum", "sym": "ETH", "price": "$4,211", "trend": "📈 ‾\_/"},
            {"img": "◎", "name": "Solana", "sym": "SOL", "price": "$245.80", "trend": "📈 /‾‾"},
        ]

        for pos in positions:
            st.markdown(f"""
                <div class="asset-row">
                    <div style="display:flex; align-items:center;">
                        <div style="background:#f0f3f7; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px; font-weight:bold; color:#0066ff;">{pos['img']}</div>
                        <div><b>{pos['name']}</b><br><small style="color:#6b778c;">{pos['sym']}</small></div>
                    </div>
                    <div class="sparkline">{pos['trend']}</div>
                    <div style="text-align:right;"><b>{pos['price']}</b><br><small style="color:#00875a;">Live</small></div>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "Market Prices":
        st.header("Global Market Index")
        # Interactive Progress Bars
        st.write("Market Dominance")
        st.progress(52, text="BTC Dominance: 52%")
        st.progress(18, text="ETH Dominance: 18%")
        
        m_df = pd.DataFrame({
            "Asset": ["Bitcoin", "Ethereum", "Gold", "S&P 500", "USDT"],
            "Price": ["$102,401", "$4,211", "$2,340", "$5,102", "$1.00"],
            "24h Vol": ["$45B", "$21B", "$12B", "$80B", "$60B"]
        })
        st.table(m_df)

    elif choice == "Admin Control":
        st.title("Admin Master Console")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance', 'invested', 'interest']])
        
        target = st.selectbox("Select Client", df['email'])
        c_a, c_b, c_c = st.columns(3)
        nb = c_a.number_input("Set Balance")
        ni = c_b.number_input("Set Invested")
        nr = c_c.number_input("Set Interest")
        if st.button("Apply Changes"):
            supabase.table("profiles").update({"balance": nb, "invested": ni, "interest": nr}).eq("email", target).execute()
            st.success("Portfolio Updated.")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
