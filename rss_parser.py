import feedparser

def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:5]:  # Последние 5 записей
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary
        })
    return articles

rss_url = "https://www.awwwards.com/blog/feed/"
articles = fetch_rss_feed(rss_url)
for article in articles:
    print(f"{article['title']} - {article['link']}")

    print("Начинаем парсить RSS...")
    articles = fetch_rss_feed(rss_url)
    print("Парсинг завершён.")