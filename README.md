# 📰 Command-Line News Fetcher

A beginner-friendly Python command-line application that connects to [NewsAPI](https://newsapi.org) to fetch, parse, and display the latest top news headlines or custom keyword searches.

---

## 🌟 Features

- **Interactive CLI Menu**: Choose popular categories (Technology, Sports, Business, Science, Entertainment, Health) or search any custom keyword.
- **Top 5 Curated Articles**: Cleanly displays Article Title, News Source, Short Description, and Web Link.
- **Secure Secrets Management**: Keeps your API key private using `.env` and `python-dotenv`.
- **Robust Error Handling**:
  - Handles invalid or missing API keys (HTTP 401).
  - Handles network disconnects (`ConnectionError`) and timeouts (`Timeout`).
  - Handles missing fields (e.g., articles with missing descriptions, deleted articles marked `[Removed]`, or unknown sources).
  - Handles queries with 0 results.
- **Learning Mode**: Optional prompt to view the raw JSON data payload directly before it gets parsed.

---

## 📁 Project Structure

```text
News Fetcher/
├── .env                # Private API key (ignored by Git - NEVER commit this!)
├── .env.example        # Example template for setting up keys
├── .gitignore          # Tells Git to ignore .env and cache folders
├── main.py             # Main application logic and modular functions
├── requirements.txt    # Python dependencies list
└── README.md           # Documentation and setup instructions
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed on your computer.

### 2. Clone or Open the Repository
```bash
git clone https://github.com/Hawi-T/e-news-fetcher.git
cd e-news-fetcher
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Free NewsAPI Key
1. Visit [https://newsapi.org/register](https://newsapi.org/register) and create a free account.
2. Copy your API Key from the dashboard.

### 5. Configure Your `.env` File
Create a `.env` file in the project folder (or copy from `.env.example`):
```bash
cp .env.example .env
```
Open `.env` and paste your actual API key:
```env
NEWS_API_KEY=your_actual_key_here
```

### 6. Run the App
```bash
python main.py
```

---

## 💻 Example Output

```text
=======================================================
        WELCOME TO THE PYTHON NEWS FETCHER             
=======================================================

Select an option:
  1. Technology
  2. Sports
  3. Business
  4. Science
  5. Entertainment
  6. Health
  7. Search by custom keyword
  8. Exit

Enter choice (1-8): 1
Inspect raw JSON response before parsing? (y/n, default=n): n

Fetching news for 'technology'...

======================================================================
 TOP 5 NEWS HEADLINES: TECHNOLOGY
======================================================================

[1] Phantom Blade Zero launch trailer, PS5 physical editions launch in 2027 - Gematsu
    Source      : Gematsu
    Description : S-GAME has released the launch trailer for Wuxia action RPG Phantom Blade Zero, as well as announced that physical standard, Deluxe, and Ultimate editions will launch for PlayStation 5 in 2027.
    Link        : https://www.gematsu.com/2026/10/phantom-blade-zero-launch-trailer-ps5-physical-editions-launch-in-2027
----------------------------------------------------------------------

[2] iPhone Duo Reviewers Really Miss Face ID - MacRumors
    Source      : MacRumors
    Description : Touch ID on the iPhone Duo might end up being frustrating for some users, based on media reviews that came out today. Multiple reviewers found Touch...
    Link        : https://www.macrumors.com/2026/10/21/iphone-duo-touch-id-complaints/
----------------------------------------------------------------------

[3] Giant iPhone Duo installations spotted at Apple Fifth Avenue ahead of Friday launch - 9to5Mac
    Source      : 9to5Mac
    Description : While the iPhone Duo doesn't launch until Friday, preparations are already underway at Apple's flagship Fifth Avenue store in New York for the big day.
    Link        : https://9to5mac.com/2026/10/21/giant-iphone-duo-installations-spotted-at-apple-fifth-avenue-ahead-of-friday-launch/
----------------------------------------------------------------------

[4] Xbox wants you to pay 24 to 40 cents per hour to stream games you already bought - Ars Technica
    Source      : Ars Technica
    Description : Time-based a la carte charges come on top of the purchase price for the games themselves.
    Link        : https://arstechnica.com/gaming/2026/10/xbox-wants-you-to-pay-24-to-40-cents-per-hour-to-stream-games-you-already-bought/
----------------------------------------------------------------------

[5] Bose acquires Skullcandy to help it reach a wider audience - The Verge
    Source      : The Verge
    Description : Details about the deal weren't revealed, but Skullcandy will remain a separate brand under Bose's premium consumer audio business.
    Link        : https://www.theverge.com/tech/1015276/bose-acquisition-skullcandy-headphones-earbuds-speakers
----------------------------------------------------------------------
```

---

## 💡 How It Works (Concepts Explained)

1. **Environment Variables (`.env`)**: Secret tokens like API keys should never be hardcoded into Python files. `python-dotenv` loads key-value pairs into `os.environ` so your code remains safe to share publicly.
2. **HTTP GET Requests (`requests`)**: Communicates with web servers using standard HTTP requests to fetch news data from NewsAPI endpoints (`/v2/top-headlines` or `/v2/everything`).
3. **Query Parameters**: Key-value pairs appended to an API URL (such as `?category=technology&pageSize=10&apiKey=...`) to instruct the server what data to filter and return.
4. **JSON Parsing (`data.json()`)**: The server returns JSON text (JavaScript Object Notation), which Python translates into native dictionaries and lists for safe indexing and extraction.

---

## 📦 Pushing Changes to GitHub

To push future updates:

```bash
git add .
git commit -m "Your descriptive commit message"
git push
```
