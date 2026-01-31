import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets Elite", layout="wide")

# --- 2. THE "DRIBBBLE" CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8f9fb; }
    .stApp { background-color: #f8f9fb; }

    /* Top Marquee Ticker */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #0b0e11; color: #f0b90b; padding: 10px; font-weight: 600; overflow: hidden; }
    .ticker-move { display: flex; animation: marquee 30s linear infinite; }
    .ticker-item { padding: 0 50px; white-space: nowrap; }

    /* Premium Wallet Cards */
    .wallet-card { 
        background: linear-gradient(135deg, #1e2329 0%, #0b0e11 100%); 
        padding: 30px; border-radius: 20px; color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .stats-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;
        text-align: left;
    }
    .label { color: #848e9c; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .value { color: #1e2329; font-size: 28px; font-weight: 800; margin-top: 5px; }
    .interest { color: #03a66d; font-weight: 700; font-size: 14px; }

    /* Sidebar and Buttons */
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #eee; }
    .stButton>button { 
        background: #f0b90b !important; color: black !important; 
        border-radius: 12px !important; border: none !important;
        font-weight: 700 !important; width: 100%; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TOP MOVING TICKER ---
st.markdown('<div class="ticker-wrap"><div class="ticker-move">'
            '<div class="ticker-item">BTC/USD: $67,432.10 (+2.4%)</div>'
            '<div class="ticker-item">ETH/USD: $3,210.45 (-0.8%)</div>'
            '<div class="ticker-item">SOL/USD: $145.67 (+5.1%)</div>'
            '<div class="ticker-item">BNB/USD: $592.12 (+1.2%)</div>'
            '</div></div>', unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION UI ---
if st.session_state.user is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h1 style='text-align:center; color:#1e2329;'>Prime Assets</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#848e9c;'>The world's most trusted asset terminal.</p>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["Login", "Create Account"])
        with t1:
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            if st.button("Sign In to Secure Vault"):
                res = supabase.table("profiles").select("*").eq("email", email.lower().strip()).eq("password", pw).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
                else: st.error("Access Denied.")
        with t2:
            n = st.text_input("Full Name")
            em = st.text_input("Work Email")
            new_pw = st.text_input("New Password", type="password")
            if st.button("Open Institutional Account"):
                supabase.table("profiles").insert({"full_name": n, "email": em.lower().strip(), "password": new_pw, "balance": 0, "invested": 0, "interest": 0}).execute()
                st.success("Registration Successful.")

# --- 5. THE REAL DASHBOARD ---
else:
    u = st.session_state.user
    # Re-fetch for live admin updates
    u_data = supabase.table("profiles").select("*").eq("email", u['email']).execute().data[0]
    
    # Sidebar
    st.sidebar.markdown("<h2 style='color:#1e2329;'>P. Assets</h2>", unsafe_allow_html=True)
    menu = ["Dashboard", "Market", "Wallets"]
    if u['email'].lower() == ADMIN_EMAIL.lower():
        menu.append("👑 ADMIN MASTER")
    
    choice = st.sidebar.radio("Navigation", menu)
    
    if choice == "Dashboard":
        st.markdown(f"### Hello, {u['full_name']} 👋")
        
        # Main Wallet Card (Dark Mode)
        st.markdown(f"""
            <div class="wallet-card">
                <div class="label" style="color:#f0b90b;">Total Account Value</div>
                <div style="font-size: 40px; font-weight: 800; margin: 10px 0;">${u_data['balance']:,}.00</div>
                <div style="font-size: 14px; opacity: 0.8;">Account ID: PA-{u_data['id'][:8].upper()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sub Stats (White Cards)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="stats-card"><div class="label">Total Invested</div><div class="value">${u_data['invested']:,}.00</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="stats-card"><div class="label">Profit / Interest</div><div class="value" style="color:#03a66d;">+${u_data['interest']:,}.00</div><div class="interest">↑ 12.5% This Month</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Asset Performance")
        st.area_chart([100, 150, 130, 170, 210, 240, 300])

    elif choice == "👑 ADMIN MASTER":
        st.title("Admin Master Control")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.write("### All Client Portfolios")
        st.dataframe(df[['full_name', 'email', 'balance', 'invested', 'interest']])
        
        st.divider()
        st.subheader("Modify Client Assets")
        target = st.selectbox("Select User", df['email'])
        c1, c2, c3 = st.columns(3)
        b = c1.number_input("Balance", value=0)
        i = c2.number_input("Invested", value=0)
        r = c3.number_input("Interest", value=0)
        
        if st.button("Update Account Data"):
            supabase.table("profiles").update({"balance": b, "invested": i, "interest": r}).eq("email", target).execute()
            st.success("Successfully updated.")
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
