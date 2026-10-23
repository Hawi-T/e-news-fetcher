# 📰 News Fetcher Pro (CLI & Web App)

A modern, real-time news aggregator with both an **Interactive Command-Line Interface** and a **Stunning Browser Web Application** powered by **Python, FastAPI, and NewsAPI**.

---

## 🌟 Key Features

- **🌐 Sleek Web Interface**: Modern dark mode, glassmorphism design, responsive card layouts, and topic filters.
- **⚡ Command-Line Interface (CLI)**: Fast, lightweight terminal news reader with structured menus.
- **🔍 Custom Keyword & Topic Search**: Search for any query (e.g., *"Artificial Intelligence"*, *"SpaceX"*, *"Quantum Computing"*) or choose from curated categories (Technology, Sports, Business, Science, Entertainment, Health).
- **🖼️ Rich Article Previews**: Displays article images, news sources, publication dates, excerpts, and external links.
- **🔬 Educational Raw JSON Viewer**: One-click toggle in the browser and CLI to inspect raw API payloads.
- **🔒 Secure Secrets Management**: API keys are isolated in `.env` and guarded by `.gitignore`.
- **🛡️ Production-Grade Error Handling**: Handles network disconnects, timeouts, takedown placeholders (`[Removed]`), and invalid keys with friendly error messages.

---

## 📁 Project Structure

```text
News Fetcher/
├── static/
│   ├── index.html       # Web application front-end UI
│   ├── style.css        # Premium responsive styling (Vanilla CSS)
│   └── app.js           # Interactive UI logic & API calls
├── .env                 # Private API key (ignored by Git)
├── .env.example         # Template for environment configuration
├── .gitignore           # Keeps .env safe from Git commits
├── app.py               # FastAPI web backend server
├── main.py              # CLI application & unified launcher
├── requirements.txt     # Python dependencies
└── README.md            # Documentation & deployment guide
```

---

## 🚀 Quick Start (Running Locally)

### 1. Clone the Repository
```bash
git clone https://github.com/Hawi-T/e-news-fetcher.git
cd e-news-fetcher
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Free NewsAPI Key
1. Sign up for free at [newsapi.org/register](https://newsapi.org/register).
2. Copy your key and add it to `.env`:
```env
NEWS_API_KEY=your_actual_key_here
```

### 4. Run the Application

#### Option A: Launch in Your Web Browser (Recommended)
```bash
python app.py
```
This automatically starts the server and opens `http://127.0.0.1:8000` in your default browser!

#### Option B: Run in the Terminal (CLI)
```bash
python main.py
```

---

## ☁️ Free Cloud Deployment Guide

You can deploy this web application for free on **Render** in just 3 minutes:

### Deploying to Render.com (Free Tier)
1. Push your code to your GitHub repository ([Hawi-T/e-news-fetcher](https://github.com/Hawi-T/e-news-fetcher)).
2. Go to [Render.com](https://render.com) and sign in with GitHub.
3. Click **New +** > **Web Service**.
4. Select your **`e-news-fetcher`** repository.
5. Set the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Scroll down to **Environment Variables** and add:
   - Key: `NEWS_API_KEY`
   - Value: *(your actual NewsAPI key)*
7. Click **Create Web Service**. Render will automatically build your app and give you a live public URL (e.g. `https://e-news-fetcher.onrender.com`)!

---

## 💡 How It Works Behind the Scenes

1. **Environment Variables**: `python-dotenv` loads `NEWS_API_KEY` safely without exposing secrets in your source code.
2. **FastAPI Backend (`app.py`)**: Acts as a secure proxy between your browser and `newsapi.org`, protecting your API key from being exposed to the client.
3. **Endpoint Filtering**: 
   - Uses `/v2/top-headlines` for curated categories.
   - Uses `/v2/everything` for broad keyword searches.
4. **Data Sanitization**: Automatically filters out missing fields and `[Removed]` takedown notices, guaranteeing a clean presentation.
