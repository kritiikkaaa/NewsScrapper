from urllib.parse import urlparse

import nltk
from newspaper import Article, Config


def ensure_nltk_tokenizer_data():
    """Install the tokenizer data Newspaper3k needs for article summaries."""
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        if not nltk.download("punkt_tab", quiet=True):
            raise RuntimeError("NLTK tokenizer data could not be downloaded. Please try again while online.")


def extract_article_content(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        return {"error": "Please enter a valid http or https article URL.", "url": url}

    try:
        ensure_nltk_tokenizer_data()
        config = Config()
        config.browser_user_agent = "Mozilla/5.0 (compatible; AI-News-Intelligence/1.0)"
        config.request_timeout = 15
        article = Article(url, config=config)
        article.download()
        article.parse()
        if not article.text.strip():
            raise RuntimeError("No readable article text was found at this URL.")
        article.nlp()
        return {"title": article.title or "Untitled article", "text": article.text, "summary": article.summary, "url": url}
    except Exception as error:
        return {"error": "We could not read this article. The site may block automated access or the URL may not be an article.", "details": str(error), "url": url}
