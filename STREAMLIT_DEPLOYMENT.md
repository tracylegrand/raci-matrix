# Streamlit Cloud Deployment Instructions

## Main App (Production)
- **Branch:** `main`
- **URL:** https://raci-matrix-testing.streamlit.app (or your main URL)
- **Status:** Production version without joke features

## Joke Version for Brian Kim
- **Branch:** `joke-brian-kim`
- **URL:** `https://raci-matrix-testing-brianversion.streamlit.app`
  - **Note:** Streamlit URLs are lowercase only - use `brianversion` (all lowercase)

### Steps to Deploy Joke Version:

1. Go to Streamlit Community Cloud: https://share.streamlit.io/
2. Click "New app"
3. Configure the new app:
   - **Repository:** tracylegrand/raci-matrix
   - **Branch:** `joke-brian-kim`
   - **Main file path:** `raci_app.py`
   - **App URL:** `raci-matrix-testing-brianversion` (must be lowercase, no capital letters)

4. The full URL will be: `https://raci-matrix-testing-brianversion.streamlit.app`

### Troubleshooting Access Errors:

**If you get an access error, check:**
1. **App is deployed:** Go to https://share.streamlit.io/ and verify the app exists
2. **URL format:** Streamlit URLs must be:
   - All lowercase
   - No spaces or special characters (except hyphens)
   - Example: ✅ `raci-matrix-testing-brianversion` ❌ `raci-matrix-testing-BrianVersion`
3. **Branch exists:** Verify `joke-brian-kim` branch is on GitHub
4. **Deployment status:** Check the app status in Streamlit Cloud dashboard

### Current Branches:
- **main:** Production version (v1.1.0) - no joke features
- **joke-brian-kim:** Joke version (v1.1.0-joke) - includes Brian Kim joke feature

Both branches are pushed to GitHub and ready for deployment.

