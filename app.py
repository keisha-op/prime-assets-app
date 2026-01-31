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

# --- 2. ELITE CORPORATE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Roboto+Mono&display=swap');
    
    .stApp { background-color: #f4f7f9; color: #1a1e23; font-family: 'Montserrat', sans-serif; }
    
    /* Moving Ticker Animation */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #0066ff; color: white; padding: 10px 0; overflow: hidden; font-weight: 600; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 25s linear infinite; }

    /* Vault Cards */
    .vault-card {
        background: white; padding: 30px; border-radius: 16px;
        border: 1px solid #eef2f6; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    /* Interactive Asset Row */
    .asset-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 20px; background: white; border-radius: 12px;
        margin-bottom: 8px; border: 1px solid #f0f3f7; transition: 0.3s;
    }
    .asset-row:hover { border-color: #0066ff; transform: scale(1.01); }

    .coin-logo { 
        width: 35px; height: 35px; background: #f0f3f7; 
        border-radius: 50%; display: flex; align-items: center; 
        justify-content: center; margin-right: 15px; font-weight: bold; color: #0066ff;
    }

    .status-up { color: #00875a; font-weight: 600; background: #e3fcef; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER: MOVING TICKER ---
def draw_ticker():
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker-move">
                BITCOIN (BTC): $102,401.50 (+2.4%) &nbsp;&nbsp;&nbsp;&nbsp; ETHEREUM (ETH): $4,211.20 (+1.8%) &nbsp;&nbsp;&nbsp;&nbsp; 
                SOLANA (SOL): $245.89 (+5.2%) &nbsp;&nbsp;&nbsp;&nbsp; GOLD: $2,340.05 (-0.2%) &nbsp;&nbsp;&nbsp;&nbsp;
                TETHER (USDT): $1.00 (STABLE) &nbsp;&nbsp;&nbsp;&nbsp; BINANCE (BNB): $612.45 (+0.9%)
            </div>
        </div>
        """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        st.markdown("<h2 style='text-align:center; color:#0066ff;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Secure Login", "Institutional Sign-up"])
        with tab1:
            email = st.text_input("Corporate Email")
            pw = st.text_input("Access Key", type="password")
            if st.button("Authenticate"):
                res = supabase.table("profiles").select("*").eq("email", email.lower().strip()).eq("password", pw).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n = st.text_input("Full Name")
            em = st.text_input("Email Address")
            new_pw = st.text_input("Password", type="password")
            if st.button("Register Account"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": new_pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Registration Successful.")

# --- 5. MAIN DASHBOARD ---
else:
    draw_ticker()
    u = st.session_state.user
    u_data = supabase.table("profiles").select("*").eq("email", u['email']).execute().data[0]

    st.sidebar.markdown("<h3 style='color:#0066ff;'>Prime Terminal</h3>", unsafe_allow_html=True)
    menu = ["Asset Overview", "Live Market Prices", "Admin Control"]
    if u['email'].lower() != ADMIN_EMAIL.lower():
        menu.remove("Admin Control")
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Asset Overview":
        st.markdown(f"#### Welcome back, {u_data['full_name']}")
        
        # KPI Cards
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"""<div class="vault-card"><small>TOTAL EQUITY</small><h2>${u_data['balance']:,}.00</h2></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class="vault-card"><small>CAPITAL INVESTED</small><h2>${u_data['invested']:,}.00</h2></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class="vault-card"><small>YIELD EARNED</small><h2 style="color:#00875a;">+${u_data['interest']:,}.00</h2></div>""", unsafe_allow_html=True)

        st.markdown("<br>### Portfolio Allocation", unsafe_allow_html=True)
        
        # Interactive Asset Rows with "Logos"
        positions = [
            {"logo": "₿", "name": "Bitcoin Core", "val": "$62,401.50", "share": "45%", "status": "+2.4%"},
            {"logo": "Ξ", "name": "Ethereum 2.0", "val": "$3,211.20", "share": "30%", "status": "+1.8%"},
            {"logo": "₮", "name": "USDT Liquidity", "val": "$1.00", "share": "25%", "status": "STABLE"},
        ]
        
        for pos in positions:
            st.markdown(f"""
                <div class="asset-row">
                    <div style="display:flex; align-items:center;">
                        <div class="coin-logo">{pos['logo']}</div>
                        <div><span style="font-weight:700;">{pos['name']}</span><br><small style="color:#6b778c;">Allocation: {pos['share']}</small></div>
                    </div>
                    <div style="text-align:right;"><span style="font-family:'Roboto Mono'; font-weight:700;">{pos['val']}</span><br><span class="status-up">{pos['status']}</span></div>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "Live Market Prices":
        st.header("Global Market Index")
        st.write("Real-time valuation of major institutional assets.")
        
        # Market Table
        market_data = pd.DataFrame({
            "Asset": ["Bitcoin", "Ethereum", "Solana", "Gold (oz)", "S&P 500 Index"],
            "Price (USD)": ["$102,401.50", "$4,211.20", "$245.80", "$2,340.05", "$5,102.30"],
            "Change (24h)": ["+2.41%", "+1.80%", "+5.22%", "-0.20%", "+0.45%"],
            "Status": ["Bullish", "Bullish", "Overbought", "Stable", "Neutral"]
        })
        st.table(market_data)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(65, text="Institutional Buy Pressure: 65%")

    elif choice == "Admin Control":
        st.title("Admin Console")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance', 'interest']])
        
        target = st.selectbox("Select Client", df['email'])
        new_bal = st.number_input("Update Balance")
        new_int = st.number_input("Update Interest")
        if st.button("Save Changes"):
            supabase.table("profiles").update({"balance": new_bal, "interest": new_int}).eq("email", target).execute()
            st.success("User account updated.")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
