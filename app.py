from io import BytesIO
from uuid import uuid4

from flask import Flask, abort, make_response, redirect, render_template, request, url_for
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from nlp import analyze_text
from scraper import extract_article_content

app = Flask(__name__)
analysis_results = {}
MAX_CACHED_RESULTS = 50


def save_result(article):
    """Keep a small in-memory cache so a report can be downloaded."""
    result_id = str(uuid4())
    analysis_results[result_id] = article
    while len(analysis_results) > MAX_CACHED_RESULTS:
        analysis_results.pop(next(iter(analysis_results)))
    return result_id


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url", "").strip()
    if not url:
        return redirect(url_for("home"))

    article = extract_article_content(url)
    if "text" in article:
        article.update(analyze_text(article["text"], article.get("summary", "")))

    result_id = save_result(article)
    return redirect(url_for("result", result_id=result_id))


@app.route("/result/<result_id>")
def result(result_id):
    article = analysis_results.get(result_id)
    if article is None:
        abort(404)
    return render_template("result.html", article=article, result_id=result_id)


@app.route("/report/<result_id>.pdf")
def download_report(result_id):
    article = analysis_results.get(result_id)
    if article is None:
        abort(404)
    if "error" in article:
        return redirect(url_for("result", result_id=result_id))

    pdf_buffer = BytesIO()
    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
    )
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.textColor = colors.HexColor("#312E81")
    body_style = styles["BodyText"]
    body_style.leading = 16

    sentiment = article["sentiment"]
    keywords = ", ".join(keyword["text"] for keyword in article["keywords"])
    entities = ", ".join(f"{entity['text']} ({entity['label']})" for entity in article["entities"])
    story = [
        Paragraph("AI News Intelligence Report", title_style),
        Spacer(1, 0.22 * inch),
        Paragraph(article["title"], styles["Heading2"]),
        Paragraph(f"Source: {article['url']}", body_style),
        Spacer(1, 0.16 * inch),
        Paragraph("AI Summary", styles["Heading2"]),
        Paragraph(article["summary"] or "No summary was generated.", body_style),
        Spacer(1, 0.16 * inch),
        Paragraph("Insights", styles["Heading2"]),
        Paragraph(
            f"Sentiment: {sentiment['polarity_label']} ({sentiment['polarity']:+.2f})<br/>"
            f"Subjectivity: {sentiment['subjectivity_label']} ({sentiment['subjectivity']:.2f})<br/>"
            f"Words: {article['word_count']} | Reading time: {article['reading_time']} min<br/>"
            f"Keywords: {keywords or 'None detected'}<br/>"
            f"Entities: {entities or 'None detected'}",
            body_style,
        ),
    ]
    document.build(story)

    response = make_response(pdf_buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=news-intelligence-report.pdf"
    return response


if __name__ == "__main__":
    app.run(debug=True)
