import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Fredoka Elite", layout="wide")

# --- 2. CSS (High Visibility & Fredoka) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp, p, div, span, h1, h2, h3, h4, button {
        font-family: 'Fredoka', sans-serif !important;
    }

    .stApp { background-color: #fcfcfc; color: #111111; }
    
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #000000; color: #ffffff; padding: 15px 0; overflow: hidden; border-bottom: 2px solid #222; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 20s linear infinite; font-size: 18px; font-weight: 500; }
    .ticker-move span { color: #00ff88; margin-left: 5px; }

    .Widget>label { color: #ffffff !important; font-size: 18px !important; font-weight: 600 !important; }
    .stTextInput>div>div>input { background-color: #1a1a1a !important; color: #ffffff !important; border-radius: 12px !important; }

    .kpi-card { background: #ffffff; padding: 25px; border-radius: 25px; border: 2px solid #f0f0f0; text-align: center; }
    .kpi-value { font-size: 36px; font-weight: 700; color: #000; }

    .asset-row { display: flex; justify-content: space-between; align-items: center; padding: 18px 25px; background: white; border-radius: 20px; margin-bottom: 12px; border: 1px solid #eee; }
    .activity-item { padding: 10px 15px; border-left: 4px solid #000; background: #f9f9f9; margin-bottom: 10px; border-radius: 0 10px 10px 0; font-size: 14px; }

    @keyframes wave { 0%, 100% { transform: rotate(0deg); } 20% { transform: rotate(15deg); } 40% { transform: rotate(-10deg); } 60% { transform: rotate(15deg); } }
    .wave { display: inline-block; animation: wave 2.5s infinite; transform-origin: 70% 70%; font-size: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. COMPONENTS ---
def draw_ticker():
    st.markdown("""<div class="ticker-wrap"><div class="ticker-move">BTC <span>$102,401</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; ETH <span>$4,211</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; SOL <span>$245.89</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; ADA <span>$0.65</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; BNB <span>$612.45</span></div></div>""", unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; font-size:60px;'>P.</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            e = st.text_input("Institutional Email")
            p = st.text_input("Access Key", type="password")
            if st.button("Unlock Terminal"):
                res = supabase.table("profiles").select("*").eq("email", e.lower().strip()).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
        with tab2:
            n, em, pw = st.text_input("Full Name"), st.text_input("Email"), st.text_input("Password", type="password")
            if st.button("Create Account"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Done.")

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u_data = supabase.table("profiles").select("*").eq("email", st.session_state.user['email']).execute().data[0]
    st.sidebar.markdown("## PRIME ASSETS")
    choice = st.sidebar.radio("Navigation", ["Overview", "Global Index", "Admin"] if u_data['email'].lower() == ADMIN_EMAIL.lower() else ["Overview", "Global Index"])

    if choice == "Overview":
        st.markdown(f"<h1>Welcome back, {u_data['full_name']} <span class='wave'>👋</span></h1>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="kpi-card"><small>BALANCE</small><div class="kpi-value">${u_data["balance"]:,}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><small>INVESTED</small><div class="kpi-value">${u_data["invested"]:,}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi-card"><small>YIELD</small><div class="kpi-value" style="color:#00c853;">+${u_data["interest"]:,}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="kpi-card"><small>STATUS</small><div class="kpi-value" style="color:#0066ff;">ACTIVE</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        cl, cr = st.columns([2, 1])
        with cl:
            st.markdown("### Portfolio Breakdown")
            for m in [{"l": "₿", "n": "Bitcoin", "p": "$102,401"}, {"l": "Ξ", "n": "Ethereum", "p": "$4,211"}]:
                st.markdown(f'<div class="asset-row"><div><span>{m["l"]}</span> <b>{m["n"]}</b></div><b>{m["p"]}</b></div>', unsafe_allow_html=True)
        with cr:
            st.markdown("### Live Activity")
            st.markdown('<div class="activity-item">Yield Processed: +$12.40</div>', unsafe_allow_html=True)

    elif choice == "Global Index":
        st.markdown("<h1 style='font-size:20px;'>Global Market Index (Live)</h1>", unsafe_allow_html=True)
        full_market = [{"l": "₿", "n": "Bitcoin", "p": "$102,401"}, {"l": "Ξ", "n": "Ethereum", "p": "$4,211"}, {"l": "◎", "n": "Solana", "p": "$245.80"}, {"l": "₮", "n": "Tether", "p": "$1.00"}, {"l": "🔶", "n": "Binance", "p": "$612.45"}, {"l": "✕", "n": "XRP", "p": "$0.62"}, {"l": "🐶", "n": "Doge", "p": "$0.18"}, {"l": "🔵", "n": "Polkadot", "p": "$8.45"}, {"l": "🔗", "n": "Chainlink", "p": "$19.20"}, {"l": "🌸", "n": "Cardano", "p": "$0.65"}, {"l": "🔺", "n": "Avalanche", "p": "$42.15"}, {"l": "🏗️", "n": "Near", "p": "$7.12"}, {"l": "🟣", "n": "Polygon", "p": "$0.78"}, {"l": "🌕", "n": "Luna Classic", "p": "$0.0001"}, {"l": "🛡️", "n": "Monero", "p": "$175.40"}, {"l": "🪙", "n": "Litecoin", "p": "$98.20"}, {"l": "📦", "n": "Filecoin", "p": "$6.45"}, {"l": "🌌", "n": "Cosmos", "p": "$11.20"}, {"l": "💎", "n": "Toncoin", "p": "$5.32"}, {"l": "👻", "n": "Fantom", "p": "$0.89"}]
        for m in full_market:
            st.markdown(f'<div style="font-size:20px; display:flex; justify-content:space-between; padding:15px; border-bottom:1px solid #eee;"><div><span>{m["l"]}</span> <b>{m["n"]}</b></div><div style="color:#00c853;">{m["p"]}</div></div>', unsafe_allow_html=True)

    # --- 6. ADMIN SECTION (RESTORED) ---
    elif choice == "Admin":
        st.markdown("<h1>Vault Control Panel</h1>", unsafe_allow_html=True)
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        
        st.markdown("### Client Database")
        st.dataframe(df[['full_name', 'email', 'balance', 'interest']])
        
        st.markdown("---")
        st.markdown("### Adjust Portfolio")
        target = st.selectbox("Select Client", df['email'])
        nb = st.number_input("New Balance ($)", min_value=0)
        ni = st.number_input("New Yield/Interest ($)", min_value=0)
        
        if st.button("Update Ledger"):
            supabase.table("profiles").update({"balance": nb, "interest": ni}).eq("email", target).execute()
            st.success(f"Ledger updated for {target}")
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
