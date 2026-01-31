import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Elite Global", layout="wide")

# --- 2. LUXURY NOIR CSS (High-Contrast & Bouncy) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Outfit:wght@300;500;800&display=swap');
    
    .stApp { background-color: #fcfcfc; color: #111111; font-family: 'Outfit', sans-serif; }
    
    /* Moving Ticker (Black Background, White/Green Font) */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #000000; color: #ffffff; padding: 14px 0; overflow: hidden; font-family: 'Fredoka', sans-serif; border-bottom: 3px solid #222; position: fixed; top: 0; left: 0; width: 100%; z-index: 9999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 25s linear infinite; font-size: 15px; font-weight: 500; letter-spacing: 0.5px; }
    .ticker-move span { color: #00ff88; margin-left: 5px; }

    /* Interactive KPI Cards */
    .kpi-container { display: flex; gap: 20px; justify-content: space-between; margin-top: 20px; }
    .kpi-card {
        background: #ffffff; padding: 25px; border-radius: 28px; flex: 1;
        border: 2px solid #f0f0f0; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.03);
    }
    .kpi-card:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 25px 50px rgba(0,0,0,0.1); border-color: #000; }
    .kpi-label { font-family: 'Fredoka', sans-serif; font-size: 14px; color: #888; letter-spacing: 1px; }
    .kpi-value { font-size: 34px; font-weight: 800; color: #000; margin: 8px 0; font-family: 'Fredoka', sans-serif; }

    /* Managed Asset Rows */
    .asset-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 20px 30px; background: white; border-radius: 22px;
        margin-bottom: 12px; border: 1px solid #f2f2f2; transition: 0.3s ease;
    }
    .asset-row:hover { background: #000; color: #fff !important; transform: scale(1.01); }
    .asset-logo { font-size: 28px; margin-right: 20px; }

    /* Waving Emoji Animation */
    @keyframes wave { 0%, 100% { transform: rotate(0deg); } 20% { transform: rotate(15deg); } 40% { transform: rotate(-10deg); } 60% { transform: rotate(15deg); } }
    .wave { display: inline-block; animation: wave 2.5s infinite; transform-origin: 70% 70%; }
    
    /* General Bouncy Class */
    .bouncy { font-family: 'Fredoka', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DYNAMIC COMPONENTS ---
def draw_ticker():
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker-move">
                BITCOIN (BTC) <span>$102,401.50 (+2.4%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                ETHEREUM (ETH) <span>$4,211.20 (+1.8%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                SOLANA (SOL) <span>$245.89 (+5.2%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                CARDANO (ADA) <span>$0.65 (+3.1%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                RIPPLE (XRP) <span>$0.62 (+1.1%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                POLKADOT (DOT) <span>$8.45 (+4.5%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
                DOGE <span>$0.18 (+8.2%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; 
                CHAINLINK (LINK) <span>$19.20 (-0.5%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
                AVALANCHE (AVAX) <span>$42.15 (+2.9%)</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
                TETHER (USDT) <span>$1.00 (STABLE)</span>
            </div>
        </div>
        <br><br>
        """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; font-size:60px; font-family:Fredoka;'>P.</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Secure Login", "Open Account"])
        with tab1:
            e = st.text_input("Corporate Email")
            p = st.text_input("Access Key", type="password")
            if st.button("Unlock Portal"):
                res = supabase.table("profiles").select("*").eq("email", e.lower().strip()).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n = st.text_input("Legal Name")
            em = st.text_input("Work Email")
            pw = st.text_input("New Access Key", type="password")
            if st.button("Initialize"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Account Initialized. Please Login.")

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u_data = supabase.table("profiles").select("*").eq("email", st.session_state.user['email']).execute().data[0]

    st.sidebar.markdown("<h2 class='bouncy' style='padding-top:20px;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
    menu = ["Asset Overview", "Global Index", "Admin"]
    if u_data['email'].lower() != ADMIN_EMAIL.lower():
        menu.remove("Admin")
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Asset Overview":
        st.markdown(f"<h1 class='bouncy'>Welcome back, {u_data['full_name']} <span class='wave'>👋</span></h1>", unsafe_allow_html=True)
        
        # 4 KPIs ROW
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="kpi-card"><div class="kpi-label">TOTAL BALANCE</div><div class="kpi-value">${u_data["balance"]:,}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><div class="kpi-label">CAPITAL INVESTED</div><div class="kpi-value">${u_data["invested"]:,}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi-card"><div class="kpi-label">TOTAL YIELD</div><div class="kpi-value" style="color:#00c853;">+${u_data["interest"]:,}</div></div>', unsafe_allow_html=True)
        # 4th KPI: Portfolio Health Score
        health = "98%" if u_data["balance"] > 0 else "0%"
        c4.markdown(f'<div class="kpi-card"><div class="kpi-label">PORTFOLIO HEALTH</div><div class="kpi-value" style="color:#0066ff;">{health}</div></div>', unsafe_allow_html=True)

        st.markdown("<br><h3 class='bouncy'>Active Institutional Positions</h3>", unsafe_allow_html=True)
        
        # 10 MANAGED ASSETS
        managed = [
            {"l": "₿", "n": "Bitcoin", "s": "BTC", "p": "$102,401", "c": "+2.4%"},
            {"l": "Ξ", "n": "Ethereum", "s": "ETH", "p": "$4,211", "c": "+1.8%"},
            {"l": "◎", "n": "Solana", "s": "SOL", "p": "$245.80", "c": "+5.2%"},
            {"l": "₮", "n": "Tether", "s": "USDT", "p": "$1.00", "c": "STABLE"},
            {"l": "✕", "n": "Ripple", "s": "XRP", "p": "$0.62", "c": "+1.1%"},
            {"l": "🔶", "n": "Binance", "s": "BNB", "p": "$612.45", "c": "+0.9%"},
            {"l": "🌸", "n": "Cardano", "s": "ADA", "p": "$0.65", "c": "+3.1%"},
            {"l": "🔗", "n": "Chainlink", "s": "LINK", "p": "$19.20", "c": "-0.5%"},
            {"l": "🔵", "n": "Polkadot", "s": "DOT", "p": "$8.45", "c": "+4.5%"},
            {"l": "🐶", "n": "Dogecoin", "s": "DOGE", "p": "$0.18", "c": "+8.2%"}
        ]
        
        for m in managed:
            st.markdown(f"""
                <div class="asset-row">
                    <div style="display:flex; align-items:center;">
                        <span class="asset-logo">{m['l']}</span>
                        <div class="bouncy"><b>{m['n']}</b><br><small style="color:#888;">{m['s']}</small></div>
                    </div>
                    <div style="text-align:right;"><b class="bouncy">{m['p']}</b><br><span style="color:#00c853;">{m['c']}</span></div>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "Global Index":
        st.markdown("<h1 class='bouncy'>Real-Time Market Data</h1>", unsafe_allow_html=True)
        # Reuse market logic with higher detail
        market_list = pd.DataFrame([
            {"Asset": "Bitcoin", "Ticker": "BTC", "Price (USD)": "$102,401.50", "24h Change": "+2.4%", "Status": "BULLISH"},
            {"Asset": "Ethereum", "Ticker": "ETH", "Price (USD)": "$4,211.20", "24h Change": "+1.8%", "Status": "STABLE"},
            {"Asset": "Solana", "Ticker": "SOL", "Price (USD)": "$245.89", "24h Change": "+5.2%", "Status": "HIGH VOL"},
            {"Asset": "Gold", "Ticker": "XAU", "Price (USD)": "$2,340.05", "24h Change": "-0.2%", "Status": "STABLE"},
            {"Asset": "S&P 500", "Ticker": "SPX", "Price (USD)": "$5,102.30", "24h Change": "+0.4%", "Status": "NEUTRAL"},
            {"Asset": "Tether", "Ticker": "USDT", "Price (USD)": "$1.00", "24h Change": "0.0%", "Status": "PEGGED"},
            {"Asset": "XRP", "Ticker": "XRP", "Price (USD)": "$0.62", "24h Change": "+1.1%", "Status": "NEUTRAL"},
            {"Asset": "Cardano", "Ticker": "ADA", "Price (USD)": "$0.65", "24h Change": "+3.1%", "Status": "BULLISH"},
            {"Asset": "Polkadot", "Ticker": "DOT", "Price (USD)": "$8.45", "24h Change": "+4.5%", "Status": "BULLISH"},
            {"Asset": "Binance", "Ticker": "BNB", "Price (USD)": "$612.45", "24h Change": "+0.9%", "Status": "STABLE"}
        ])
        st.table(market_list)
        st.progress(72, text="Institutional Sentiment: 72% Bullish")

    elif choice == "Admin":
        st.title("Portfolio Management")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance', 'interest']])
        target = st.selectbox("Client", df['email'])
        nb = st.number_input("New Balance")
        ni = st.number_input("New Interest")
        if st.button("Apply Portfolio Update"):
            supabase.table("profiles").update({"balance": nb, "interest": ni}).eq("email", target).execute()
            st.rerun()

    if st.sidebar.button("Secure Exit"):
        st.session_state.user = None
        st.rerun()
