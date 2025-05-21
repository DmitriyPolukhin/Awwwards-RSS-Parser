import feedparser

def fetch_rss_feed(url):
    articles = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Последние 5 записей
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            })
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        # articles is already []
    return articles

if __name__ == "__main__":
    rss_url = "https://www.awwwards.com/blog/feed/"
    articles = fetch_rss_feed(rss_url)
    for article in articles:
        print(f"{article['title']} - {article['link']}")