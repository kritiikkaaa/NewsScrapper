import spacy
from textblob import TextBlob

nlp_model = spacy.load("en_core_web_sm")

def analyze_text(text):
    doc = nlp_model(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents][:10]
    sentiment = TextBlob(text).sentiment

    # Polarity labeling with more categories
    p = sentiment.polarity
    if p >= 0.6:
        polarity_label = "Strongly Positive"
    elif 0.2 <= p < 0.6:
        polarity_label = "Slightly Positive"
    elif -0.2 < p < 0.2:
        polarity_label = "Neutral"
    elif -0.6 < p <= -0.2:
        polarity_label = "Slightly Negative"
    else:  # p <= -0.6
        polarity_label = "Strongly Negative"

    # Subjectivity labeling with more categories
    s = sentiment.subjectivity
    if s >= 0.75:
        subjectivity_label = "Highly Subjective (Very Opinionated)"
    elif 0.5 <= s < 0.75:
        subjectivity_label = "Somewhat Subjective"
    elif 0.25 <= s < 0.5:
        subjectivity_label = "Somewhat Objective"
    else:  # s < 0.25
        subjectivity_label = "Highly Objective (Factual)"

    return {
        "summary": text[:500] + "...",
        "entities": entities,
        "sentiment": {
            "polarity": p,
            "polarity_label": polarity_label,
            "subjectivity": s,
            "subjectivity_label": subjectivity_label
        }
    }
