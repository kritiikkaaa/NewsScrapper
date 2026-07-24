from urllib.parse import urlparse

from newspaper import Article, Config


def extract_article_content(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        return {"error": "Please enter a valid http or https article URL.", "url": url}

    try:
        config = Config()
        config.browser_user_agent = "Mozilla/5.0 (compatible; AI-News-Intelligence/1.0)"
        config.request_timeout = 15
        article = Article(url, config=config)
        article.download()
        article.parse()
        if not article.text.strip():
            raise RuntimeError("No readable article text was found at this URL.")
        return {"title": article.title or "Untitled article", "text": article.text, "summary": "", "url": url}
    except Exception as error:
        return {"error": "We could not read this article. The site may block automated access or the URL may not be an article.", "details": str(error), "url": url}
