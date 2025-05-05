# -*- coding: utf-8 -*-
"""
main.py
Flask API exposing /search and /openapi.json endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
import json, re, pathlib

app = Flask(__name__)

# ---------- load the text index on start-up ----------
DATA_FILE = pathlib.Path("data/index.json")
if DATA_FILE.exists():
    with DATA_FILE.open() as fp:
        DOCS = json.load(fp)
else:
    DOCS = []
    print("⚠ data/index.json not found – run crawler.py and extract.py first")


@app.get("/")
def root():
    return {"message": "KCDC Planning Lookup API is running"}


@app.get("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify(error="Please supply a query via ?q="), 400

    regex = re.compile(re.escape(query), re.I)
    hits = []

    for doc in DOCS:
        if (match := regex.search(doc["text"])):
            snippet = doc["text"][max(0,
                                      match.start() - 120):match.end() + 120]
            hits.append({"url": doc["url"], "snippet": snippet.strip() + "…"})

        if len(hits) >= 10:
            break

    return jsonify(query=query, results=hits)


# ---------- serve the OpenAPI spec so ChatGPT can import it ----------
@app.get("/openapi.json")
def spec():
    return send_from_directory("static",
                               "openapi.json",
                               mimetype="application/json")


if __name__ == "__main__":
    # Replit expects the server on 0.0.0.0, port 3000
    app.run(host="0.0.0.0", port=3000)
