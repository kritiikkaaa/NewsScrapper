from flask import Flask, render_template, request, redirect, url_for
from scraper import extract_article_content
from nlp import analyze_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')

    if not url:
        return redirect(url_for('home'))

    article = extract_article_content(url)

    if 'text' in article:
        article.update(analyze_text(article['text']))
        articles = [article]
    else:
        articles = [article]

    return render_template('result.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)