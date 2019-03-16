import feedparser


class MiscProvider():
    @staticmethod
    def rss(url):
        feed = feedparser.parse(url)
        result = [
            {
                "id": item.id,
                "href": item.link,
                "title": item.title,
                "date": item.published
            } for item in feed.entries
        ]
        organized = sorted(
            result,
            key=lambda item: item['date'],
            reverse=True
        )
        return organized[:200]
