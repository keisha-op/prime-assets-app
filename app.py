import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. CONFIG & CONNECTION ---
SUPABASE_URL = "https://esnuyyklguvltfngiexj.supabase.co"
SUPABASE_KEY = "sb_publishable_IUQtk2m5J5CbNEh3ZM_9Bg_DGyqR9iA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "primeassets288@gmail.com"

st.set_page_config(page_title="Prime Assets | Elite", layout="wide")

# --- 2. THE CSS (FORCING BRIGHT LABELS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp, p, div, span, h1, h2, h3, h4, button {
        font-family: 'Fredoka', sans-serif !important;
    }

    /* Force Login Labels to be Visible White */
    .stTextInput label, .stPasswordInput label {
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        display: block !important;
        margin-bottom: 8px !important;
    }

    /* Input Box Styling */
    .stTextInput input, .stPasswordInput input {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #444 !important;
    }

    /* Black Background for the Auth Card */
    .auth-card {
        background-color: #000000;
        padding: 40px;
        border-radius: 30px;
        border: 1px solid #333;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    /* Ticker Styling */
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #000000; color: #ffffff; padding: 15px 0; overflow: hidden; border-bottom: 2px solid #222; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: marquee 20s linear infinite; font-size: 18px; }
    .ticker-move span { color: #00ff88; margin-left: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TICKER COMPONENT ---
def draw_ticker():
    st.markdown("""<div class="ticker-wrap"><div class="ticker-move">BTC <span>$102,401</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; ETH <span>$4,211</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; SOL <span>$245.89</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; ADA <span>$0.65</span> &nbsp;&nbsp;&bull;&nbsp;&nbsp; BNB <span>$612.45</span></div></div>""", unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 4. AUTHENTICATION (The Visible Version) ---
if st.session_state.user is None:
    draw_ticker()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    
    with col:
        # Wrap everything in a div so we can control the background
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:white;'>P.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888; font-size:14px;'>Institutional Asset Management Portal</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Access Portal", "Open New Account"])
        
        with tab1:
            email = st.text_input("Institutional Email", key="login_email")
            password = st.text_input("Access Key", type="password", key="login_pass")
            if st.button("Unlock Dashboard", use_container_width=True):
                res = supabase.table("profiles").select("*").eq("email", email.lower().strip()).eq("password", password).execute()
                if res.data:
                    st.session_state.user = res.data[0]
                    st.rerun()
                else:
                    st.error("Invalid Authorization Key")
        
        with tab2:
            new_name = st.text_input("Full Legal Name")
            new_email = st.text_input("Corporate Email")
            new_pass = st.text_input("Create Access Key", type="password")
            if st.button("Initialize Account", use_container_width=True):
                supabase.table("profiles").insert({
                    "full_name": new_name, 
                    "email": new_email.lower().strip(), 
                    "password": new_pass, 
                    "balance": 0, 
                    "invested": 0, 
                    "interest": 0
                }).execute()
                st.success("Account Ready. Switch to 'Access Portal' to login.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. DASHBOARD ---
else:
    draw_ticker()
    u_data = supabase.table("profiles").select("*").eq("email", st.session_state.user['email']).execute().data[0]
    
    st.sidebar.markdown("## PRIME ASSETS")
    menu = ["Overview", "Global Index"]
    if u_data['email'].lower() == ADMIN_EMAIL.lower():
        menu.append("Admin")
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Overview":
        st.markdown(f"<h1>Welcome back, {u_data['full_name']} <span class='wave'>👋</span></h1>", unsafe_allow_html=True)
        # (Remaining Overview code stays the same)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BALANCE", f"${u_data['balance']:,}")
        c2.metric("INVESTED", f"${u_data['invested']:,}")
        c3.metric("YIELD", f"+${u_data['interest']:,}")
        c4.metric("STATUS", "ACTIVE")

    elif choice == "Global Index":
        st.markdown("<h1 style='font-size:20px;'>Global Market Index (Live)</h1>", unsafe_allow_html=True)
        # Use your custom 20px Fredoka list here
        full_market = [{"l": "₿", "n": "Bitcoin", "p": "$102,401"}, {"l": "Ξ", "n": "Ethereum", "p": "$4,211"}] # (Truncated for brevity)
        for m in full_market:
            st.markdown(f'<div style="font-size:20px; display:flex; justify-content:space-between; padding:15px; border-bottom:1px solid #eee;"><div><span>{m["l"]}</span> <b>{m["n"]}</b></div><div style="color:#00c853;">{m["p"]}</div></div>', unsafe_allow_html=True)

    elif choice == "Admin":
        st.title("Admin Vault Control")
        all_users = supabase.table("profiles").select("*").execute()
        df = pd.DataFrame(all_users.data)
        st.dataframe(df[['full_name', 'email', 'balance', 'interest']])
        target = st.selectbox("Select User", df['email'])
        new_bal = st.number_input("Update Balance")
        new_int = st.number_input("Update Interest")
        if st.button("Save Changes"):
            supabase.table("profiles").update({"balance": new_bal, "interest": new_int}).eq("email", target).execute()
            st.success("Updated!")
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
