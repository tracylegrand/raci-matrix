# How to Share Your RACI Matrix Builder

There are several ways to share your Streamlit application with colleagues. Choose the method that best fits your needs:

## Option 1: Streamlit Community Cloud (Easiest - Recommended) 🌟

Streamlit Community Cloud offers free hosting for public repositories. This is the easiest way to share your app.

### Steps:

1. **Push your code to GitHub:**
   ```bash
   # Initialize git repository (if not already done)
   git init
   git add raci_app.py requirements.txt
   git commit -m "Add RACI Matrix Builder app"
   
   # Create a new repository on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path to: `raci_app.py`
   - Click "Deploy"

3. **Share the link:**
   - Your app will be available at: `https://YOUR_APP_NAME.streamlit.app`
   - Share this URL with your colleagues

**Note:** Streamlit Community Cloud is free but requires a public GitHub repository. For private repos, you'll need Streamlit Teams (paid).

---

## Option 2: Share Code for Local Installation

If your colleagues can run Python locally, share the code files.

### Steps:

1. **Share the files:**
   - `raci_app.py`
   - `requirements.txt`

2. **Colleagues install and run:**
   ```bash
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Run the app
   streamlit run raci_app.py
   ```

---

## Option 3: Self-Hosted on a Server

Deploy on your own server or cloud instance (AWS, Azure, GCP, etc.).

### Steps:

1. **Set up a server** (Linux-based recommended)

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run Streamlit:**
   ```bash
   streamlit run raci_app.py --server.port 8501 --server.address 0.0.0.0
   ```

4. **Use a reverse proxy** (nginx) or firewall rules to make it accessible

5. **For production**, use a process manager like `systemd` or `supervisor`

---

## Option 4: Docker Container

Package the app in a Docker container for easy deployment.

### Create Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY raci_app.py .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "raci_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and run:

```bash
docker build -t raci-matrix-builder .
docker run -p 8501:8501 raci-matrix-builder
```

---

## Option 5: Streamlit for Teams (Enterprise)

For private repositories and enterprise features:
- Visit [streamlit.io/cloud](https://streamlit.io/cloud)
- Sign up for Streamlit Teams
- Deploy private repositories with team access controls

---

## Quick Comparison

| Method | Cost | Setup Time | Best For |
|--------|------|------------|----------|
| Streamlit Community Cloud | Free (public) | 5 min | Quick sharing, public projects |
| Local Installation | Free | 2 min | Small teams, developers |
| Self-Hosted | Varies | 30+ min | Full control, custom domain |
| Docker | Free | 15 min | Containerized environments |
| Streamlit Teams | Paid | 5 min | Enterprise, private repos |

---

## Recommended: Streamlit Community Cloud

For most use cases, **Streamlit Community Cloud** is the best option because it's:
- ✅ Free for public repos
- ✅ Easy to set up (5 minutes)
- ✅ No server maintenance
- ✅ Automatic HTTPS
- ✅ Easy to share (just a URL)

