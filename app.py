import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Elite", layout="wide")

# --- 2. LUXURY NOIR CSS (Bouncy Fonts & Interactive Styles) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Outfit:wght@300;500;800&display=swap');
    
    /* Luxury Background */
    .stApp { background-color: #fcfcfc; color: #111111; font-family: 'Outfit', sans-serif; }
    
    /* Bouncy Headlines */
    h1, h2, h3, .bouncy { font-family: 'Fredoka', sans-serif; transition: 0.3s; }
    
    /* Moving Ticker (Black & White) */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #000000; color: #ffffff; padding: 12px 0; overflow: hidden; font-family: 'Fredoka', sans-serif; border-bottom: 2px solid #333; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 20s linear infinite; font-size: 16px; letter-spacing: 1px; }

    /* Interactive KPI Cards */
    .kpi-card {
        background: #ffffff; padding: 25px; border-radius: 25px;
        border: 2px solid #f0f0f0; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .kpi-card:hover { transform: scale(1.05); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: #000; }
    .kpi-value { font-size: 38px; font-weight: 800; color: #000; margin: 10px 0; }
    
    /* Interactive Row */
    .market-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 18px 25px; background: white; border-radius: 20px;
        margin-bottom: 12px; border: 1px solid #eee; transition: 0.3s;
    }
    .market-row:hover { background: #000; color: #fff !important; transform: translateX(10px); }
    .market-row:hover small { color: #ccc; }

    /* Waving Animation */
    @keyframes wave { 0% { transform: rotate(0deg); } 10% { transform: rotate(14deg); } 20% { transform: rotate(-8deg); } 30% { transform: rotate(14deg); } 40% { transform: rotate(-4deg); } 50% { transform: rotate(10deg); } 60% { transform: rotate(0deg); } 100% { transform: rotate(0deg); } }
    .wave-emoji { display: inline-block; animation: wave 2.5s infinite; transform-origin: 70% 70%; font-size: 40px; }

    /* Button Styling */
    .stButton>button {
        background: #000 !important; color: #fff !important;
        border-radius: 50px !important; padding: 15px 30px !important;
        font-family: 'Fredoka', sans-serif !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. COMPONENTS ---
def draw_ticker():
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker-move">
                BTC/USD: $102,401.50 (+2.4%) &nbsp;&bull;&nbsp; ETH/USD: $4,211.20 (+1.8%) &nbsp;&bull;&nbsp; 
                SOL/USD: $245.89 (+5.2%) &nbsp;&bull;&nbsp; ADA/USD: $0.65 (+3.1%) &nbsp;&bull;&nbsp; 
                XRP/USD: $0.62 (+1.1%) &nbsp;&bull;&nbsp; DOT/USD: $8.45 (+4.5%) &nbsp;&bull;&nbsp;
                DOGE/USD: $0.18 (+8.2%) &nbsp;&bull;&nbsp; LINK/USD: $19.20 (-0.5%)
            </div>
        </div>
        """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; font-size:50px;'>P.</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            e = st.text_input("Email")
            p = st.text_input("Key", type="password")
            if st.button("Unlock Terminal"):
                res = supabase.table("profiles").select("*").eq("email", e.lower().strip()).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n = st.text_input("Name")
            em = st.text_input("Email Address")
            pw = st.text_input("Password", type="password")
            if st.button("Create Account"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Welcome to the Elite.")

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u_data = supabase.table("profiles").select("*").eq("email", st.session_state.user['email']).execute().data[0]

    st.sidebar.markdown("<h2 class='bouncy'>PRIME.</h2>", unsafe_allow_html=True)
    menu = ["Dashboard", "Markets", "Admin Control"]
    if u_data['email'].lower() != ADMIN_EMAIL.lower():
        menu.remove("Admin Control")
    choice = st.sidebar.radio("Go to:", menu)

    if choice == "Dashboard":
        st.markdown(f"<h1>Welcome back, {u_data['full_name']} <span class='wave-emoji'>👋</span></h1>", unsafe_allow_html=True)
        
        # KPI ROW
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="kpi-card"><div class="bouncy" style="color:#888;">BALANCE</div><div class="kpi-value">${u_data["balance"]:,}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="kpi-card"><div class="bouncy" style="color:#888;">INVESTED</div><div class="kpi-value">${u_data["invested"]:,}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="kpi-card"><div class="bouncy" style="color:#888;">INTEREST</div><div class="kpi-value" style="color:#00c853;">+${u_data["interest"]:,}</div></div>', unsafe_allow_html=True)

        st.markdown("<br><h3 class='bouncy'>Your Managed Assets</h3>", unsafe_allow_html=True)
        
        # Asset List
        assets = [
            {"logo": "₿", "name": "Bitcoin", "sym": "BTC", "price": "$102,401", "chg": "+2.4%"},
            {"logo": "Ξ", "name": "Ethereum", "sym": "ETH", "price": "$4,211", "chg": "+1.8%"},
            {"logo": "◎", "name": "Solana", "sym": "SOL", "price": "$245.80", "chg": "+5.2%"},
        ]
        for a in assets:
            st.markdown(f"""
                <div class="market-row">
                    <div style="display:flex; align-items:center;">
                        <span style="font-size:24px; margin-right:15px;">{a['logo']}</span>
                        <div class="bouncy"><b>{a['name']}</b><br><small>{a['sym']}</small></div>
                    </div>
                    <div style="text-align:right;"><b class="bouncy">{a['price']}</b><br><span style="color:#00c853;">{a['chg']}</span></div>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "Markets":
        st.markdown("<h1 class='bouncy'>Global Market Index</h1>", unsafe_allow_html=True)
        
        m_data = [
            {"l": "₿", "n": "Bitcoin", "p": "$102,401", "c": "+2.4%", "s": "BULLISH"},
            {"l": "Ξ", "n": "Ethereum", "p": "$4,211", "c": "+1.8%", "s": "STABLE"},
            {"l": "◎", "n": "Solana", "p": "$245.80", "c": "+5.2%", "s": "HIGH VOL"},
            {"l": "₮", "n": "Tether", "p": "$1.00", "c": "0.0%", "s": "PEGGED"},
            {"l": "🔶", "n": "Binance", "p": "$612.45", "c": "+0.9%", "s": "NEUTRAL"},
            {"l": "✕", "n": "XRP", "p": "$0.62", "c": "+1.1%", "s": "STABLE"},
            {"l": "🐶", "n": "Doge", "p": "$0.18", "c": "+8.2%", "s": "TRENDING"},
            {"l": "🔵", "n": "Polkadot", "p": "$8.45", "c": "+4.5%", "s": "BULLISH"},
            {"l": "🔗", "n": "Chainlink", "p": "$19.20", "c": "-0.5%", "s": "BEARISH"},
            {"l": "🌸", "n": "Cardano", "p": "$0.65", "c": "+3.1%", "s": "STABLE"},
        ]
        
        for m in m_data:
            st.markdown(f"""
                <div class="market-row">
                    <div style="display:flex; align-items:center; width:30%;">
                        <span style="margin-right:15px;">{m['l']}</span>
                        <b class="bouncy">{m['n']}</b>
                    </div>
                    <div style="width:20%; font-family:'Roboto Mono';">{m['p']}</div>
                    <div style="width:20%; color:#00c853; font-weight:bold;">{m['c']}</div>
                    <div style="width:30%; text-align:right;"><span style="background:#eee; padding:5px 12px; border-radius:15px; font-size:10px; color:#333; font-weight:800;">{m['s']}</span></div>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "Admin Control":
        st.title("Admin Console")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance', 'interest']])
        
        target = st.selectbox("Client", df['email'])
        c1, c2 = st.columns(2)
        nb = c1.number_input("Set Balance")
        ni = c2.number_input("Set Interest")
        if st.button("Apply"):
            supabase.table("profiles").update({"balance": nb, "interest": ni}).eq("email", target).execute()
            st.rerun()

    if st.sidebar.button("Log out"):
        st.session_state.user = None
        st.rerun()
