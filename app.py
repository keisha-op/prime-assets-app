import streamlit as st
from supabase import create_client
import pandas as pd

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
    
    /* Global Font Override */
    html, body, [class*="css"], .stApp, p, div, span, h1, h2, h3, h4, button {
        font-family: 'Fredoka', sans-serif !important;
    }

    .stApp { background-color: #fcfcfc; color: #111111; }
    
    /* Moving Ticker (Black & White) */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #000000; color: #ffffff; padding: 15px 0; overflow: hidden; border-bottom: 2px solid #222; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 20s linear infinite; font-size: 18px; font-weight: 500; }
    .ticker-move span { color: #00ff88; margin-left: 5px; }

    /* Interactive KPI Cards */
    .kpi-card {
        background: #ffffff; padding: 25px; border-radius: 25px;
        border: 2px solid #f0f0f0; transition: 0.4s ease-in-out;
        text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }
    .kpi-card:hover { transform: scale(1.05); border-color: #000; box-shadow: 0 15px 30px rgba(0,0,0,0.08); }
    .kpi-value { font-size: 36px; font-weight: 700; color: #000; margin-top: 5px; }

    /* Asset Row Styling */
    .asset-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 18px 25px; background: white; border-radius: 20px;
        margin-bottom: 12px; border: 1px solid #eee; transition: 0.3s;
    }
    .asset-row:hover { background: #000; color: #fff !important; transform: translateX(8px); }
    
    /* Activity Feed Styling */
    .activity-item {
        padding: 10px 15px; border-left: 4px solid #000; background: #f9f9f9;
        margin-bottom: 10px; border-radius: 0 10px 10px 0; font-size: 14px;
    }

    /* Waving Emoji */
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

# --- 4. AUTHENTICATION ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; font-size:70px;'>P.</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            e = st.text_input("Email Address")
            p = st.text_input("Access Key", type="password")
            if st.button("Unlock Dashboard"):
                res = supabase.table("profiles").select("*").eq("email", e.lower().strip()).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n = st.text_input("Full Name")
            em = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            if st.button("Create Account"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Registration Complete.")

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u_data = supabase.table("profiles").select("*").eq("email", st.session_state.user['email']).execute().data[0]

    st.sidebar.markdown("<h2 style='padding-top:20px;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
    choice = st.sidebar.radio("Navigation", ["Overview", "Global Index", "Admin"] if u_data['email'].lower() == ADMIN_EMAIL.lower() else ["Overview", "Global Index"])

    if choice == "Overview":
        st.markdown(f"<h1>Welcome back, {u_data['full_name']} <span class='wave'>👋</span></h1>", unsafe_allow_html=True)
        
        # 4 KPIs
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="kpi-card"><small>BALANCE</small><div class="kpi-value">${u_data["balance"]:,}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><small>INVESTED</small><div class="kpi-value">${u_data["invested"]:,}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi-card"><small>YIELD</small><div class="kpi-value" style="color:#00c853;">+${u_data["interest"]:,}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="kpi-card"><small>STATUS</small><div class="kpi-value" style="color:#0066ff;">ACTIVE</div></div>', unsafe_allow_html=True)

        # Dynamic Grid: Assets vs Activity
        st.markdown("<br>", unsafe_allow_html=True)
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown("### Portfolio Breakdown")
            managed = [
                {"l": "₿", "n": "Bitcoin", "p": "$102,401", "c": "+2.4%"},
                {"l": "Ξ", "n": "Ethereum", "p": "$4,211", "c": "+1.8%"},
                {"l": "◎", "n": "Solana", "p": "$245.80", "c": "+5.2%"},
                {"l": "₮", "n": "Tether", "p": "$1.00", "c": "STABLE"},
                {"l": "✕", "n": "Ripple", "p": "$0.62", "c": "+1.1%"}
            ]
            for m in managed:
                st.markdown(f'<div class="asset-row"><div><span style="font-size:22px; margin-right:12px;">{m["l"]}</span><b>{m["n"]}</b></div><div><b>{m["p"]}</b> <span style="color:#00c853; margin-left:10px;">{m["c"]}</span></div></div>', unsafe_allow_html=True)

        with col_right:
            st.markdown("### Live Activity")
            activities = [
                "Yield Processed: +$12.40",
                "Security Audit: Passed",
                "BTC Price Alert: Up 2.4%",
                "USDT Staking: Active"
            ]
            for act in activities:
                st.markdown(f'<div class="activity-item">{act}</div>', unsafe_allow_html=True)

    elif choice == "Global Index":
        st.markdown("<h1>Global Index (20)</h1>", unsafe_allow_html=True)
        
        full_market = [
            {"l": "₿", "n": "Bitcoin", "p": "$102,401", "ch": "+2.4%", "st": "BULLISH"},
            {"l": "Ξ", "n": "Ethereum", "p": "$4,211", "ch": "+1.8%", "st": "STABLE"},
            {"l": "◎", "n": "Solana", "p": "$245.80", "ch": "+5.2%", "st": "HIGH VOL"},
            {"l": "₮", "n": "Tether", "p": "$1.00", "ch": "0.0%", "st": "PEGGED"},
            {"l": "🔶", "n": "Binance", "p": "$612.45", "ch": "+0.9%", "st": "STABLE"},
            {"l": "✕", "n": "XRP", "p": "$0.62", "ch": "+1.1%", "st": "STABLE"},
            {"l": "🐶", "n": "Doge", "p": "$0.18", "ch": "+8.2%", "st": "TRENDING"},
            {"l": "🔵", "n": "Polkadot", "p": "$8.45", "ch": "+4.5%", "st": "BULLISH"},
            {"l": "🔗", "n": "Chainlink", "p": "$19.20", "ch": "-0.5%", "st": "BEARISH"},
            {"l": "🌸", "n": "Cardano", "ch": "+3.1%", "p": "$0.65", "st": "STABLE"},
            {"l": "🔺", "n": "Avalanche", "p": "$42.15", "ch": "+2.9%", "st": "BULLISH"},
            {"l": "🏗️", "n": "Near", "p": "$7.12", "ch": "+4.1%", "st": "GROWTH"},
            {"l": "🟣", "n": "Polygon", "p": "$0.78", "ch": "-1.2%", "st": "NEUTRAL"},
            {"l": "🌕", "n": "Luna Classic", "p": "$0.0001", "ch": "+0.2%", "st": "VOLATILE"},
            {"l": "🛡️", "n": "Monero", "p": "$175.40", "ch": "+0.5%", "st": "SECURE"},
            {"l": "🪙", "n": "Litecoin", "p": "$98.20", "ch": "+1.3%", "st": "STABLE"},
            {"l": "📦", "n": "Filecoin", "p": "$6.45", "ch": "+2.1%", "st": "STABLE"},
            {"l": "🌌", "n": "Cosmos", "p": "$11.20", "ch": "+3.4%", "st": "BULLISH"},
            {"l": "💎", "n": "Toncoin", "p": "$5.32", "ch": "+6.7%", "st": "HIGH GROWTH"},
            {"l": "👻", "n": "Fantom", "p": "$0.89", "ch": "+1.9%", "st": "STABLE"}
        ]
        
        for m in full_market:
            st.markdown(f"""
                <div class="asset-row">
                    <div style="display:flex; align-items:center; width:30%;">
                        <span style="margin-right:12px; font-size:22px;">{m['l']}</span>
                        <b>{m['n']}</b>
                    </div>
                    <div style="width:25%; font-weight:600;">{m['p']}</div>
                    <div style="width:20%; color:#00c853; font-weight:bold;">{m['ch']}</div>
                    <div style="width:25%; text-align:right;"><span style="background:#eee; padding:5px 12px; border-radius:15px; font-size:11px; font-weight:700;">{m['st']}</span></div>
                </div>
                """, unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
