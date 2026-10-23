import os
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ---------------------------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------------------------
load_dotenv()

app = FastAPI(
    title="News Fetcher API",
    description="Backend API for fetching and parsing global news headlines using NewsAPI",
    version="1.0.0"
)

# Mount the static folder for CSS, JavaScript, and assets
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the front-end user interface."""
    return FileResponse("static/index.html")


@app.get("/api/news")
async def get_news(
    topic: str = Query("technology", description="Category name or custom search query"),
    is_category: bool = Query(True, description="True for preset categories, False for keyword search")
):
    """
    Fetches the top news articles from NewsAPI, handles API errors safely,
    and returns both cleaned articles and raw JSON.
    """
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key or api_key.strip() == "your_api_key_here":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "message": "Missing API Key. Please add your valid NEWS_API_KEY to the .env file."
            }
        )

    # Choose endpoint based on category vs custom keyword search
    if is_category:
        endpoint = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": topic.lower(),
            "language": "en",
            "pageSize": 10,  # Request 10 to guarantee at least 5 after deduplication
            "apiKey": api_key
        }
    else:
        endpoint = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": api_key
        }

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        data = response.json()

        # Handle API authentication / authorization errors
        if response.status_code == 401:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "message": "Invalid API Key. Double-check your key in the .env file."
                }
            )

        if response.status_code != 200 or data.get("status") != "ok":
            return JSONResponse(
                status_code=response.status_code if response.status_code >= 400 else 500,
                content={
                    "status": "error",
                    "message": data.get("message", "NewsAPI server encountered an error.")
                }
            )

        # Parse & clean articles
        raw_articles = data.get("articles", [])
        cleaned_articles = []

        for item in raw_articles:
            title = item.get("title")
            # Skip takedown placeholders
            if not title or title.strip() == "[Removed]":
                continue

            source_data = item.get("source") or {}
            source_name = source_data.get("name") or "Unknown Source"
            description = item.get("description") or "No description provided."
            url = item.get("url") or "#"
            url_to_image = item.get("urlToImage")
            published_at = item.get("publishedAt")

            cleaned_articles.append({
                "title": title.strip(),
                "source": source_name.strip(),
                "description": description.strip(),
                "url": url.strip(),
                "urlToImage": url_to_image,
                "publishedAt": published_at
            })

            # Cap at top 5 curated articles
            if len(cleaned_articles) == 5:
                break

        return {
            "status": "ok",
            "totalResults": len(cleaned_articles),
            "articles": cleaned_articles,
            "raw": data
        }

    except requests.exceptions.ConnectionError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "message": "Network connection error. Please check your internet connectivity."
            }
        )
    except requests.exceptions.Timeout:
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={
                "status": "error",
                "message": "The request timed out. NewsAPI server took too long to reply."
            }
        )
    except Exception as err:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": f"Unexpected server error: {str(err)}"
            }
        )


if __name__ == "__main__":
    import threading
    import time
    import webbrowser

    port = int(os.environ.get("PORT", 8000))

    def open_browser():
        time.sleep(1.2)
        webbrowser.open(f"http://127.0.0.1:{port}")

    # Launch browser automatically for smooth local development
    threading.Thread(target=open_browser, daemon=True).start()

    print(f"\n=======================================================")
    print(f"       NEWS FETCHER WEB APP RUNNING ON PORT {port}     ")
    print(f"       Opening http://127.0.0.1:{port} in your browser... ")
    print(f"=======================================================\n")

    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
