from newspaper import Article
import requests
from bs4 import BeautifulSoup

def get_article_links(base_url="https://news.ycombinator.com/"):
    res = requests.get(base_url)
    print("Status Code:", res.status_code)

    soup = BeautifulSoup(res.text, 'html.parser')

    links = [a['href'] for a in soup.select('.titleline a') if a['href'].startswith('http')]

    print("Links Found:", links)

    return links[:5]

def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "url": url
        }
    except Exception as e:
        return {"error": str(e), "url": url} 
    