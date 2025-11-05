# Streamlit Cloud Deployment Instructions

## Main App (Production)
- **Branch:** `main`
- **URL:** https://raci-matrix-testing.streamlit.app (or your main URL)
- **Status:** Production version without joke features

## Joke Version for Brian Kim
- **Branch:** `joke-brian-kim`
- **URL:** `https://raci-matrix-testing-BrianVersion.streamlit.app`

### Steps to Deploy Joke Version:

1. Go to Streamlit Community Cloud: https://share.streamlit.io/
2. Click "New app"
3. Configure the new app:
   - **Repository:** tracylegrand/raci-matrix
   - **Branch:** `joke-brian-kim`
   - **Main file path:** `raci_app.py`
   - **App URL:** `raci-matrix-testing-BrianVersion`

4. The full URL will be: `https://raci-matrix-testing-BrianVersion.streamlit.app`

### Current Branches:
- **main:** Production version (v1.1.0) - no joke features
- **joke-brian-kim:** Joke version (v1.1.0-joke) - includes Brian Kim joke feature

Both branches are pushed to GitHub and ready for deployment.

