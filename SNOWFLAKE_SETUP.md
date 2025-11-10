# Snowflake Integration Setup Guide

This guide explains how to configure Snowflake database storage for the RACI Matrix Builder application.

## Overview

The RACI Matrix Builder can save and load RACI matrices from a Snowflake database, providing persistent storage across sessions and users.

## Prerequisites

1. **Snowflake Account**: You need access to a Snowflake account
2. **Database Access**: Permissions to create tables and insert/select data
3. **Streamlit Secrets**: Ability to configure secrets in Streamlit (local or Cloud)

## Step 1: Install Dependencies

The required packages are already in `requirements.txt`:
- `snowflake-connector-python>=3.0.0`
- `snowflake-sqlalchemy>=1.4.0`

Install them:
```bash
pip install -r requirements.txt
```

## Step 2: Configure Snowflake Connection

### For Local Development

1. Create a `.streamlit` directory in your project root (if it doesn't exist):
   ```bash
   mkdir -p .streamlit
   ```

2. Create or edit `.streamlit/secrets.toml`:
   ```toml
   [snowflake]
   account = "your_account_identifier"
   user = "your_username"
   password = "your_password"
   warehouse = "your_warehouse"
   database = "your_database"
   schema = "your_schema"
   role = "your_role"  # Optional
   ```

### For Streamlit Cloud Deployment

1. Go to your Streamlit Cloud app dashboard
2. Click on "Settings" → "Secrets"
3. Add the following secrets:
   ```toml
   [snowflake]
   account = "your_account_identifier"
   user = "your_username"
   password = "your_password"
   warehouse = "your_warehouse"
   database = "your_database"
   schema = "your_schema"
   role = "your_role"  # Optional
   ```

## Step 3: Snowflake Account Configuration

### Finding Your Account Identifier

Your Snowflake account identifier can be found in your Snowflake URL:
- Format: `https://<account_identifier>.snowflakecomputing.com`
- Example: If your URL is `https://abc12345.us-east-1.snowflakecomputing.com`, your account is `abc12345.us-east-1`

### Required Snowflake Objects

1. **Warehouse**: A compute warehouse for running queries
   ```sql
   CREATE WAREHOUSE IF NOT EXISTS my_warehouse
   WITH WAREHOUSE_SIZE = 'X-SMALL'
   AUTO_SUSPEND = 60
   AUTO_RESUME = TRUE;
   ```

2. **Database**: A database to store the RACI matrices
   ```sql
   CREATE DATABASE IF NOT EXISTS raci_db;
   ```

3. **Schema**: A schema within the database
   ```sql
   USE DATABASE raci_db;
   CREATE SCHEMA IF NOT EXISTS raci_schema;
   ```

4. **Role** (Optional): A role with appropriate permissions
   ```sql
   CREATE ROLE IF NOT EXISTS raci_role;
   GRANT USAGE ON WAREHOUSE my_warehouse TO ROLE raci_role;
   GRANT USAGE ON DATABASE raci_db TO ROLE raci_role;
   GRANT USAGE ON SCHEMA raci_db.raci_schema TO ROLE raci_role;
   GRANT CREATE TABLE ON SCHEMA raci_db.raci_schema TO ROLE raci_role;
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA raci_db.raci_schema TO ROLE raci_role;
   ```

## Step 4: Table Structure

The application automatically creates the `raci_matrices` table on first use. The table structure is:

```sql
CREATE TABLE IF NOT EXISTS raci_matrices (
    matrix_id VARCHAR(255),
    matrix_name VARCHAR(500),
    functions VARIANT,
    stakeholders VARIANT,
    raci_data VARIANT,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    created_by VARCHAR(255),
    PRIMARY KEY (matrix_id)
);
```

**Note**: The table is created automatically when you first save a matrix. You don't need to create it manually.

## Step 5: Test the Connection

1. Run the Streamlit app:
   ```bash
   streamlit run raci_app.py
   ```

2. Create a test RACI matrix with some functions and stakeholders

3. Go to the "💾 Snowflake Database" section

4. Try saving a matrix - if configured correctly, you should see a success message

## Troubleshooting

### Error: "Snowflake credentials not found"

- **Solution**: Make sure `.streamlit/secrets.toml` exists and contains the `[snowflake]` section
- For Streamlit Cloud: Check that secrets are configured in the app settings

### Error: "Error connecting to Snowflake"

- **Check**: Account identifier format (should include region if applicable)
- **Check**: Username and password are correct
- **Check**: Warehouse, database, and schema names are correct
- **Check**: Network connectivity to Snowflake

### Error: "Error initializing Snowflake table"

- **Check**: User has CREATE TABLE permissions on the schema
- **Check**: Database and schema exist
- **Check**: Warehouse is running (not suspended)

### Error: "snowflake-connector-python not installed"

- **Solution**: Run `pip install snowflake-connector-python`

## Security Best Practices

1. **Never commit secrets.toml to Git**: Add `.streamlit/secrets.toml` to `.gitignore`
2. **Use Streamlit Secrets**: For production, always use Streamlit Cloud secrets or environment variables
3. **Use Service Accounts**: Consider using service accounts with limited permissions
4. **Rotate Passwords**: Regularly rotate Snowflake passwords
5. **Use Key Pair Authentication**: For production, consider using key pair authentication instead of passwords

## Features

Once configured, you can:

- **Save Matrices**: Save your current RACI matrix with a name and creator identifier
- **Load Matrices**: Load previously saved matrices from Snowflake
- **List Matrices**: View all saved matrices with metadata (name, created date, updated date, creator)
- **Delete Matrices**: Remove matrices you no longer need

## Data Storage

- **Matrix ID**: Unique UUID for each saved matrix
- **Matrix Name**: User-provided descriptive name
- **Functions**: Stored as JSON array in VARIANT column
- **Stakeholders**: Stored as JSON array in VARIANT column
- **RACI Data**: Stored as JSON object in VARIANT column
- **Timestamps**: Automatic creation and update timestamps
- **Created By**: User identifier for tracking

## Support

For issues or questions:
1. Check the error messages in the app - they provide specific details
2. Verify your Snowflake connection using Snowflake's web interface
3. Check Streamlit logs for detailed error information

