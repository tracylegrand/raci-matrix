# 📊 Practice Manager Performance Dashboard

A Streamlit application for tracking and analyzing Practice Manager performance with Technical Services bookings in the manufacturing industry.

## Features

- ✅ **5 Practice Managers** - Track performance for Sarah Chen, Michael Rodriguez, Emily Johnson, David Park, and Jennifer Martinez
- ✅ **Quarterly Performance Tracking** - Q1 through Q4 with incremental growth
- ✅ **Multiple Booking Types** - Total Bookings, Paid Bookings, and Investment Bookings
- ✅ **Customer Account Linking** - 15 manufacturing industry customer accounts
- ✅ **Interactive Filtering** - Select individual or multiple Practice Managers
- ✅ **Visual Analytics** - Interactive charts showing trends and comparisons
- ✅ **Quarter-over-Quarter Growth** - Visual trend analysis

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run practice_manager_dashboard.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select Practice Managers**: Use the sidebar to select one or more Practice Managers
2. **Filter by Quarter**: Choose specific quarters to analyze
3. **View Performance**: See total, paid, and investment bookings
4. **Analyze Trends**: Review quarter-over-quarter growth charts
5. **Explore Customers**: View detailed customer account information

## Sharing with Colleagues

### Option 1: Streamlit Community Cloud (Recommended) 🌟

**Easiest and free for public repositories:**

1. **Push to GitHub:**
   ```bash
   git add practice_manager_dashboard.py requirements.txt
   git commit -m "Add Practice Manager Performance Dashboard"
   git push
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `practice_manager_dashboard.py`
   - Click "Deploy"
   - Share the URL: `https://YOUR_APP_NAME.streamlit.app`

### Option 2: Share Code Files

Share these files with colleagues:
- `practice_manager_dashboard.py`
- `requirements.txt`

They can then run:
```bash
pip install -r requirements.txt
streamlit run practice_manager_dashboard.py
```

### Option 3: Docker Deployment

Build and run with Docker:
```bash
docker build -f Dockerfile.pm_dashboard -t pm-dashboard .
docker run -p 8501:8501 pm-dashboard
```

### Option 4: Network Sharing (Local Network)

Run on your local network:
```bash
streamlit run practice_manager_dashboard.py --server.address 0.0.0.0
```

Then share your local IP address (e.g., `http://192.168.1.100:8501`)

## Data

The application uses **fictional data** that is automatically generated on first load. The data includes:
- 5 Practice Managers
- 15 Manufacturing industry customer accounts
- Technical Services bookings
- Quarterly performance data (Q1-Q4)
- Incremental quarter-over-quarter growth

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Support

For deployment help, see [DEPLOYMENT.md](./DEPLOYMENT.md)

