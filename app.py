import streamlit as st
from supabase import create_client
import pandas as pd
import numpy as np

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Global Terminal", layout="wide")

# --- 2. ELITE CORPORATE CSS (No Black, No Emojis) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Roboto+Mono&display=swap');
    
    /* Clean Arctic Background */
    .stApp { background-color: #f4f7f9; color: #1a1e23; font-family: 'Montserrat', sans-serif; }
    
    /* Sidebar: Institutional Blue */
    [data-testid="stSidebar"] { 
        background-color: #ffffff !important; 
        border-right: 1px solid #e0e6ed; 
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }

    /* Glass Cards */
    .vault-card {
        background: white;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #eef2f6;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    .vault-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.08); }

    /* Interactive Asset Row */
    .asset-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 20px; background: white; border-radius: 12px;
        margin-bottom: 8px; border: 1px solid #f0f3f7;
    }
    .asset-row:hover { background: #fafbfc; border-color: #0066ff; cursor: pointer; }

    /* Typography */
    .label { color: #6b778c; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .value { color: #091e42; font-size: 32px; font-weight: 700; font-family: 'Roboto Mono', monospace; }
    .status-up { color: #00875a; font-weight: 600; font-size: 14px; background: #e3fcef; padding: 4px 10px; border-radius: 20px; }

    /* Custom Button */
    .stButton>button {
        background: #0066ff !important; color: white !important;
        border-radius: 8px !important; border: none !important;
        padding: 12px 24px !important; font-weight: 600 !important;
        width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background: #0052cc !important; box-shadow: 0 4px 12px rgba(0,102,255,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
if 'user' not in st.session_state:
    st.session_state.user = None

# AUTHENTICATION
if st.session_state.user is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        st.markdown("<h2 style='text-align:center; color:#0066ff;'>PRIME ASSETS</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#6b778c;'>Global Institutional Wealth Management</p>", unsafe_allow_html=True)
        
        email = st.text_input("Corporate ID (Email)")
        pw = st.text_input("Access Key", type="password")
        if st.button("Authenticate"):
            res = supabase.table("profiles").select("*").eq("email", email.lower().strip()).eq("password", pw).execute()
            if res.data:
                st.session_state.user = res.data[0]
                st.rerun()
            else: st.error("Authentication Failed: Invalid Credentials")

# MAIN DASHBOARD
else:
    u = st.session_state.user
    u_data = supabase.table("profiles").select("*").eq("email", u['email']).execute().data[0]

    # Sidebar Navigation
    st.sidebar.markdown("<h3 style='color:#0066ff;'>Terminal v4.0</h3>", unsafe_allow_html=True)
    menu = ["Asset Overview", "Digital Vault", "Transfer", "Admin Control"]
    if u['email'].lower() != ADMIN_EMAIL.lower():
        menu.remove("Admin Control")
    
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Asset Overview":
        st.markdown(f"#### Welcome, {u['full_name']}")
        
        # High-End KPI Row
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="vault-card"><div class="label">Total Managed Equity</div><div class="value">${u_data['balance']:,}.00</div><div class="status-up">LIVE PORTFOLIO</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="vault-card"><div class="label">Total Capital Invested</div><div class="value">${u_data['invested']:,}.00</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="vault-card"><div class="label">Accumulated Yield</div><div class="value" style="color:#00875a;">+${u_data['interest']:,}.00</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Interactive Performance List (No Charts)
        st.markdown("### Active Institutional Positions")
        positions = [
            {"name": "Bitcoin Core", "val": "$62,401.50", "share": "45%", "status": "+2.4%"},
            {"name": "Ethereum 2.0 Staking", "val": "$3,211.20", "share": "30%", "status": "+1.8%"},
            {"name": "Global Gold Index", "val": "$2,340.00", "share": "15%", "status": "-0.2%"},
            {"name": "Prime USDT Liquidity", "val": "$1.00", "share": "10%", "status": "STABLE"},
        ]
        
        for pos in positions:
            st.markdown(f"""
                <div class="asset-row">
                    <div><span style="font-weight:700;">{pos['name']}</span><br><small style="color:#6b778c;">Portfolio Allocation: {pos['share']}</small></div>
                    <div style="text-align:right;"><span style="font-family:'Roboto Mono'; font-weight:700;">{pos['val']}</span><br><span class="status-up">{pos['status']}</span></div>
                </div>
                """, unsafe_allow_html=True)

    elif choice == "Digital Vault":
        st.header("Asset Inventory")
        st.info("Your assets are secured using Grade-A Cold Storage protocols.")
        st.write("Current holdings breakdown:")
        st.progress(45, text="High Growth Assets")
        st.progress(35, text="Fixed Income")
        st.progress(20, text="Cash Reserves")

    elif choice == "Admin Control":
        st.title("Administrative Access")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.table(df[['full_name', 'email', 'balance', 'invested', 'interest']])
        
        target = st.selectbox("Select Portfolio to Modify", df['email'])
        new_bal = st.number_input("Update Balance ($)", value=0)
        new_int = st.number_input("Update Interest ($)", value=0)
        if st.button("Apply Changes"):
            supabase.table("profiles").update({"balance": new_bal, "interest": new_int}).eq("email", target).execute()
            st.success("Portfolio Updated.")

    if st.sidebar.button("Secure Logout"):
        st.session_state.user = None
        st.rerun()
