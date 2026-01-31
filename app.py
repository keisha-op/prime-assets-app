import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. DATABASE CONNECTION (UPDATED) ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. ADMIN EMAIL SETTING ---
ADMIN_EMAIL = "primeassets288@gmail.com"

# --- 3. PAGE BRANDING & STYLE ---
st.set_page_config(page_title="Prime Assets | Global Terminal", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .price-card { background: #1e2329; padding: 15px; border-radius: 10px; border-left: 5px solid #f0b90b; margin-bottom: 10px; }
    .stMetric { background-color: #1e2329; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stButton>button { width: 100%; background-color: #f0b90b; color: black; font-weight: bold; border: none; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- TOP LIVE TICKER ---
cols = st.columns(4)
cols[0].markdown("<div class='price-card'>BTC/USD<br><b>$67,432.10</b> <span style='color:green'>+2.4%</span></div>", unsafe_allow_html=True)
cols[1].markdown("<div class='price-card'>ETH/USD<br><b>$3,210.45</b> <span style='color:red'>-0.8%</span></div>", unsafe_allow_html=True)
cols[2].markdown("<div class='price-card'>BNB/USD<br><b>$592.12</b> <span style='color:green'>+1.2%</span></div>", unsafe_allow_html=True)
cols[3].markdown("<div class='price-card'>SOL/USD<br><b>$145.67</b> <span style='color:green'>+5.1%</span></div>", unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if st.session_state.user is None:
    st.markdown("<h2 style='text-align: center;'>🛡️ PRIME ASSETS TERMINAL</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔒 Member Login", "🛡️ Register"])
    
    with tab1:
        e = st.text_input("Email Address")
        p = st.text_input("Password", type="password")
        if st.button("Enter Terminal"):
            try:
                res = supabase.table("profiles").select("*").eq("email", e).eq("password", p).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Credentials.")
            except Exception as err:
                st.error("Database Connection Error. Ensure your Supabase table 'profiles' exists.")
    
    with tab2:
        n = st.text_input("Full Name")
        em = st.text_input("Registration Email")
        pw = st.text_input("Secure Password", type="password")
        if st.button("Create My Account"):
            if n and em and pw:
                supabase.table("profiles").insert({"full_name": n, "email": em, "password": pw, "balance": 0}).execute()
                st.success("Registration Successful! Switch to Login tab.")
            else:
                st.warning("All fields are required.")

else:
    u = st.session_state.user
    st.sidebar.markdown("<h1 style='color: #f0b90b;'>P</h1>", unsafe_allow_html=True)
    st.sidebar.title("PRIME ASSETS")
    
    # NAVIGATION MENU
    menu = ["Dashboard", "Market Trends"]
    if u['email'].lower() == ADMIN_EMAIL.lower():
        menu.append("👑 ADMIN PANEL")
    
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Dashboard":
        st.title(f"Welcome, {u['full_name']}")
        c1, c2 = st.columns(2)
        c1.metric("Current Balance", f"${u['balance']:,}.00")
        c2.metric("Account Status", "ACTIVE", "Verified")
        st.area_chart([20, 35, 30, 45, 50, 48, 70])

    elif choice == "👑 ADMIN PANEL":
        st.title("Admin Management")
        st.write("View and Manage all Prime Assets users below:")
        
        # Pull all users
        all_users = supabase.table("profiles").select("*").execute()
        if all_users.data:
            df = pd.DataFrame(all_users.data)
            st.dataframe(df[['full_name', 'email', 'balance']])
            
            st.divider()
            st.subheader("Quick Fund User")
            target = st.selectbox("Select User to Fund", df['email'])
            new_val = st.number_input("New Balance Amount ($)", min_value=0)
            if st.button("Update User Balance"):
                supabase.table("profiles").update({"balance": new_val}).eq("email", target).execute()
                st.success(f"Balance updated for {target}!")
                st.rerun()

    if st.sidebar.button("Log Out"):
        st.session_state.user = None
        st.rerun()
