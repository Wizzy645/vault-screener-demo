"""
MAIN APPLICATION ENTRY POINT - Enterprise UI
================================================
Phase 1 Architecture:
- File-based authentication (YAML config)
- Premium UI styling matching Screener Template
- Streamlined Command Center dashboard
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Quant Trading Dashboard",
    page_icon="🎛️",  
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM FINTECH UI STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1117 25%, #0f141f 50%, #0d1117 75%, #0a0e1a 100%);
        background-attachment: fixed;
        font-family: 'Inter', -apple-system, sans-serif;
        color: #e6edf3;
    }
    
    /* Hide Default Streamlit Navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Login Container */
    .login-container {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.95) 0%, rgba(13, 17, 23, 0.95) 100%);
        border: 1px solid rgba(88, 166, 255, 0.15);
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(88, 166, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Premium Headers */
    .premium-header {
        background: linear-gradient(135deg, #58a6ff 0%, #79c0ff 50%, #58a6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    
    .section-divider {
        width: 100px; 
        height: 3px; 
        background: linear-gradient(90deg, transparent, #58a6ff, transparent); 
        margin: 1.5rem auto; 
        border-radius: 2px;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(13, 17, 23, 0.6) !important;
        border: 1px solid rgba(88, 166, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #e6edf3 !important;
        padding: 0.875rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff !important;
        background: rgba(22, 27, 34, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15) !important;
    }
    
    /* Primary Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: #ffffff;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(35, 134, 54, 0.4);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# AUTHENTICATION CONFIGURATION
# ============================================================================

def load_auth_config():
    config_path = 'config.yaml'
    try:
        with open(config_path, 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        config = {
            'credentials': {
                'usernames': {
                    'demo_trader': {
                        'name': 'Demo Trader',
                        'password': '$2b$12$VLK1fPgzxAzZzYUWUx5qeOxGVxQbB4v3RqJqbOBJKgXGZCJpMRVVC',  # password123
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'quant_trading_dashboard_secure_key_123', 
                'name': 'quant_dashboard_cookie'
            },
            'preauthorized': {'emails': []}
        }
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    return config

config = load_auth_config()
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# ============================================================================
# AUTHENTICATED DASHBOARD (COMMAND CENTER)
# ============================================================================

def render_dashboard():
    # --- SIDEBAR ---
    with st.sidebar:
        # Premium Profile Card
        st.markdown("""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.6) 0%, rgba(13, 17, 23, 0.6) 100%); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); text-align: center; margin-bottom: 2rem; backdrop-filter: blur(10px);'>
    <div style='width: 60px; height: 60px; background: linear-gradient(135deg, #58a6ff 0%, #79c0ff 100%); border-radius: 50%; margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; color: #0d1117; box-shadow: 0 4px 15px rgba(88, 166, 255, 0.3);'>
        DT
    </div>
    <div style='color: #e6edf3; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.2rem;'>
        Demo Trader
    </div>
    <div style='color: #8b949e; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;'>
        Premium Tier
    </div>
</div>
""", unsafe_allow_html=True)

        # Navigation
        st.markdown("<div style='color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 1rem;'>Navigation</div>", unsafe_allow_html=True)
        st.page_link("app.py", label="Command Center", icon="🎛️")
        try:
            st.page_link("pages/1_Screener_Template.py", label="Screener Template", icon="📈")
        except Exception:
            pass

        st.markdown("---")
        
        # System Status
        st.markdown("<div style='color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 1rem;'>System Status</div>", unsafe_allow_html=True)
        st.markdown("""
<div style='display: flex; align-items: center; margin-bottom: 0.75rem; padding: 0.5rem; background: rgba(13, 17, 23, 0.5); border-radius: 8px; border: 1px solid rgba(88, 166, 255, 0.05);'>
    <div style='width: 8px; height: 8px; border-radius: 50%; background: #3fb950; margin-right: 12px; box-shadow: 0 0 10px #3fb950;'></div>
    <span style='color: #c9d1d9; font-size: 0.9rem; font-weight: 500;'>Authentication: Active</span>
</div>
<div style='display: flex; align-items: center; padding: 0.5rem; background: rgba(13, 17, 23, 0.5); border-radius: 8px; border: 1px solid rgba(88, 166, 255, 0.05);'>
    <div style='width: 8px; height: 8px; border-radius: 50%; background: #3fb950; margin-right: 12px; box-shadow: 0 0 10px #3fb950;'></div>
    <span style='color: #c9d1d9; font-size: 0.9rem; font-weight: 500;'>API Access: Granted</span>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        authenticator.logout(location='sidebar')

    # --- MAIN CONTENT ---
    st.markdown("""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <h1 class='premium-header' style='font-size: 3rem; margin-bottom: 1rem;'>
                Command Center
            </h1>
            <p style='color: #8b949e; font-size: 1.15rem; font-weight: 400;'>
                System overview and module access
            </p>
            <div class='section-divider'></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Premium metric cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 220px; display: flex; flex-direction: column; padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); position: relative; overflow: hidden; backdrop-filter: blur(10px);'>
    <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #58a6ff, transparent);'></div>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 1rem;'>Active Modules</div>
    <div class='premium-header' style='font-size: 2.75rem;'>1</div>
    <div style='margin-top: auto; padding: 0.5rem 1rem; background: linear-gradient(135deg, #238636 0%, #2ea043 100%); border-radius: 8px; color: #ffffff; font-weight: 600; font-size: 0.8rem; text-align: center;'>System Online</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 220px; display: flex; flex-direction: column; padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); position: relative; overflow: hidden; backdrop-filter: blur(10px);'>
    <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #58a6ff, transparent);'></div>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 1rem;'>Current Session</div>
    <div class='premium-header' style='font-size: 1.75rem;'>{st.session_state.get('name', 'User')}</div>
    <div style='margin-top: auto; padding: 0.5rem 1rem; background: linear-gradient(135deg, #238636 0%, #2ea043 100%); border-radius: 8px; color: #ffffff; font-weight: 600; font-size: 0.8rem; text-align: center;'>Authenticated</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 220px; display: flex; flex-direction: column; padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); position: relative; overflow: hidden; backdrop-filter: blur(10px);'>
    <div style='position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #58a6ff, transparent);'></div>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 1rem;'>Account Level</div>
    <div class='premium-header' style='font-size: 2.75rem;'>Pro</div>
    <div style='margin-top: auto; padding: 0.5rem 1rem; background: linear-gradient(135deg, #238636 0%, #2ea043 100%); border-radius: 8px; color: #ffffff; font-weight: 600; font-size: 0.8rem; text-align: center;'>Full Access</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- QUICK LAUNCH CARDS ---
    st.markdown("<h3 style='color: #c9d1d9; margin-bottom: 1rem;'>Quick Launch</h3>", unsafe_allow_html=True)
    
    q_col1, q_col2 = st.columns(2)
    
    with q_col1:
        st.markdown("""
<div style='background: rgba(30, 41, 59, 0.3); padding: 2rem; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.1); cursor: pointer; transition: all 0.3s ease;'
     onmouseover="this.style.background='rgba(30, 41, 59, 0.6)'; this.style.borderColor='rgba(88, 166, 255, 0.3)';"
     onmouseout="this.style.background='rgba(30, 41, 59, 0.3)'; this.style.borderColor='rgba(148, 163, 184, 0.1)';">
    <div style='font-size: 2rem; margin-bottom: 1rem;'>📈</div>
    <h3 style='color: #e6edf3; margin-bottom: 0.5rem;'>Technical Screener</h3>
    <p style='color: #8b949e; font-size: 0.9rem;'>Scan the market using moving averages, RSI, and custom price filters. Exports data to CSV.</p>
</div>
""", unsafe_allow_html=True)
        # Hidden button overlay to make the card clickable in Streamlit
        if st.button("Launch Screener", key="launch_screener", use_container_width=True):
            st.switch_page("pages/1_Screener_Template.py")

    with q_col2:
        st.markdown("""
<div style='background: rgba(30, 41, 59, 0.3); padding: 2rem; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.1); opacity: 0.6;'>
    <div style='font-size: 2rem; margin-bottom: 1rem;'>🤖</div>
    <h3 style='color: #e6edf3; margin-bottom: 0.5rem;'>Algorithmic Backtester</h3>
    <p style='color: #8b949e; font-size: 0.9rem;'>Test trading logic against historical data. <i>(Module in Development - Phase 2)</i></p>
</div>
""", unsafe_allow_html=True)
        st.button("Coming Soon", disabled=True, use_container_width=True)

    st.markdown("---")
    st.caption("Quant Trading Dashboard v1.1 | Enterprise UI Release")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    if not st.session_state.get('authentication_status'):
        # Display custom login branding
        col1, col2, col3 = st.columns([1, 2.5, 1])
        with col2:
            st.markdown("""
                <div style='text-align: center; margin: 2rem 0 3rem 0;'>
                    <h1 class='premium-header' style='font-size: 2.5rem; margin-bottom: 0.5rem;'>Quant Trading Dashboard</h1>
                    <p style='color: #8b949e; font-size: 1rem;'>Professional Stock Screening & Analysis Platform</p>
                    <div class='section-divider'></div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔑 Demo Credentials", expanded=False):
                st.code("Username: demo_trader\nPassword: password123", language="text")

    authenticator.login(location='main')
    
    if st.session_state.get('authentication_status'):
        render_dashboard()
    elif st.session_state.get('authentication_status') is False:
        st.error('❌ Username/password is incorrect')

if __name__ == "__main__":
    main()