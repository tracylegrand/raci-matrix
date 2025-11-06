# 🚀 Quick Guide: Share Practice Manager Dashboard

## Fastest Way: Streamlit Community Cloud (5 minutes)

### Step 1: Push to GitHub

If you haven't already:

```bash
# Make sure you're in the Git directory
cd /Users/tlegrand/Documents/Git

# Add and commit the dashboard
git add practice_manager_dashboard.py requirements.txt PM_DASHBOARD_README.md
git commit -m "Add Practice Manager Performance Dashboard"

# Push to GitHub (replace with your repo URL)
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select your GitHub repo
   - **Branch**: `main` (or `master`)
   - **Main file path**: `practice_manager_dashboard.py`
   - **App URL**: Choose a name (e.g., `pm-performance-dashboard`)
5. Click **"Deploy"**
6. Wait 1-2 minutes for deployment
7. **Share the URL** with colleagues: `https://pm-performance-dashboard.streamlit.app`

### ✅ Done!

Your colleagues can now access the dashboard via the shared URL. No installation needed!

---

## Alternative: Share via Network (Same Office)

If you're on the same network:

```bash
# Run with network access
streamlit run practice_manager_dashboard.py --server.address 0.0.0.0
```

Find your IP address:
- Mac/Linux: `ifconfig | grep "inet "`
- Windows: `ipconfig`

Share: `http://YOUR_IP_ADDRESS:8501`

---

## Alternative: Share Code Files

Send these files to colleagues:
- `practice_manager_dashboard.py`
- `requirements.txt`

They run:
```bash
pip install -r requirements.txt
streamlit run practice_manager_dashboard.py
```

---

## Need Help?

- See [PM_DASHBOARD_README.md](./PM_DASHBOARD_README.md) for full documentation
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for advanced deployment options

