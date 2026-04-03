"""
SCREENER TEMPLATE - Enterprise Technical Analysis
==================================================
Phase 1: Production UI Rewrite
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Screener Template",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# AUTHENTICATION CHECK
# ============================================================================
if 'authentication_status' not in st.session_state or not st.session_state.get('authentication_status'):
    st.error("Access Denied: Please login from the main page")
    st.stop()

# ============================================================================
# PREMIUM FINTECH UI STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* Hide Default Streamlit Navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #58a6ff 0%, #79c0ff 50%, #58a6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    
    /* Section Dividers */
    .section-divider {
        width: 100px; 
        height: 3px; 
        background: linear-gradient(90deg, transparent, #58a6ff, transparent); 
        margin: 1.5rem auto; 
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA FETCHING & MATH FUNCTIONS (CACHED)
# ============================================================================

@st.cache_data(ttl=300, show_spinner=False)
def fetch_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        if df.empty:
            raise ValueError(f"No data available for ticker: {ticker}")
        df['Ticker'] = ticker
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def fetch_multiple_tickers(tickers: list, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    all_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, ticker in enumerate(tickers):
        status_text.text(f"Fetching {ticker}... ({idx + 1}/{len(tickers)})")
        df = fetch_stock_data(ticker, period, interval)
        if not df.empty:
            all_data.append(df)
        progress_bar.progress((idx + 1) / len(tickers))
        time.sleep(0.1)
        
    progress_bar.empty()
    status_text.empty()
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def calculate_rsi(df: pd.DataFrame, window: int = 14, column: str = 'Close') -> pd.Series:
    delta = df[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values('Date')
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['Price_vs_SMA20'] = ((df['Close'] - df['SMA_20']) / df['SMA_20'] * 100)
    df['Price_vs_SMA50'] = ((df['Close'] - df['SMA_50']) / df['SMA_50'] * 100)
    df['RSI_14'] = calculate_rsi(df, 14)
    df['Daily_Change_%'] = df['Close'].pct_change() * 100
    df['Above_SMA20'] = df['Close'] > df['SMA_20']
    return df

# ============================================================================
# SIDEBAR - NAVIGATION, PROFILE & INPUTS
# ============================================================================

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

    # Command Inputs
    st.markdown("<div style='color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 1rem;'>Search Targets</div>", unsafe_allow_html=True)
    
    # Smart Input: Handles 1 or 100 tickers gracefully
    ticker_text = st.text_input("Enter Tickers (comma-separated)", value="AAPL, MSFT, NVDA, TSLA", placeholder="e.g. AAPL, TSLA, BTC-USD")
    tickers = [t.strip().upper() for t in ticker_text.split(',') if t.strip()]
    
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    with col2:
        interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

    # Prime CTA exactly where it belongs
    run_analysis = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
    
    st.markdown("---")

    # Progressive Disclosure for Filters
    with st.expander("⚙️ Advanced Parameters", expanded=True):
        min_price = st.number_input("Minimum Price ($)", min_value=0.0, value=0.0, step=10.0)
        min_volume = st.number_input("Minimum Volume", min_value=0, value=0, step=1000000)
        rsi_range = st.slider("RSI Range", min_value=0, max_value=100, value=(0, 100))
        show_latest_only = st.checkbox("Show Latest Data Only", value=True)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 class='premium-header' style='font-size: 3rem; margin-bottom: 1rem;'>
            Technical Analysis Engine
        </h1>
        <p style='color: #8b949e; font-size: 1.15rem; font-weight: 400;'>
            Real-time equity screening and momentum detection
        </p>
        <div class='section-divider'></div>
    </div>
""", unsafe_allow_html=True)

if run_analysis or 'last_analysis' not in st.session_state:
    if not tickers:
        st.error("⚠️ Please enter at least one valid ticker symbol.")
        st.stop()
        
    with st.spinner("Executing Market Scan..."):
        df = fetch_multiple_tickers(tickers, period, interval)
        
    if df.empty:
        st.error("❌ Failed to fetch data. Verify ticker symbols and network connection.")
        st.stop()

    with st.spinner("Processing Technical Indicators..."):
        df_with_indicators = df.groupby('Ticker', group_keys=True).apply(add_technical_indicators, include_groups=False).reset_index()

    # Apply Filters
    df_with_indicators = df_with_indicators[
        (df_with_indicators['Close'] >= min_price) &
        (df_with_indicators['Volume'] >= min_volume) &
        (df_with_indicators['RSI_14'] >= rsi_range[0]) &
        (df_with_indicators['RSI_14'] <= rsi_range[1])
    ]

    if show_latest_only and 'Ticker' in df_with_indicators.columns:
        df_display = df_with_indicators.groupby('Ticker').tail(1).reset_index(drop=True)
    else:
        df_display = df_with_indicators

    st.session_state['last_analysis'] = df_display
    st.session_state['full_data'] = df_with_indicators
    st.session_state['tickers'] = tickers

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

if 'last_analysis' in st.session_state:
    df_display = st.session_state['last_analysis']
    
    # --- METRICS ROW ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 140px; display: flex; flex-direction: column; justify-content: space-between; padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);'>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;'>Scan Results</div>
    <div class='premium-header' style='font-size: 2.25rem;'>{len(df_display)}</div>
    <div style='color: #64748b; font-size: 0.8rem;'>Matches Found</div>
</div>
""", unsafe_allow_html=True)
    with col2:
        avg_rsi = df_display['RSI_14'].mean() if 'RSI_14' in df_display.columns else 0
        st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 140px; display: flex; flex-direction: column; justify-content: space-between; padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);'>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;'>Sector Momentum</div>
    <div class='premium-header' style='font-size: 2.25rem;'>{avg_rsi:.1f}</div>
    <div style='color: #64748b; font-size: 0.8rem;'>Average RSI</div>
</div>
""", unsafe_allow_html=True)
    with col3:
        num_tickers = len(st.session_state['tickers'])
        st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 140px; display: flex; flex-direction: column; justify-content: space-between; padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);'>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;'>Target Universe</div>
    <div class='premium-header' style='font-size: 2.25rem;'>{num_tickers}</div>
    <div style='color: #64748b; font-size: 0.8rem;'>Assets Scanned</div>
</div>
""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
<div style='background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%); height: 140px; display: flex; flex-direction: column; justify-content: space-between; padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.15); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);'>
    <div style='color: #8b949e; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;'>System Status</div>
    <div class='premium-header' style='font-size: 2.25rem;'>Live</div>
    <div style='color: #64748b; font-size: 0.8rem;'>Data Synced</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- THE DATA GRID ---
    if not df_display.empty:
        st.markdown("<h3 style='color: #c9d1d9; margin-bottom: 1rem;'>Market Overview</h3>", unsafe_allow_html=True)
        
        # Enterprise Dataframe Configuration
        st.dataframe(
            df_display,
            column_config={
                "Date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
                "Ticker": st.column_config.TextColumn("Symbol"),
                "Close": st.column_config.NumberColumn("Close Price", format="$%.2f"),
                "Volume": st.column_config.NumberColumn("Volume", format="%d"),
                "Daily_Change_%": st.column_config.NumberColumn("Daily Change", format="%.2f %%"),
                "RSI_14": st.column_config.ProgressColumn("RSI (14-Day)", min_value=0, max_value=100, format="%.1f"),
                "Price_vs_SMA20": st.column_config.NumberColumn("vs SMA 20", format="%.2f %%"),
                "Price_vs_SMA50": st.column_config.NumberColumn("vs SMA 50", format="%.2f %%"),
            },
            column_order=["Date", "Ticker", "Close", "Daily_Change_%", "Volume", "RSI_14", "Price_vs_SMA20", "Price_vs_SMA50"],
            hide_index=True,
            use_container_width=True,
            height=400
        )
        
        col_space, col_dl = st.columns([4, 1])
        with col_dl:
            st.download_button(
                label="📥 Export Data",
                data=df_display.to_csv(index=False).encode('utf-8'),
                file_name=f"screener_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    # --- THE CHART ---
    tickers_list = st.session_state['tickers']
    if len(tickers_list) == 1 and not st.session_state['full_data'].empty:
        st.markdown("<br><h3 style='color: #c9d1d9; margin-bottom: 1rem;'>Technical Chart</h3>", unsafe_allow_html=True)
        
        ticker_data = st.session_state['full_data'].sort_values('Date')
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
        
        # Candlesticks
        fig.add_trace(go.Candlestick(
            x=ticker_data['Date'], open=ticker_data['Open'], high=ticker_data['High'],
            low=ticker_data['Low'], close=ticker_data['Close'], name='Price',
            increasing_line_color='#3fb950', decreasing_line_color='#f85149'
        ), row=1, col=1)
        
        # SMAs
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_20'], name='SMA 20', line=dict(color='#58a6ff', width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['SMA_50'], name='SMA 50', line=dict(color='#d29922', width=1.5)), row=1, col=1)
        
        # RSI
        fig.add_trace(go.Scatter(
            x=ticker_data['Date'], y=ticker_data['RSI_14'], name='RSI',
            line=dict(color='#bc8cff', width=1.5), fill='tozeroy', fillcolor='rgba(188, 140, 255, 0.1)'
        ), row=2, col=1)
        
        # Reference Lines
        fig.add_hline(y=70, line_dash="dash", line_color="#f85149", opacity=0.5, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#3fb950", opacity=0.5, row=2, col=1)
        
        # Professional Styling
        fig.update_layout(
            template='plotly_dark',
            height=600,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False, # Hidden for cleaner UI
            plot_bgcolor='rgba(13, 17, 23, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_rangeslider_visible=False,
            hovermode='x unified'
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(48, 54, 61, 0.5)', zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(48, 54, 61, 0.5)', zeroline=False)
        
        # Hide the floating toolbar
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})