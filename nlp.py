from collections import Counter
from io import BytesIO
from base64 import b64encode

import spacy
from textblob import TextBlob
from wordcloud import WordCloud

nlp_model = spacy.load("en_core_web_sm")


def sentiment_label(score):
    if score >= 0.6:
        return "Strongly Positive"
    if score >= 0.2:
        return "Positive"
    if score > -0.2:
        return "Neutral"
    if score > -0.6:
        return "Negative"
    return "Strongly Negative"


def subjectivity_label(score):
    if score >= 0.75:
        return "Highly Subjective"
    if score >= 0.5:
        return "Somewhat Subjective"
    if score >= 0.25:
        return "Somewhat Objective"
    return "Highly Objective"


def extract_keywords(doc, limit=10):
    terms = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and not token.is_stop and not token.is_punct and len(token) > 2
    ]
    return [{"text": term, "count": count} for term, count in Counter(terms).most_common(limit)]


def create_word_cloud(text):
    try:
        image = WordCloud(
            width=1200,
            height=600,
            background_color=None,
            mode="RGBA",
            colormap="viridis",
            stopwords=None,
            collocations=False,
        ).generate(text)
        buffer = BytesIO()
        image.to_image().save(buffer, format="PNG")
        return b64encode(buffer.getvalue()).decode("ascii")
    except ValueError:
        return None


def create_summary(doc, maximum_sentences=3):
    """Create a short extractive summary without requiring NLTK data files."""
    sentences = [sentence.text.strip() for sentence in doc.sents if sentence.text.strip()]
    if not sentences:
        return "No summary was generated for this article."
    return " ".join(sentences[:maximum_sentences])


def analyze_text(text, article_summary):
    doc = nlp_model(text)
    entities = []
    seen_entities = set()
    for entity in doc.ents:
        key = (entity.text.strip(), entity.label_)
        if key[0] and key not in seen_entities:
            seen_entities.add(key)
            entities.append({"text": key[0], "label": key[1]})
        if len(entities) == 12:
            break

    sentiment = TextBlob(text).sentiment
    word_count = len(text.split())
    entity_counts = Counter(entity["label"] for entity in entities)
    polarity = round(sentiment.polarity, 2)
    subjectivity = round(sentiment.subjectivity, 2)

    return {
        "summary": article_summary or create_summary(doc),
        "entities": entities,
        "entity_chart": {"labels": list(entity_counts), "values": list(entity_counts.values())},
        "keywords": extract_keywords(doc),
        "word_cloud": create_word_cloud(text),
        "word_count": word_count,
        "reading_time": max(1, round(word_count / 200)),
        "char_count": len(text),
        "sentiment": {
            "polarity": polarity,
            "polarity_label": sentiment_label(polarity),
            "subjectivity": subjectivity,
            "subjectivity_label": subjectivity_label(subjectivity),
        },
    }
