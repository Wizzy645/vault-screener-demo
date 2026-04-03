# 📊 Quant Trading Dashboard - Phase 1
## Professional Stock Screening Web Application

---

## 🎯 Quick Start (3 Steps)

### Step 1: Run the Setup Script
```cmd
setup.bat
```

This will:
- Create the `pages` folder
- Install all Python dependencies
- Verify your setup

### Step 2: Create the Screener Template
1. Open `SCREENER_TEMPLATE_CODE.txt`
2. Copy ALL the code
3. Create a new file: `pages\1_Screener_Template.py`
4. Paste the code and save

### Step 3: Launch the App
```cmd
streamlit run app.py
```

Login with:
- **Username**: `demo_trader`
- **Password**: `password123`

---

## 📁 Project Files

| File | Status | Purpose |
|------|--------|---------|
| `app.py` | ✅ Created | Main entry point with authentication |
| `requirements.txt` | ✅ Created | Python dependencies |
| `setup.bat` | ✅ Created | Automated setup script |
| `SETUP_GUIDE.md` | ✅ Created | Detailed setup instructions |
| `SCREENER_TEMPLATE_CODE.txt` | ✅ Created | Full screener code to copy |
| `pages/` | ⚠️ **YOU CREATE** | Folder for screener pages |
| `pages/1_Screener_Template.py` | ⚠️ **YOU CREATE** | Copy code from .txt file |
| `config.yaml` | Auto-generated | User credentials (created on first run) |

---

## 🚀 Features

### Authentication
- ✅ Secure bcrypt password hashing
- ✅ Session-based auth with cookies
- ✅ Easy user management via YAML file
- ✅ Auto-logout functionality

### Screener Capabilities
- ✅ **Single or multi-ticker analysis**
- ✅ **Technical Indicators**:
  - SMA 20, 50, 200
  - RSI (Relative Strength Index)
  - Golden Cross / Death Cross detection
  - Price vs SMA percentage
- ✅ **Smart Caching** (5-min TTL, prevents API rate limits)
- ✅ **Advanced Filters**: Price, Volume, RSI range
- ✅ **Sortable/Filterable Tables**: Native Streamlit dataframes
- ✅ **CSV Export**: Download results instantly
- ✅ **Professional Dark Theme**: Desktop & mobile friendly

---

## 🖥️ User Interface

### Login Screen
```
📊 Quant Trading Dashboard
Professional Stock Screening & Analysis Platform

[Username input]
[Password input]
[Login button]

Demo Credentials:
Username: demo_trader
Password: password123
```

### Main Dashboard
```
🎯 Welcome to Your Quant Trading Dashboard

[Metrics: Active Screeners | Logged In | Access Level]

Getting Started Guide:
- Navigation via sidebar
- Available screeners
- Features & best practices
```

### Screener Interface
```
📈 Screener Template - Technical Analysis

Sidebar Configuration:
├── 📊 Ticker Selection (single or multiple)
├── 📅 Timeframe (period & interval)
├── 🔍 Filters (price, volume, RSI)
└── 📋 Display Options (columns, latest only)

Main Area:
├── 📊 Analysis Parameters
├── 🔄 Data Fetching (with progress)
├── ⚙️ Indicator Calculation
├── 📊 Summary Metrics
└── 📋 Sortable Results Table + Download
```

---

## 🔐 Managing Users

### View Current Users
Open `config.yaml` after first run to see:

```yaml
credentials:
  usernames:
    demo_trader:
      name: 'Demo Trader'
      password: '$2b$12$...'  # Hashed password
    admin:
      name: 'Administrator'
      password: '$2b$12$...'
```

### Add New User

1. **Generate Password Hash**:
```python
from streamlit_authenticator import Hasher
hashed = Hasher(['new_password_123']).generate()[0]
print(hashed)
```

2. **Add to config.yaml**:
```yaml
credentials:
  usernames:
    new_trader:
      name: 'John Doe'
      password: '$2b$12$...'  # Your hashed password
```

3. **Restart the app**

### Remove User
Simply delete their entry from `config.yaml` and restart.

---

## 🛠️ Technical Details

### Tech Stack
```
Frontend:  Streamlit 1.32+
Auth:      streamlit-authenticator 0.3.2
Data:      yfinance 0.2.37
Analysis:  pandas 2.2.0, numpy 1.26.0
Config:    PyYAML 6.0.1
```

### Caching Strategy
```python
@st.cache_data(ttl=300)  # 5-minute cache
def fetch_stock_data(ticker, period, interval):
    # Prevents excessive API calls
    # Automatically refreshes every 5 minutes
    # Can manually clear via app menu
```

### File Structure
```
c:\Users\hp\upwork projects\
│
├── app.py                          # Main entry (auth gatekeeper)
├── requirements.txt                # Dependencies
├── config.yaml                     # User credentials (auto-generated)
│
├── pages/                          # Multi-page app structure
│   └── 1_Screener_Template.py    # Example screener
│
├── setup.bat                       # Setup automation
├── SETUP_GUIDE.md                  # Detailed guide
├── SCREENER_TEMPLATE_CODE.txt      # Code to copy
└── README.md                       # This file
```

---

## 📊 Example Workflow

### Scenario: Screen Tech Stocks Above SMA20

1. **Login** with credentials
2. **Navigate** to "Screener Template"
3. **Configure**:
   - Multiple Tickers: `AAPL,MSFT,GOOGL,AMZN,META`
   - Period: `1y`
   - Interval: `1d`
   - Enable Filters: ✅
   - Minimum Price: `$50`
   - Display Columns: `Ticker, Close, SMA_20, Price_vs_SMA20, RSI_14`
4. **Run Analysis** ▶️
5. **Review Results**:
   - Sort by `Price_vs_SMA20` (descending)
   - Filter RSI between 30-70
   - Identify stocks above SMA20 with healthy momentum
6. **Download CSV** for further analysis

---

## 🔧 Customization

### Add New Screener

1. **Duplicate Template**:
```cmd
copy pages\1_Screener_Template.py pages\2_Momentum_Screener.py
```

2. **Rename & Modify**:
```python
# In 2_Momentum_Screener.py
st.title("💨 Momentum Screener - Volume Surge Detection")

# Add your custom logic here:
def calculate_volume_surge(df):
    df['Avg_Volume_50'] = df['Volume'].rolling(50).mean()
    df['Volume_Surge_%'] = (df['Volume'] / df['Avg_Volume_50'] - 1) * 100
    return df
```

3. **Restart App** - New page appears automatically in sidebar!

### Modify Theme Colors

In `app.py`, change the CSS:

```python
st.markdown("""
    <style>
    /* Change primary color from green to blue */
    .stButton > button {
        background-color: #0066ff;  /* Was: #00d4aa */
    }
    </style>
""", unsafe_allow_html=True)
```

---

## ⚠️ Troubleshooting

### Issue: "Module not found" error
**Solution**: 
```cmd
pip install -r requirements.txt
```

### Issue: "No data for ticker XYZ"
**Solution**:
- Verify ticker exists on Yahoo Finance
- Check for typos (case-insensitive)
- Try a different ticker to test connectivity

### Issue: "Rate limit exceeded"
**Solution**:
- Wait 5 minutes for cache to reset
- Reduce number of tickers
- Use longer intervals (1wk instead of 1d)

### Issue: "Authentication failed"
**Solution**:
- Delete `config.yaml` and restart (regenerates defaults)
- Check username/password exactly (case-sensitive)
- Clear browser cookies

### Issue: "Pages not showing in sidebar"
**Solution**:
- Ensure `pages` folder exists
- Check file naming: `1_Name.py` (number_underscore_name)
- Restart Streamlit app

---

## 📈 Phase 2 Roadmap

### Planned Enhancements

1. **More Screeners**:
   - Momentum Strategy (volume surge, price acceleration)
   - Value Investing (P/E, P/B, dividend yield)
   - Growth Stocks (revenue growth, EPS trends)
   - Options Flow (unusual activity)

2. **Advanced Features**:
   - Interactive Plotly charts
   - Backtesting framework
   - Email/SMS alerts
   - Watchlist management
   - Portfolio tracking

3. **Infrastructure**:
   - Database backend (PostgreSQL)
   - REST API for programmatic access
   - Cloud deployment (AWS/Azure)
   - Payment integration (Stripe)
   - User roles & permissions

4. **Analytics**:
   - Correlation heatmaps
   - Sector rotation analysis
   - Market regime detection
   - Risk metrics (Sharpe, Beta, etc.)

---

## 📞 Support

### Documentation
- **Setup Guide**: `SETUP_GUIDE.md` (detailed instructions)
- **Code Reference**: `SCREENER_TEMPLATE_CODE.txt` (full template)
- **This README**: Quick reference & troubleshooting

### Community Resources
- [Streamlit Docs](https://docs.streamlit.io)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Pandas Tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)

---

## 🔒 Security Notes

### For Development (Current)
- ✅ Passwords hashed with bcrypt
- ✅ Session cookies with expiration
- ✅ File-based credentials (easy to manage)
- ⚠️ config.yaml should be in .gitignore
- ⚠️ Change cookie secret key in production

### For Production (Phase 2)
- 🔜 HTTPS/SSL required
- 🔜 Database for credentials
- 🔜 2FA authentication
- 🔜 Rate limiting
- 🔜 Audit logging

---

## 📜 License & Disclaimer

### Usage
This is a **commercial tool** built for professional traders. It's designed for Phase 1 deployment with paying users.

### Disclaimer
- **Not Financial Advice**: For educational/analytical purposes only
- **Data Accuracy**: Yahoo Finance data may have delays/errors
- **Risk Warning**: Trading involves significant risk of loss
- **No Warranty**: Provided as-is without guarantees

### Credits
- **Framework**: Streamlit (Apache 2.0 License)
- **Data Provider**: Yahoo Finance via yfinance
- **Authentication**: streamlit-authenticator
- **Built by**: Quant Python Engineer

---

## ✅ Final Checklist

Before launching to clients:

- [ ] Run `setup.bat` successfully
- [ ] Create `pages` folder
- [ ] Copy code to `pages\1_Screener_Template.py`
- [ ] Test login with demo credentials
- [ ] Test screener with real tickers
- [ ] Customize `config.yaml` with real users
- [ ] Change cookie secret key in `app.py`
- [ ] Add `config.yaml` to `.gitignore`
- [ ] Test on target deployment environment
- [ ] Prepare user documentation
- [ ] Set up support channel

---

## 🎉 You're Ready!

**Run this command to start:**
```cmd
streamlit run app.py
```

**Access at:** `http://localhost:8501`

**Happy Trading! 📊📈**

---

*Version 1.0.0 | Phase 1 Commercial Release | Built with Streamlit*
