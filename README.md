# Briefly — AI News Intelligence

Paste a public English-language news URL to receive an AI summary, sentiment score, named entities, keyword analysis, word cloud, visual entity chart, and a downloadable PDF report.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Open `http://127.0.0.1:5000`.

## Notes

- Some publishers block automated readers; the app shows a clear error in that case.
- Reports are held in a small in-memory cache, so download them before restarting the server.
