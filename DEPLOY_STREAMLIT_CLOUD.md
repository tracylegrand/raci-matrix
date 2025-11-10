# Deploy RACI App to Streamlit Cloud with Snowflake

This guide walks you through deploying the RACI Matrix Builder to Streamlit Cloud and configuring Snowflake integration.

## Prerequisites

1. ✅ Code committed to GitHub repository
2. ✅ Snowflake account and credentials ready
3. ✅ GitHub account connected to Streamlit Cloud

## Step 1: Commit and Push Your Code

First, make sure all your changes are committed and pushed to GitHub:

```bash
# Check current status
git status

# Add all changes (excluding secrets.toml which is in .gitignore)
git add raci_app.py requirements.txt SNOWFLAKE_SETUP.md DEPLOY_STREAMLIT_CLOUD.md

# Commit changes
git commit -m "Add Snowflake integration and deployment configuration"

# Push to GitHub (replace with your remote name if different)
git push origin main
```

**Important**: The `.streamlit/secrets.toml` file is already in `.gitignore`, so it won't be committed. This is correct - you'll configure secrets directly in Streamlit Cloud.

## Step 2: Deploy to Streamlit Cloud

### 2.1 Go to Streamlit Community Cloud

1. Visit [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. Authorize Streamlit to access your repositories

### 2.2 Create New App

1. Click **"New app"** button
2. Fill in the deployment details:
   - **Repository**: Select your GitHub repository (e.g., `tracylegrand/raci-matrix`)
   - **Branch**: `main` (or the branch you want to deploy)
   - **Main file path**: `raci_app.py`
   - **App URL**: Choose a name (e.g., `raci-matrix-builder`)
     - ⚠️ **Note**: URL must be all lowercase, no spaces or special characters (except hyphens)
     - Example: ✅ `raci-matrix-builder` ❌ `RACI-Matrix-Builder`

3. Click **"Deploy"**

4. Wait 1-2 minutes for the initial deployment

## Step 3: Configure Snowflake Secrets in Streamlit Cloud

### 3.1 Access App Settings

1. Once deployed, click on your app in the Streamlit Cloud dashboard
2. Click the **"⋮"** (three dots) menu in the top right
3. Select **"Settings"**

### 3.2 Add Snowflake Secrets

1. In the Settings page, find the **"Secrets"** section
2. Click **"Edit secrets"** or the **"+"** button
3. Paste the following template and fill in your actual Snowflake credentials:

```toml
[snowflake]
account = "your_account_identifier"
user = "your_username"
password = "your_password"
warehouse = "your_warehouse"
database = "your_database"
schema = "your_schema"
role = ""
```

**Example:**
```toml
[snowflake]
account = "abc12345.us-east-1"
user = "my_username"
password = "my_secure_password"
warehouse = "COMPUTE_WH"
database = "RACI_DB"
schema = "PUBLIC"
role = ""
```

### 3.3 Save Secrets

1. Click **"Save"** to save your secrets
2. The app will automatically redeploy with the new secrets

## Step 4: Verify Deployment

### 4.1 Check App Status

1. Go to your app URL: `https://YOUR_APP_NAME.streamlit.app`
2. Verify the app loads correctly
3. Check for any error messages

### 4.2 Test Snowflake Integration

1. Create a test RACI matrix:
   - Add a function (e.g., "Project Planning")
   - Add a stakeholder (e.g., "Project Manager")
   - Assign a RACI role

2. Go to the **"💾 Snowflake Database"** section

3. Try saving to Snowflake:
   - Enter a matrix name (e.g., "Test Matrix")
   - Enter your name in "Created By"
   - Click **"💾 Save to Snowflake"**

4. If successful, you should see:
   - ✅ Success message with matrix ID
   - The matrix should appear in the "Load from Snowflake" tab

## Step 5: Share Your App

Once deployed and tested:

1. **Share the URL**: `https://YOUR_APP_NAME.streamlit.app`
2. **No installation needed** - users can access it directly in their browser
3. **Automatic updates** - when you push changes to GitHub, Streamlit Cloud automatically redeploys

## Troubleshooting

### App Won't Deploy

**Error: "Module not found"**
- Check that `requirements.txt` includes all dependencies
- Verify `snowflake-connector-python>=3.0.0` is in requirements.txt

**Error: "File not found"**
- Verify `raci_app.py` is in the repository root
- Check the "Main file path" in deployment settings

### Snowflake Connection Issues

**Error: "Snowflake credentials not found"**
- Go to Settings → Secrets
- Verify the `[snowflake]` section exists
- Check that all required fields are filled (account, user, password, warehouse, database, schema)

**Error: "Error connecting to Snowflake"**
- Verify your account identifier format (may need region: `account.region`)
- Check that username and password are correct
- Ensure warehouse, database, and schema names match exactly (case-sensitive)
- Verify your Snowflake account allows connections from Streamlit Cloud IPs

**Error: "Error initializing Snowflake table"**
- Check that your user has CREATE TABLE permissions
- Verify database and schema exist
- Ensure warehouse is running (not suspended)

### App Deploys But Shows Errors

1. **Check logs**: In Streamlit Cloud dashboard, click "Manage app" → "Logs"
2. **Check secrets**: Verify secrets are correctly formatted (TOML format)
3. **Test locally first**: Run `streamlit run raci_app.py` locally to catch errors

## Updating Your App

To update the deployed app:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
3. Streamlit Cloud automatically detects the push and redeploys
4. Wait 1-2 minutes for the new version to be live

## Security Best Practices

1. ✅ **Never commit secrets.toml** - It's already in `.gitignore`
2. ✅ **Use Streamlit Cloud Secrets** - Never hardcode credentials in code
3. ✅ **Rotate passwords regularly** - Update secrets in Streamlit Cloud when you rotate Snowflake passwords
4. ✅ **Use service accounts** - Consider creating a dedicated Snowflake user for the app
5. ✅ **Limit permissions** - Grant only necessary permissions to the Snowflake user

## Next Steps

- ✅ App is deployed and accessible
- ✅ Snowflake integration is configured
- ✅ Users can save/load RACI matrices from Snowflake
- 📊 Share the app URL with your team
- 🔄 Set up automated backups if needed
- 📈 Monitor usage in Streamlit Cloud dashboard

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify Snowflake connection using Snowflake web interface
3. Test locally with `streamlit run raci_app.py`
4. Review error messages in the app UI

