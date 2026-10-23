import os
import json
import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Step 1: Load Environment Variables
# ---------------------------------------------------------------------------
# load_dotenv() searches for a .env file in the current folder and loads
# the variables inside it into Python's os.environ dictionary.
load_dotenv()


def fetch_news(topic_or_keyword, is_category=False, show_raw_json=False):
    """
    Sends an HTTP GET request to NewsAPI to fetch the top 5 articles.

    Parameters:
        topic_or_keyword (str): The search word or category name.
        is_category (bool): True if topic_or_keyword is a curated category.
        show_raw_json (bool): If True, prints raw JSON received from the API.

    Returns:
        dict or None: The parsed JSON response dictionary, or None if failed.
    """
    # 1. Retrieve the API key from environment variables
    api_key = os.getenv("NEWS_API_KEY")

    # Guard check: Ensure user replaced the placeholder
    if not api_key or api_key.strip() == "your_api_key_here":
        print("\n[Error] Missing API Key!")
        print("Please open the '.env' file and set NEWS_API_KEY to your free key from https://newsapi.org/register")
        return None

    # 2. Select endpoint and query parameters based on user choice
    # - "top-headlines" is best for categories like technology, sports, etc.
    # - "everything" is best for free-text search queries (e.g., "artificial intelligence")
    if is_category:
        endpoint = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": topic_or_keyword,
            "language": "en",
            "pageSize": 10,
            "apiKey": api_key
        }
    else:
        endpoint = "https://newsapi.org/v2/everything"
        params = {
            "q": topic_or_keyword,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": api_key
        }

    # 3. Make the HTTP GET request with error handling
    try:
        # We set a timeout (in seconds) so the app won't freeze forever if the server is slow
        response = requests.get(endpoint, params=params, timeout=10)

        # Convert the HTTP response body into a Python dictionary using .json()
        data = response.json()

        # Optional: Print raw JSON for learning and debugging
        if show_raw_json:
            print("\n" + "=" * 25 + " RAW JSON RESPONSE " + "=" * 25)
            print(json.dumps(data, indent=2))
            print("=" * 70 + "\n")

        # Handle API-level errors (like invalid key or rate limit)
        if response.status_code == 401:
            print("\n[Error] Invalid API Key (HTTP 401)!")
            print(f"API Message: {data.get('message', 'Unauthorized access.')}")
            print("Double-check the key in your .env file.")
            return None

        if response.status_code != 200 or data.get("status") != "ok":
            print(f"\n[Error] API returned status code {response.status_code}.")
            print(f"Message: {data.get('message', 'Unknown error.')}")
            return None

        return data

    except requests.exceptions.ConnectionError:
        print("\n[Error] No internet connection. Please check your network and try again.")
        return None
    except requests.exceptions.Timeout:
        print("\n[Error] The request timed out. NewsAPI server took too long to reply.")
        return None
    except requests.exceptions.RequestException as err:
        print(f"\n[Error] An unexpected network error occurred: {err}")
        return None


def parse_articles(raw_data):
    """
    Extracts and cleans up article fields from raw NewsAPI JSON.
    Safely handles missing or None fields (e.g., missing descriptions).

    Parameters:
        raw_data (dict): The dictionary returned by fetch_news.

    Returns:
        list[dict]: A list of clean article dictionaries.
    """
    if not raw_data:
        return []

    # Get list of articles from response; fallback to empty list if missing
    articles_list = raw_data.get("articles", [])

    cleaned_articles = []
    for item in articles_list:
        # NewsAPI sometimes returns takedown placeholders with title "[Removed]"
        title = item.get("title")
        if not title or title.strip() == "[Removed]":
            continue

        # Safe extraction for nested source: source can be None or a dict
        source_data = item.get("source") or {}
        source_name = source_data.get("name") or "Unknown Source"

        # Safe extraction with defaults for missing or empty fields
        description = item.get("description") or "No description provided."
        url = item.get("url") or "No link provided"

        cleaned_articles.append({
            "title": title.strip(),
            "source": source_name.strip(),
            "description": description.strip(),
            "url": url.strip()
        })

        # Stop once we have reached the desired top 5 articles
        if len(cleaned_articles) == 5:
            break

    return cleaned_articles


def display_articles(articles, topic_name):
    """
    Nicely formats and prints articles to the console.

    Parameters:
        articles (list[dict]): The cleaned articles.
        topic_name (str): The search keyword or category name.
    """
    if not articles:
        print(f"\nNo articles found for '{topic_name}'. Try another keyword or category!")
        return

    print("\n" + "=" * 70)
    print(f" TOP {len(articles)} NEWS HEADLINES: {topic_name.upper()}")
    print("=" * 70)

    for index, article in enumerate(articles, start=1):
        print(f"\n[{index}] {article['title']}")
        print(f"    Source      : {article['source']}")
        print(f"    Description : {article['description']}")
        print(f"    Link        : {article['url']}")
        print("-" * 70)


def main():
    """
    Main user loop for the command-line interface.
    """
    categories = {
        "1": "technology",
        "2": "sports",
        "3": "business",
        "4": "science",
        "5": "entertainment",
        "6": "health",
    }

    print("\n=======================================================")
    print("        WELCOME TO THE PYTHON NEWS FETCHER             ")
    print("=======================================================")

    while True:
        print("\nSelect an option:")
        print("  1. Technology")
        print("  2. Sports")
        print("  3. Business")
        print("  4. Science")
        print("  5. Entertainment")
        print("  6. Health")
        print("  7. Search by custom keyword")
        print("  8. Launch Web App in Browser")
        print("  9. Exit")

        choice = input("\nEnter choice (1-9): ").strip()

        if choice == "9":
            print("\nThanks for using News Fetcher. Goodbye!")
            break

        if choice == "8":
            print("\nStarting News Fetcher Web Server on http://127.0.0.1:8000 ...")
            import subprocess
            import sys
            subprocess.run([sys.executable, "app.py"])
            continue

        if choice in categories:
            topic = categories[choice]
            is_category = True
        elif choice == "7":
            topic = input("\nEnter search keyword (e.g. 'artificial intelligence', 'NASA'): ").strip()
            if not topic:
                print("Search keyword cannot be empty. Please try again.")
                continue
            is_category = False
        else:
            print("Invalid choice. Please select 1 through 9.")
            continue

        # Optional learning feature: Ask if the user wants to see the raw JSON
        inspect_json = input("Inspect raw JSON response before parsing? (y/n, default=n): ").strip().lower() == "y"

        print(f"\nFetching news for '{topic}'...")
        raw_data = fetch_news(topic, is_category=is_category, show_raw_json=inspect_json)

        if raw_data:
            articles = parse_articles(raw_data)
            display_articles(articles, topic)


if __name__ == "__main__":
    main()
