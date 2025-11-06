# 📊 Streamlit Applications

This repository contains multiple Streamlit applications:

## 1. Interactive RACI Matrix Builder

A Streamlit application for creating and managing RACI (Responsible, Accountable, Consulted, Informed) matrices interactively.

## Features

- ✅ **Interactive RACI Matrix** - Add functions (rows) and stakeholders (columns)
- ✅ **Visual Color Coding** - Easy-to-read matrix with color-coded roles
- ✅ **Export to Excel** - Formatted spreadsheet with colors and borders
- ✅ **Export to CSV** - Simple CSV format for data analysis
- ✅ **Export to PowerPoint** - Presentation-ready slide with formatted table

## Quick Start

### Installation

```bash
# Install dependencies
pip3 install -r requirements.txt
```

### Run Locally

```bash
streamlit run raci_app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Add Functions**: Use the sidebar to add functions (rows) to your matrix
2. **Add Stakeholders**: Add stakeholders (columns) in the sidebar
3. **Fill RACI Roles**: Select R, A, C, or I for each cell in the matrix
4. **Export**: Download your matrix as Excel, CSV, or PowerPoint

## Sharing the Application

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions on sharing this app with colleagues.

**Quick options:**
- 🌟 **Streamlit Community Cloud** (Recommended) - Free hosting for public repos
- 📦 **Share code** - Colleagues run locally
- 🐳 **Docker** - Containerized deployment
- 🖥️ **Self-hosted** - Deploy on your own server

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 2. Practice Manager Performance Dashboard

A Streamlit application for tracking and analyzing Practice Manager performance with Technical Services bookings in the manufacturing industry.

**Quick Start:**
```bash
streamlit run practice_manager_dashboard.py
```

**Features:**
- Track 5 Practice Managers' quarterly performance
- Total, Paid, and Investment bookings tracking
- Customer account linking (manufacturing industry)
- Interactive filtering and visualizations
- Quarter-over-quarter growth analysis

**To share with colleagues:** See [SHARE_PM_DASHBOARD.md](./SHARE_PM_DASHBOARD.md) for quick deployment guide.

For full documentation, see [PM_DASHBOARD_README.md](./PM_DASHBOARD_README.md)

---

## License

This project is open source and available for use.
