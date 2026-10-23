# 📰 Command-Line News Fetcher

A beginner-friendly Python command-line application that connects to [NewsAPI](https://newsapi.org) to fetch, parse, and display the latest top news headlines or custom keyword searches.

---

## 🌟 Features

- **Interactive CLI Menu**: Choose popular categories (Technology, Sports, Business, Science, Entertainment, Health) or search any custom keyword.
- **Top 5 Curated Articles**: Cleanly displays Article Title, News Source, Short Description, and Web Link.
- **Secure Secrets Management**: Keeps your API key private using `.env` and `python-dotenv`.
- **Robust Error Handling**:
  - Handles invalid / missing API keys (HTTP 401).
  - Handles network disconnects (`ConnectionError`) and timeouts (`Timeout`).
  - Handles missing fields (e.g., articles with missing descriptions or unknown sources).
  - Handles queries with 0 results.
- **Learning Mode**: Optional prompt to view the raw JSON data payload directly before it gets parsed.

---

## 📁 Project Structure

```text
News Fetcher/
├── .env                # Private API key (ignored by Git - NEVER commit this!)
├── .env.example        # Example template for setting up keys
├── .gitignore          # Tells Git to ignore .env and cache folders
├── main.py             # Main application logic and functions
├── requirements.txt    # Python dependencies list
└── README.md           # Documentation and setup instructions
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed on your computer.

### 2. Clone or Open the Repository
```bash
cd "News Fetcher"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Free NewsAPI Key
1. Visit [https://newsapi.org/register](https://newsapi.org/register) and create a free account.
2. Copy your API Key from the dashboard.

### 5. Configure Your `.env` File
Open the `.env` file in the project folder and replace `your_api_key_here` with your actual key:
```env
NEWS_API_KEY=1234567890abcdef1234567890abcdef
```

### 6. Run the App
```bash
python main.py
```

---

## 💡 How It Works (Concepts Explained)

1. **Environment Variables (`.env`)**: Secret tokens like API keys should never be hardcoded into Python files. `python-dotenv` loads key-value pairs into `os.environ` so your code remains safe to share publicly.
2. **HTTP GET Requests (`requests`)**: Communicates with web servers using the standard Web protocol to request data from NewsAPI endpoints (`/v2/top-headlines` or `/v2/everything`).
3. **Query Parameters**: Values appended to an API URL (like `?category=technology&pageSize=5&apiKey=...`) to filter and instruct the server on what exact data to send back.
4. **JSON Parsing (`data.json()`)**: The server returns JSON text (JavaScript Object Notation), which Python translates into native dictionaries and lists for easy manipulation.

---

## 📦 Pushing to GitHub

Run these commands in your project terminal:

```bash
# 1. Initialize git repository
git init

# 2. Stage all files (.gitignore automatically prevents .env from being added)
git add .

# 3. Create initial commit
git commit -m "Initial commit: Command-line News Fetcher in Python"

# 4. Set default branch to main
git branch -M main

# 5. Connect to your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/<YOUR-USERNAME>/news-fetcher.git

# 6. Push to GitHub
git push -u origin main
```
